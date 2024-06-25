from abc import ABC, abstractmethod
from web3 import Web3

from typing import Optional


class DexClass(ABC):
    def __init__(
            self,
            provider_url: str,
            fernet_key: str,
            private_key: str,
    ):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.fernet_key = fernet_key
        self.private_key = private_key

    @abstractmethod
    def is_address(self, address: str) -> bool:
        ...

    @abstractmethod
    def is_checksum_address(self, address: str) -> str:
        ...

    @abstractmethod
    def to_checksum_address(self, address: str) -> str:
        ...

    @abstractmethod
    def max_priority_fee(self) -> int:
        ...

    @abstractmethod
    def gas_price(self) -> int:
        ...

    @abstractmethod
    def chain_id(self) -> int:
        ...

    @abstractmethod
    def get_balance(self, address: str, block_identifier: int):
        ...

    @abstractmethod
    def get_block_number(self) -> int:
        ...

    @abstractmethod
    def get_block(
            self,
            block_identifier: int,
            full_transactions: bool,
    ):
        ...

    @abstractmethod
    def get_transaction(self, transaction_hash):
        ...

    @abstractmethod
    def wait_for_transaction_receipt(
            self,
            transaction_hash,
            timeout: int,
            poll_latency: int,
    ):
        ...

    @abstractmethod
    def get_transaction_receipt(self, transaction_hash):
        ...

    @abstractmethod
    def send_raw_transaction(self, raw_transaction):
        ...

    @abstractmethod
    def sign_transaction(self, transaction_dict):
        ...

    @abstractmethod
    def estimate_gas(
            self,
            transaction,
            block_identifier: Optional[int] = None,
            state_override: Optional[int] = None,
    ):
        ...

    @abstractmethod
    def contract(
            self,
            address: Optional[str] = None,
            contract_name: Optional[str] = None,
            factory_: Optional[str] = None,
            abi: Optional[str] = None,
            **kwargs,
    ):
        ...

    @abstractmethod
    def swap(self, ):
        ...

    @abstractmethod
    def get_pool(self, ):
        ...
