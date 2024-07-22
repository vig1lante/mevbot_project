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
from source.abi_storage import AbiStorage, Net, SmartContractName
from source.dexes.dex_pool import DexPool


class QuickSwap(DexClass):
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
        deadline: int = 60,  # временной лимит, в течение которого операция обмена токенов должна быть выполнена. Если операция не завершится в течение указанного deadline, то она будет отменена.
    ):
        super().__init__(node_url, fernet_key, private_key)
        self.router_address = router_address
        self.factory_address = factory_address
        self.abi_factory = abi_factory
        self.abi_router = abi_router
        self.abi_pool = abi_pool
        self.deadline = deadline

    async def get_pool(
        self,
        first_address: str,
        second_address: str,
        fee: int,
    ):

        contract = await self.web3.contract(
            address=self.factory_address,
            abi=self.abi_factory,
        )

        first_address = await self.web3.to_checksum_address(first_address)
        second_address = await self.web3.to_checksum_address(second_address)

        is_check_sum_usdt = await self.web3.is_checksum_address(first_address)
        is_check_sum_usdc = await self.web3.is_checksum_address(second_address)

        if is_check_sum_usdt and is_check_sum_usdc:
            pool = await contract.functions.poolByPair(
                first_address,
                second_address,
            ).call()
            contract_pool = await self.web3.contract(address=pool, abi=self.abi_pool)
            return DexPool(
                "1",
                "2",
                first_address,
                second_address,
                pool,
                contract_pool,
            )

    async def multiple_swap(
        self,
        amount_in: int,
        amount_out: int,
        tokens: list,
        abi_tokens: list,
        pool_fee: list,
    ):
        pass

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
        decrypter = Fernet(FERNET_CRYPT_KEY)
        decrypted_from_private_key = decrypter.decrypt(
            bytes(PRIVATE_KEY, encoding="utf-8")
        ).decode(encoding="utf-8")

        from_address = await self.web3.from_key(decrypted_from_private_key)
        from_address = from_address.address
        from_wallet = await self.web3.to_checksum_address(from_address)
        token_in = await self.web3.to_checksum_address(token_in)
        token_out = await self.web3.to_checksum_address(token_out)

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
                self.deadline,
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
