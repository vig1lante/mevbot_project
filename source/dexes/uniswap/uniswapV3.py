import asyncio
import os
from typing import Optional

from cryptography.fernet import Fernet
from pathlib import Path
from source.dexes.dex_class import DexClass
from source.json_reader import JsonReader
from arbitrage.multi_chain.constants import BSC
from service_settings import (
    PRIVATE_KEY,
    FERNET_CRYPT_KEY,
)
from source.abi_storage import AbiStorage, Net, SmartContractName
from source.dexes.dex_pool import DexPool


class UniSwapV3(DexClass):
    def __init__(
        self,
        node_url: str,
        fernet_key: str,
        private_key: str,
        router_address: str,
        factory_address: str,
        abi_factory: str,
        abi_router: str,
        abi_pool: str,
    ):
        super().__init__(node_url, fernet_key, private_key)
        self.router_address = router_address
        self.factory_address = factory_address
        self.abi_factory = abi_factory
        self.abi_router = abi_router
        self.abi_pool = abi_pool

    async def get_pool(
        self,
        first_address: str,
        second_address: str,
        fee: int,
    ) -> Optional[DexPool]:
        first_address = await self.web3.to_checksum_address(first_address)
        second_address = await self.web3.to_checksum_address(second_address)

        contract = await self.web3.contract(
            address=self.factory_address,
            abi=self.abi_factory,
        )

        if not await self.web3.is_checksum_address(first_address):
            return

        if not await self.web3.is_checksum_address(second_address):
            return

        pool = await contract.functions.getPool(
            first_address,
            second_address,
            fee,
        ).call()

        contract_pool = await self.web3.contract(address=pool, abi=self.abi_pool)

        return DexPool(
            "1",  # todo поправить в будущем
            "2",
            first_address,
            second_address,
            pool,
            contract_pool,
        )

    async def swap(
        self,
        amount_in: int,
        amount_out: int,
        token_in: str,
        token_out: str,
        abi_token_in: str,
        abi_token_out: str,
        pool_fee: int,
    ):
        token_in = await self.web3.to_checksum_address(token_in)
        token_out = await self.web3.to_checksum_address(token_out)

        decrypter = Fernet(FERNET_CRYPT_KEY)
        decrypted_from_private_key = decrypter.decrypt(
            bytes(PRIVATE_KEY, encoding="utf-8")
        ).decode(encoding="utf-8")

        from_address = await self.web3.from_key(decrypted_from_private_key)
        from_address = from_address.address
        from_wallet = await self.web3.to_checksum_address(from_address)

        token_in_contract = await self.web3.contract(
            address=token_in,
            abi=abi_token_in,
        )

        if (
            await token_in_contract.functions.allowance(
                from_address, self.router_address
            ).call()
            < amount_in
        ):
            await approve_token_spender(
                self.web3,
                token_in_contract,
                from_wallet,
                decrypted_from_private_key,
                self.router_address,
                await self.web3.to_wei(1000000, "ether"),
            )

        path = (
            await self.web3.to_bytes(hexstr=token_in)
            + pool_fee.to_bytes(3, "big")
            + await self.web3.to_bytes(hexstr=token_out)
        )

        router_contract = await self.web3.contract(
            address=self.router_address,
            abi=self.abi_router,
        )
        # Вызов функции exactInput
        tx = await router_contract.functions.exactInput(
            (
                path,
                from_wallet,
                amount_in,
                amount_out,
            )
        ).build_transaction(
            {
                "from": from_wallet,
                "gas": 500000,
                "gasPrice": await self.web3.gas_price(),
                "nonce": await self.web3.get_transaction_count(from_wallet),
            }
        )

        # Подписание и отправка транзакции
        signed_tx = await self.web3.sign_transaction(tx, decrypted_from_private_key)
        tx_hash = await self.web3.send_raw_transaction(signed_tx.rawTransaction)

        # Ожидание подтверждения транзакции
        receipt = await self.web3.wait_for_transaction_receipt(tx_hash)

        return receipt


async def approve_token_spender(
    w3, token_contract, from_wallet, from_private_key, spender, amount
):
    tx = await token_contract.functions.approve(spender, amount).build_transaction(
        {
            "from": from_wallet,
            "gas": 70000,
            "gasPrice": await w3.gas_price(),
            "nonce": await w3.get_transaction_count(from_wallet),
        }
    )

    # Подписание и отправка транзакции
    signed_tx = await w3.sign_transaction(tx, from_private_key)
    tx_hash = await w3.send_raw_transaction(signed_tx.rawTransaction)

    # Ожидание подтверждения транзакции
    receipt = await w3.wait_for_transaction_receipt(tx_hash)
    return receipt


async def main():
    config_dir = os.path.join(
        Path(__file__).resolve().parent.parent.parent.parent,
        "arbitrage",
        "multi_chain",
        "config.json",
    )
    config = JsonReader(config_dir)
    abi_storage = AbiStorage()
    abi_factory = abi_storage.get_abi(
        Net.BNB.value, SmartContractName.UniswapFactory.value
    )
    abi_router = abi_storage.get_abi(
        Net.BNB.value, SmartContractName.UniswapRouter.value
    )
    abi_pool = abi_storage.get_abi(Net.BNB.value, SmartContractName.UniswapPool.value)
    pair = config.pairs.get(BSC.PAIR)

    us = UniSwapV3(
        node_url="https://bsc-dataseed1.binance.org/",
        private_key=PRIVATE_KEY,
        fernet_key=FERNET_CRYPT_KEY,
        router_address=BSC.UNISWAP_ROUTER,
        factory_address=BSC.UNISWAP_FACTORY,
        abi_factory=abi_factory,
        abi_router=abi_router,
        abi_pool=abi_pool,
    )
    # pool = await us.get_pool(
    #     first_address=BSC.USDT,
    #     second_address=BSC.USDC,
    #     fee=int(pair.get("fee")),
    # )
    # print(pool)
    # print(await pool.fee())

    # usdt_abi = abi_storage.get_abi(Net.BNB.value, SmartContractName.USDT.value)
    # usdc_abi = abi_storage.get_abi(Net.BNB.value, SmartContractName.USDC.value)

    # swap = await ps.swap(
    #     amount_in=await ps.web3.to_wei(1, "ether"),
    #     amount_out=await ps.web3.to_wei(0.9, "ether"),
    #     token_in=BSC.USDT,
    #     token_out=BSC.USDC,
    #     abi_token_in=usdt_abi,
    #     abi_token_out=usdc_abi,
    #     pool_fee=int(pair.get("fee")),
    # )
    # print(swap)


if __name__ == "__main__":
    asyncio.run(main())
