import asyncio
from web3 import Web3
from web3.exceptions import InvalidAddress


class Web3Provider:
    def __init__(self, node_url: str):
        self.node_url = node_url
        self.web3 = Web3(Web3.AsyncHTTPProvider(node_url))

    async def is_address(self, address: str) -> bool:
        return self.web3.is_address(address)

    async def is_checksum_address(self, address: str) -> bool:
        try:
            return self.web3.is_checksum_address(address)
        except InvalidAddress:
            return False

    async def to_checksum_address(self, address: str) -> str:
        try:
            return self.web3.to_checksum_address(address)
        except InvalidAddress as e:
            raise ValueError(f"Invalid address: {address}") from e
