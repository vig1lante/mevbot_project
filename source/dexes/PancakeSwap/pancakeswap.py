import asyncio

from source.dexes.dex_class import DexClass
from arbitrage.multi_chain.constants import BSC
from service_settings import (
    PRIVATE_KEY,
    FERNET_CRYPT_KEY,
)


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
        first_address: str,
        second_address: str,
        fee: int,
    ):
        abi = ""
        with open(
            file="C:\\Users\\DANIL\\Projects\\mevbot_project\\abis\\bsc\\pancake_swap_factory.abi",  # todo допилить автоматическое нахождение нужных abi в файлах проекта
            mode="r",
        ) as file:
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
                fee,  # todo допилить читалку json
            ).call()
            return pool

    async def swap(
        self,
    ): ...


async def main():
    from web3 import AsyncWeb3, AsyncHTTPProvider

    ps = PancakeSwapV3(
        node_url="https://bsc-dataseed1.binance.org/",
        private_key=PRIVATE_KEY,
        fernet_key=FERNET_CRYPT_KEY,
        router_address=BSC.PANCAKE_SWAP_ROUTER,
        factory_address=BSC.PANCAKE_SWAP_ROUTER,
    )
    pool = await ps.get_pool(
        BSC.USDT,
        BSC.USDC,
        10000,
    )
    print(pool)


if __name__ == "__main__":
    asyncio.run(main())
