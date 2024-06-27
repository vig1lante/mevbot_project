import asyncio

from source.dexes.dex_class import DexClass
from arbitrage.multi_chain.constants import BSC


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

    async def get_pool(
        self,
    ):
        abi = ""
        with open(
            file="mevbot_project\abis\bsc\pancake_swap_factory.abi", mode="r"
        ) as file:
            abi = file.readline()

        contract = await self.web3.contract(
            address=self.factory_address,
            abi=abi,
        )
        if await self.web3.is_checksum_address(
            BSC.USDT
        ) and await self.web3.is_checksum_address(BSC.USDC):
            return await contract.functions.getPool(
                await self.web3.to_checksum_address(BSC.USDT),
                await self.web3.to_checksum_address(BSC.USDC),
            )

    async def swap(
        self,
    ): ...


async def main():
    from web3 import AsyncWeb3, AsyncHTTPProvider

    w3 = AsyncWeb3(AsyncHTTPProvider("https://zkevm-rpc.com"))
    a = await w3.eth.block_number
    print(a)


if __name__ == "__main__":
    asyncio.run(main())
