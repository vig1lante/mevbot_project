import asyncio
import os
from utils import get_abi
from pathlib import Path
from cryptography.fernet import Fernet
from source.dexes.dex_class import DexClass
from source.json_reader import JsonReader

from arbitrage.multi_chain.constants import BSC
from service_settings import (
    PRIVATE_KEY,
    FERNET_CRYPT_KEY,
)

# from web3 import Web3


class PancakeSwapV3(DexClass):
    def __init__(
        self,
        node_url: str,
        fernet_key: str,
        private_key: str,
        router_address: str,
        factory_address: str,
    ):
        super().__init__(node_url, fernet_key, private_key)
        self.router_address = router_address
        self.factory_address = factory_address
        self.abi_factory = get_abi(BSC.NAME, "pancake_swap_factory.abi")
        self.abi_router = get_abi(BSC.NAME, "pancake_swap_router.abi")

    async def get_pool(
        self,
        first_address: str,
        second_address: str,
        fee: int,
    ):

        abi = ""
        with open(file=self.abi_factory, mode="r") as file:
            abi = file.readline()

        contract = await self.web3.contract(
            address=self.factory_address,
            abi=abi,
        )

        first_address = await self.web3.to_checksum_address(first_address)
        second_address = await self.web3.to_checksum_address(second_address)

        is_check_sum_usdt = await self.web3.is_checksum_address(first_address)
        is_check_sum_usdc = await self.web3.is_checksum_address(second_address)

        if is_check_sum_usdt and is_check_sum_usdc:
            pool = await contract.functions.getPool(
                first_address,
                second_address,
                fee,
            ).call()
            return pool

    async def swap(
        self,
        to_address: str,
        amount: int,
        price_limit: int,
    ):
        decrypter = Fernet(FERNET_CRYPT_KEY)
        decrypted_from_private_key = decrypter.decrypt(
            bytes(PRIVATE_KEY, encoding="utf-8")
        ).decode(encoding="utf-8")

        from_address = self.web3.web3.eth.account.from_key(  # todo добавить в провайдер
            decrypted_from_private_key
        ).address
        from_wallet = await self.web3.to_checksum_address(from_address)

        path = self.web3.web3.to_bytes(hexstr=BSC.USDT) + self.web3.web3.to_bytes(
            hexstr=BSC.USDC
        )

        abi = ""
        with open(file=self.abi_router, mode="r") as file:
            abi = file.readline()

        router_contract = await self.web3.contract(
            address=self.router_address,
            abi=abi,
        )
        to_address = await self.web3.to_checksum_address(to_address)
        # Вызов функции exactInput
        tx = router_contract.functions.exactInput(
            (
                path,
                to_address,
                amount,
                price_limit,
            )
        ).build_transaction(
            {
                "from": from_wallet,
                "gas": 300000,
                "gasPrice": await self.web3.gas_price(),
                "nonce": self.web3.web3.eth.get_transaction_count(
                    from_wallet
                ),  # todo добавить в провайдер
            }
        )

        # Подписание и отправка транзакции
        signed_tx = await self.web3.sign_transaction(tx)
        tx_hash = await self.web3.send_raw_transaction(signed_tx.rawTransaction)

        # Ожидание подтверждения транзакции
        receipt = await self.web3.wait_for_transaction_receipt(tx_hash)

        return receipt


async def main():
    config_dir = os.path.join(
        Path(__file__).resolve().parent.parent.parent.parent,
        "arbitrage",
        "multi_chain",
        "config.json",
    )
    config = JsonReader(config_dir)
    pair = config.pairs.get(BSC.PAIR)

    ps = PancakeSwapV3(
        node_url="https://bsc-dataseed1.binance.org/",
        private_key=PRIVATE_KEY,
        fernet_key=FERNET_CRYPT_KEY,
        router_address=BSC.PANCAKE_SWAP_ROUTER,
        factory_address=BSC.PANCAKE_SWAP_FACTORY,
    )
    pool = await ps.get_pool(
        BSC.USDT,
        BSC.USDC,
        int(pair.get("fee")),
    )
    print(pool)
    # w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed1.binance.org/"))
    # swap = await ps.swap(
    #     "0xCcF4ad12B17C07C82f3d8EB5C6453Be46497C27c",
    #     w3.to_wei(1, "ether"),
    #     w3.to_wei(0.99, "ether"),
    # )
    # print(swap)


if __name__ == "__main__":
    asyncio.run(main())
