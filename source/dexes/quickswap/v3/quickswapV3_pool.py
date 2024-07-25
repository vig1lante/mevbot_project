from source.dexes.dex_pool import DexPool

class QuickSwapV3Pool(DexPool):

    async def fee(self):
        fee = await self.contract.functions.globalState().call()
        return fee[2]

    async def liquidity(self):
        liquidity = await self.contract.functions.liquidity().call()
        return liquidity

    async def get_token0_price(self):
        globalState = await self.contract.functions.globalState().call()
        price = (globalState[0] / 2**96) ** 2
        return price

    async def get_token1_price(self):
        globalState = await self.contract.functions.globalState().call()
        price = (globalState[0] / 2**96) ** 2
        price = price**-1
        return price