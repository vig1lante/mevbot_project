from source.dexes.dex_pool import DexPool

class UniSwapV3Pool(DexPool):

    async def fee(self):
        fee = await self.contract.functions.fee().call()
        return fee

    async def liquidity(self):
        liquidity = await self.contract.functions.liquidity().call()
        return liquidity

    async def get_token0_price(self):
        slot0 = await self.contract.functions.slot0().call()
        price = (slot0[0] / 2**96) ** 2
        return price

    async def get_token1_price(self):
        slot0 = await self.contract.functions.slot0().call()
        price = (slot0[0] / 2**96) ** 2
        price = price**-1
        return price