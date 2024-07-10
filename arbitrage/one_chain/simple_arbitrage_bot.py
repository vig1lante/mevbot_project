import asyncio
from source.logger import arbitrage_one_chain_bot_logger
from source.dexes import pancakeswap, quickswap, uniswapV2

#todo константы

def get_pool_settings():

    network, asset, dexes_list, basic_asset = magick_get_settings()

    if basic_asset == None:
        basic_asset = const.USDT_ADRESS

    return network, asset, dexes_list, basic_asset

def initialize_dex(network: str, dex_name: str) -> DexClass:
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

def create_pool(asset_address: str, basic_asset_address: str, dex: DexClass, fee: int) -> DexPool:
    await dex.get_pool(
        first_address=asset_address,
        second_address=basic_asset_address,
        fee=fee
    )
    return pool

def main():
    try:
        #todo что передается адрес токена или его имя
        network, asset, dexes_list, basic_asset = get_pool_settings()

        #todo реализовать получение pair
        pair = config.pairs.get(BSC.PAIR)
        fee = int(pair.get("fee"))

        first_dex =None

        for dex_name in dexes_list:
            if first_dex == None:
                first_dex = initialize_dex(network, dex_name)
                first_pool = create_pool(asset_address, basic_asset_address, first_dex, fee)
            else:
                second_dex = initialize_dex(network, dex_name)
                second_pool = create_pool(asset_address, basic_asset_address, second_dex, fee)

        while True:
            try:
                first_pool_price = await first_pool.get_token0_price()
                second_pool_price = await second_pool.get_token0_price()

                if first_pool_price == second_pool_price:
                    continue

                elif first_pool_price < second_pool_price:
                    await first_dex.swap(
                        to_address=PUBLIC_KEY,
                        amount_in=await first_dex.web3.to_wei(1, "ether"),
                        amount_out=await first_dex.web3.to_wei(0.9, "ether"),
                        token_in=basic_asset_addres,
                        token_out=asset_addres,
                        abi_token_in=ERC20_abi,
                        abi_token_out=ERC20_abi,
                        pool_fee=fee
                    )
                    await second_dex.swap(
                        to_address=PUBLIC_KEY,
                        amount_in=await second_dex.web3.to_wei(1, "ether"),
                        amount_out=await second_dex.web3.to_wei(0.9, "ether"),
                        token_in=asset_addres,
                        token_out=basic_asset_addres,
                        abi_token_in=ERC20_abi,
                        abi_token_out=ERC20_abi,
                        pool_fee=fee
                    )

                elif first_pool_price > second_pool_price:
                    await second_dex.swap(
                        to_address=PUBLIC_KEY,
                        amount_in=await second_dex.web3.to_wei(1, "ether"),
                        amount_out=await second_dex.web3.to_wei(0.9, "ether"),
                        token_in=basic_asset_addres,
                        token_out=asset_addres,
                        abi_token_in=ERC20_abi,
                        abi_token_out=ERC20_abi,
                        pool_fee=fee
                    )
                    await first_dex.swap(
                        to_address=PUBLIC_KEY,
                        amount_in=await first_dex.web3.to_wei(1, "ether"),
                        amount_out=await first_dex.web3.to_wei(0.9, "ether"),
                        token_in=asset_addres,
                        token_out=basic_asset_addres,
                        abi_token_in=ERC20_abi,
                        abi_token_out=ERC20_abi,
                        pool_fee=fee
                    )

            except Exeption as e:
                arbitrage_one_chain_bot_logger.error(f"Error accrued- {str(e)}")

    except Exeption as e:
        arbitrage_one_chain_bot_logger.exeption(f"One chain bot error- {str(e)}")