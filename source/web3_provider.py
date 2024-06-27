import asyncio
from typing import Union, Type

from hexbytes import HexBytes
from web3 import Web3
from web3.contract import Contract
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
)

from eth_typing import (
    Address,
    BlockNumber,
    ChecksumAddress,
    HexStr,
)


class Web3Provider:
    def __init__(self, node_url: str):
        self.node_url = node_url
        self.web3 = Web3(Web3.AsyncHTTPProvider(node_url))

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
        return self.web3.eth.max_priority_fee

    async def gas_price(self) -> Wei:
        return self.web3.eth.gas_price

    async def chain_id(self) -> int:
        return self.web3.eth.chain_id

    async def get_balance(self, address: Union[Address, ChecksumAddress, ENS]) -> Wei:
        if not await self.is_address(address):
            raise ValueError(f"Invalid address: {address}")
        return self.web3.eth.get_balance(address)

    async def get_block_number(self) -> BlockNumber:
        return self.web3.eth.block_number

    async def get_block(self, block_identifier) -> BlockData:
        return self.web3.eth.get_block(block_identifier)

    async def get_transaction(self, transaction_hash: _Hash32) -> TxData:
        try:
            return self.web3.eth.get_transaction(transaction_hash)
        except TransactionNotFound:
            raise ValueError(f"Transaction not found: {transaction_hash}")

    async def wait_for_transaction_receipt(
        self, transaction_hash: _Hash32, timeout: int = 120
    ) -> TxReceipt:
        return self.web3.eth.wait_for_transaction_receipt(
            transaction_hash, timeout=timeout
        )

    async def get_transaction_receipt(self, transaction_hash: _Hash32) -> TxReceipt:
        try:
            return self.web3.eth.get_transaction_receipt(transaction_hash)
        except TransactionNotFound:
            raise ValueError(f"Transaction receipt not found: {transaction_hash}")

    async def send_raw_transaction(
        self, signed_transaction: Union[HexStr, bytes]
    ) -> HexBytes:
        return self.web3.eth.send_raw_transaction(signed_transaction)

    async def sign_transaction(self, transaction: dict, private_key) -> dict:
        return self.web3.eth.account.sign_transaction(transaction, private_key)

    async def estimate_gas(self, transaction: dict) -> int:
        return self.web3.eth.estimate_gas(transaction)

    async def contract(
        self, address: Union[Address, ChecksumAddress, ENS], abi: list
    ) -> Union[Type[Contract], Contract]:
        if not await self.is_address(address):
            raise ValueError(f"Invalid address: {address}")
        return self.web3.eth.contract(address=address, abi=abi)
