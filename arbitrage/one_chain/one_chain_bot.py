import asyncio
from constants import BSC
from source.logger import one_chain_bot_logger
from source.dexes.dex_class import DexClass
from source.dexes.dex_pool import DexPool
from source.dexes.pancakeswap.v3.pancakeswapV3 import PancakeSwapV3, PancakeSwapV3Pool
from source.dexes.uniswap.v3.uniswapV3 import UniSwapV3, UniSwapV3Pool
# from source.dexes.quickswap.v3.quickswapV3 import QuickSwap, QuickSwapV3Pool
from service_settings import (
    PRIVATE_KEY,
    FERNET_CRYPT_KEY,
)
from source.abi_storage import AbiStorage, Net, SmartContractName

#todo константы

class OneChainBot:

    def set_pool_settings(self):

        network = Net.BNB.value

        dexes_list = BSC.DEX_LIST

        self.fee = int(BSC.FEE)

        self.basic_asset_address = BSC.USDT

        self.asset_address = BSC.USDC

        return network, dexes_list

    def initialize_dex(self, network: str, dex_name: str, abi_storage: AbiStorage) -> DexClass:
        if network == Net.BNB.value:

            if dex_name == "PancakeSwap":

                abi_factory = abi_storage.get_abi(
                    Net.BNB.value, SmartContractName.PancakeSwapFactory.value
                )
                abi_router = abi_storage.get_abi(
                    Net.BNB.value, SmartContractName.PancakeSwapRouter.value
                )
                abi_pool = abi_storage.get_abi(
                    Net.BNB.value, SmartContractName.PancakeSwapV3Pool.value
                )

                dex = PancakeSwapV3(
                    node_url="https://bsc-dataseed1.binance.org/",
                    private_key=PRIVATE_KEY,
                    fernet_key=FERNET_CRYPT_KEY,
                    router_address=BSC.PANCAKE_SWAP_ROUTER,
                    factory_address=BSC.PANCAKE_SWAP_FACTORY,
                    abi_factory=abi_factory,
                    abi_router=abi_router,
                    abi_pool=abi_pool,
                )

            if dex_name == "Uniswap":

                abi_factory = abi_storage.get_abi(
                    Net.BNB.value, SmartContractName.UniswapFactory.value
                )
                abi_router = abi_storage.get_abi(
                    Net.BNB.value, SmartContractName.UniswapRouter.value
                )
                abi_pool = abi_storage.get_abi(Net.BNB.value, SmartContractName.UniswapPool.value)

                dex = UniSwapV3(
                    node_url="https://bsc-dataseed1.binance.org/",
                    private_key=PRIVATE_KEY,
                    fernet_key=FERNET_CRYPT_KEY,
                    router_address=BSC.UNISWAP_ROUTER,
                    factory_address=BSC.UNISWAP_FACTORY,
                    abi_factory=abi_factory,
                    abi_router=abi_router,
                    abi_pool=abi_pool,
                )
            # if dex_name == "Quickswap":
            #     dex = QuickSwap(
            #         node_url="https://bsc-dataseed1.binance.org/",
            #         private_key=const.PRIVATE_KEY,
            #         fernet_key=const.FERNET_CRYPT_KEY,
            #         router_address=const.QUICKSWAP_ROUTER,
            #         factory_address=const.QUICKSWAP_FACTORY,
            # )
            else:
                raise ValueError(f"Invalid DEX name: {dex_name}")
        return dex

    def create_pool(self, dex: DexClass) -> DexPool:
        pool = await dex.get_pool(
            first_address=self.asset_address,
            second_address=self.basic_asset_address,
            fee=self.fee
        )
        return pool

    def set_tradings_variables(self, network, dexes_list):

        abi_storage = AbiStorage()

        self.basic_asset_abi = abi_storage.get_abi(Net.BNB.value, SmartContractName.USDT.value)
        self.asset_abi = abi_storage.get_abi(Net.BNB.value, SmartContractName.USDC.value)

        self.first_dex = None
        for dex_name in dexes_list:
            if self.first_dex == None:
                self.first_dex = self.initialize_dex(network, dex_name, abi_storage)
                self.first_pool = self.create_pool(self.first_dex)
            else:
                self.second_dex = self.initialize_dex(network, dex_name, abi_storage)
                self.second_pool = self.create_pool(self.second_dex)

    def work(self):
        try:
            first_pool_price = await self.first_pool.get_token0_price()
            second_pool_price = await self.second_pool.get_token0_price()

            if first_pool_price == second_pool_price:
                return

            elif first_pool_price < second_pool_price:
                await self.first_dex.swap(
                    amount_in=await self.first_dex.web3.to_wei(1, "ether"),
                    amount_out=await self.first_dex.web3.to_wei(0.9, "ether"),
                    token_in=self.basic_asset_address,
                    token_out=self.asset_address,
                    abi_token_in=self.basic_asset_abi,
                    abi_token_out=self.asset_abi,
                    pool_fee=self.fee
                )
                await self.second_dex.swap(
                    amount_in=await self.second_dex.web3.to_wei(1, "ether"),
                    amount_out=await self.second_dex.web3.to_wei(0.9, "ether"),
                    token_in=self.asset_address,
                    token_out=self.basic_asset_address,
                    abi_token_in=self.asset_abi,
                    abi_token_out=self.basic_asset_abi,
                    pool_fee=self.fee
                )

            elif first_pool_price > second_pool_price:
                await self.second_dex.swap(
                    amount_in=await self.second_dex.web3.to_wei(1, "ether"),
                    amount_out=await self.second_dex.web3.to_wei(0.9, "ether"),
                    token_in=self.basic_asset_address,
                    token_out=self.asset_address,
                    abi_token_in=self.basic_asset_abi,
                    abi_token_out=self.asset_abi,
                    pool_fee=self.fee
                )
                await self.first_dex.swap(
                    amount_in=await self.first_dex.web3.to_wei(1, "ether"),
                    amount_out=await self.first_dex.web3.to_wei(0.9, "ether"),
                    token_in=self.asset_address,
                    token_out=self.basic_asset_address,
                    abi_token_in=self.asset_abi,
                    abi_token_out=self.basic_asset_abi,
                    pool_fee=self.fee
                )

        except Exeption as e:
            one_chain_bot_logger.error(f"Error accrued- {str(e)}")

def main():
    try:

        # todo что передается адрес токена или его имя
        network, dexes_list = OneChainBot.set_pool_settings()

        OneChainBot.set_tradings_variables(network=network,
                                           dexes_list=dexes_list
        )

        while True:
            OneChainBot.work()

    except Exeption as e:
        one_chain_bot_logger.exeption(f"One chain bot error- {str(e)}")