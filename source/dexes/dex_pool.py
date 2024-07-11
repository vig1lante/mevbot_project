
class DexPool:
    def __init__(
        self,
        token0_name,
        token1_name,
        token0_address,
        token1_address,
        contract_address,
        contract,
    ):
        self.token0_name = token0_name
        self.token1_name = token1_name
        self.token0_address = token0_address
        self.token1_address = token1_address
        self.contract_address = contract_address
        self.contract = contract

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
