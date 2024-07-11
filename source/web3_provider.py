import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Union, Type, Optional, Any, Literal
import aiohttp
from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.contract import Contract, AsyncContract
from web3.exceptions import InvalidAddress, TransactionNotFound
from web3.types import (
    ENS,
    BlockData,
    BlockIdentifier,
    BlockParams,
    CallOverride,
    CreateAccessListResponse,
    FeeHistory,
    FilterParams,
    LogReceipt,
    MerkleProof,
    Nonce,
    SignedTx,
    SyncStatus,
    TxData,
    TxParams,
    TxReceipt,
    Uncle,
    Wei,
    _Hash32,
    Hash32
)
from eth_typing import (
    Address,
    BlockNumber,
    ChecksumAddress,
    HexStr,
)
from eth_account.signers.local import (
    LocalAccount
)
from decimal import Decimal

class Web3Provider:
    def __init__(self, node_url: str):
        self.node_url = node_url
        self.web3 = AsyncWeb3(AsyncHTTPProvider(node_url))

    @staticmethod
    async def create_session():
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        return session

    async def is_address(self, address: Union[Address, ChecksumAddress, ENS]) -> bool:
        return self.web3.is_address(address)

    async def is_checksum_address(
        self, address: Union[Address, ChecksumAddress, ENS]
    ) -> bool:
        try:
            return self.web3.is_checksum_address(address)
        except InvalidAddress:
            return False

    async def to_checksum_address(
        self, address: Union[Address, ChecksumAddress, ENS]
    ) -> ChecksumAddress:
        try:
            return self.web3.to_checksum_address(address)
        except InvalidAddress as e:
            raise ValueError(f"Invalid address: {address}") from e

    async def max_priority_fee(self) -> Wei:
        return await self.web3.eth.max_priority_fee

    async def gas_price(self) -> Wei:
        return await self.web3.eth.gas_price

    async def chain_id(self) -> int:
        return await self.web3.eth.chain_id

    async def get_balance(self, address: Union[Address, ChecksumAddress, ENS]) -> Wei:
        if not await self.is_address(address):
            raise ValueError(f"Invalid address: {address}")
        return await self.web3.eth.get_balance(address)

    async def get_block_number(self) -> BlockNumber:
        return await self.web3.eth.block_number

    async def get_block(self, block_identifier) -> BlockData:
        return await self.web3.eth.get_block(block_identifier)

    async def get_transaction(self, transaction_hash: _Hash32) -> TxData:
        try:
            return await self.web3.eth.get_transaction(transaction_hash)
        except TransactionNotFound:
            raise ValueError(f"Transaction not found: {transaction_hash}")

    async def wait_for_transaction_receipt(
        self, transaction_hash: _Hash32, timeout: int = 120
    ) -> TxReceipt:
        return await self.web3.eth.wait_for_transaction_receipt(
            transaction_hash, timeout=timeout
        )

    async def get_transaction_receipt(self, transaction_hash: _Hash32) -> TxReceipt:
        try:
            return await self.web3.eth.get_transaction_receipt(transaction_hash)
        except TransactionNotFound:
            raise ValueError(f"Transaction receipt not found: {transaction_hash}")

    async def send_raw_transaction(
        self, signed_transaction: Union[HexStr, bytes]
    ) -> HexBytes:
        return await self.web3.eth.send_raw_transaction(signed_transaction)

    async def sign_transaction(
        self,
        transaction_dict: dict,
        private_key: Any,
        blobs: Any = None
    ) -> SignedTransaction:
        return self.web3.eth.account.sign_transaction(transaction_dict=transaction_dict, private_key=private_key, blobs=blobs)

    async def estimate_gas(self, transaction: dict) -> int:
        return await self.web3.eth.estimate_gas(transaction)

    async def contract(
        self,
        address: Optional[Union[Address, ChecksumAddress, ENS]] = None,
        **kwargs: Any,
    ) -> AsyncContract:
        if not await self.is_address(address):
            raise ValueError(f"Invalid address: {address}")
        return self.web3.eth.contract(address=address, **kwargs)

    async def from_key(
        self,
        private_key: Any
    ) -> LocalAccount:
        return self.web3.eth.account.from_key(private_key=private_key)

    async def to_bytes(
        self,
        primitive: bytes | int | bool | None = None,
        hexstr: HexStr | None = None,
        text: str | None = None
    ) -> bytes:
        return self.web3.to_bytes(primitive=primitive, hexstr=hexstr, text=text)

    async def to_wei(
        self,
        number: int | float | str | Decimal,
        unit: str
    ) -> Wei:
        return self.web3.to_wei(number=number, unit=unit)

    async def from_wei(
        self,
        number: int,
        unit: str
    ) -> int | Decimal:
        return self.web3.from_wei(number=number, unit=unit)

    async def get_transaction_count(
            self,
            account: Address | ChecksumAddress | ENS,
            block_identifier: Literal["latest", "earliest", "pending", "safe", "finalized"] | BlockNumber | Hash32 | HexStr | HexBytes | int | None = None
    ) -> Nonce:
        return await self.web3.eth.get_transaction_count(account=account, block_identifier=block_identifier)
# async def main():
#     w = Web3Provider("https://zkevm-rpc.com")
#
#     async with await w.create_session() as session:
#         await w.web3.provider.cache_async_session(session)
#         a = await w.get_block_number()
#         b = await w.gas_price()
#         c = await w.chain_id()
#         print(a)
#         print(b)
#         print(c)
#
# if __name__ == "__main__":
#     asyncio.run(main())
