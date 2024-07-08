from abc import ABC, abstractmethod
from source.web3_provider import Web3Provider

from typing import Optional


class DexClass(ABC):
    def __init__(
        self,
        node_url: str,
        fernet_key: str,
        private_key: str,
    ):
        self.web3 = Web3Provider(node_url)
        self.fernet_key = fernet_key
        self.private_key = private_key

    @abstractmethod
    async def swap(
        self,
        to_address: str,
        amount_in: int,
        amount_out: int,
        token_in: str,
        token_out: str,
        abi_token_in: str,
        abi_token_out: str,
        pool_fee: int,
    ): ...

    async def multiple_swap(
        self,
        to_address: str,
        amount_in: int,
        amount_out: int,
        tokens: list,
        abi_tokens: list,
        pool_fee: list,
    ): ...

    @abstractmethod
    async def get_pool(
        self,
        first_address: str,
        second_address: str,
        fee: int,
    ): ...
