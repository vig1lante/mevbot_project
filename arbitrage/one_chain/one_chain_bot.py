import asyncio
from source.logger import arbitrage_one_chain_bot_logger
from source.dexes import pancakeswap, quickswap, uniswapV2

#todo константы

class OneChainBot:

    def set_pool_settings(self):

        network, asset, dexes_list, basic_asset = magick_get_settings()

        if basic_asset == None:
            self.basic_asset_address = const.USDT_ADDRESS
        else:
            self.basic_asset_address = basic_asset

        self.asset_address = asset

        return network, dexes_list

    def initialize_dex(self, network: str, dex_name: str) -> DexClass:
        if network == "Polygon":
            if dex_name == "PancakeSwap":
                dex = pancakeswap.PancakeSwapV3(
                node_url=const.POLYGON_NODE_URL,
                private_key=const.PRIVATE_KEY,
                fernet_key=const.FERNET_CRYPT_KEY,
                router_address=const.PANCAKE_SWAP_ROUTER,
                factory_address=const.PANCAKE_SWAP_FACTORY,
            )
            if dex_name == "Uniswap":
                dex = uniswapV2.UniSwapV2(
                node_url=const.POLYGON_NODE_URL,
                private_key=const.PRIVATE_KEY,
                fernet_key=const.FERNET_CRYPT_KEY,
                router_address=const.UNISWAP_ROUTER,
                factory_address=const.UNISWAP_FACTORY,
            )
            if dex_name == "Quickswap":
                dex = quickswap.QickSwap(
                node_url=const.POLYGON_NODE_URL,
                private_key=const.PRIVATE_KEY,
                fernet_key=const.FERNET_CRYPT_KEY,
                router_address=const.QUICKSWAP_ROUTER,
                factory_address=const.QUICKSWAP_FACTORY,
            )
            else:
                raise ValueError(f"Invalid DEX name: {dex_name}")
        return dex

    def create_pool(self, dex) -> DexPool:
        await dex.get_pool(
            first_address=self.asset_address,
            second_address=self.basic_asset_address,
            fee=self.fee
        )
        return pool

    def set_tradings_variables(self, network, dexes_list):
        # todo реализовать получение pair
        pair = config.pairs.get(BSC.PAIR)
        self.fee = int(pair.get("fee"))

        self.first_dex = None

        for dex_name in dexes_list:
            if self.first_dex == None:
                self.first_dex = self.initialize_dex(network, dex_name)
                self.first_pool = self.create_pool(self.first_dex)
            else:
                self.second_dex = self.initialize_dex(network, dex_name)
                self.second_pool = self.create_pool(self.second_dex)

    def work(self):
        try:
            first_pool_price = await self.first_pool.get_token0_price()
            second_pool_price = await self.second_pool.get_token0_price()

            if first_pool_price == second_pool_price:
                return

            elif first_pool_price < second_pool_price:
                await self.first_dex.swap(
                    to_address=PUBLIC_KEY,
                    amount_in=await self.first_dex.web3.to_wei(1, "ether"),
                    amount_out=await self.first_dex.web3.to_wei(0.9, "ether"),
                    token_in=self.basic_asset_address,
                    token_out=self.asset_address,
                    abi_token_in=ERC20_abi,
                    abi_token_out=ERC20_abi,
                    pool_fee=self.fee
                )
                await self.second_dex.swap(
                    to_address=PUBLIC_KEY,
                    amount_in=await self.second_dex.web3.to_wei(1, "ether"),
                    amount_out=await self.second_dex.web3.to_wei(0.9, "ether"),
                    token_in=self.asset_address,
                    token_out=self.basic_asset_address,
                    abi_token_in=ERC20_abi,
                    abi_token_out=ERC20_abi,
                    pool_fee=self.fee
                )

            elif first_pool_price > second_pool_price:
                await self.second_dex.swap(
                    to_address=PUBLIC_KEY,
                    amount_in=await self.second_dex.web3.to_wei(1, "ether"),
                    amount_out=await self.second_dex.web3.to_wei(0.9, "ether"),
                    token_in=self.basic_asset_address,
                    token_out=self.asset_address,
                    abi_token_in=ERC20_abi,
                    abi_token_out=ERC20_abi,
                    pool_fee=self.fee
                )
                await self.first_dex.swap(
                    to_address=PUBLIC_KEY,
                    amount_in=await self.first_dex.web3.to_wei(1, "ether"),
                    amount_out=await self.first_dex.web3.to_wei(0.9, "ether"),
                    token_in=self.asset_address,
                    token_out=self.basic_asset_address,
                    abi_token_in=ERC20_abi,
                    abi_token_out=ERC20_abi,
                    pool_fee=self.fee
                )

        except Exeption as e:
            arbitrage_one_chain_bot_logger.error(f"Error accrued- {str(e)}")

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
        arbitrage_one_chain_bot_logger.exeption(f"One chain bot error- {str(e)}")