from typing import Any

from source.db_driver import PostgresDriver, ABIs
import enum
import os


class SmartContractName(enum.Enum):
    PancakeSwapFactory = "pancake_swap_v3_factory"
    PancakeSwapRouter = "pancake_swap_v3_router"
    PancakeSwapV3Pool = "pancake_swap_v3_pool"

    UniswapFactory = "uniswap_v3_factory"
    UniswapRouter = "uniswap_v3_router"
    UniswapPool = "uniswap_v3_pool"

    QuickSwapFactory = "quickswap_v3_factory"
    QuickSwapRouter = "quickswap_v3_router"
    QuickSwapPool = "quickswap_v3_pool"

    USDC = "usdc"
    USDT = "usdt"


class Net(enum.Enum):
    BNB = "BNB"
    Polygon = "Polygon"
    PolygonZKEVM = "PolygonZKEVM"
    Ethereum = "Ethereum"
    Avalanche = "Avalanche"
    Tron = "Tron"


class AbiStorage:
    def __init__(self):
        self.db_driver = PostgresDriver()
        self.__initialize_db()

    def __initialize_db(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "abis")
        net_set = set([net.value for net in Net])
        sc_name_set = set([sc_name.value for sc_name in SmartContractName])

        if os.path.exists(path):
            directories = os.listdir(path)

            for directory in directories:
                if directory in net_set:
                    abis = os.listdir(os.path.join(path, directory))

                    for abi in abis:
                        abi_path = os.path.join(path, directory, abi)
                        abi = abi.replace(".abi", "")
                        if os.path.isfile(abi_path) and abi in sc_name_set:
                            abi_str = ""
                            with open(file=abi_path, mode="r") as file:
                                abi_str = file.readline()
                            abi_obj = ABIs(name=abi, net=directory, abi=abi_str)
                            exists_abi = self.db_driver.exists_abi(
                                ABIs.name == abi, ABIs.net == directory
                            )
                            if exists_abi:
                                self.db_driver.update_abi(
                                    abi_str, ABIs.name == abi, ABIs.net == directory
                                )
                            else:
                                self.db_driver.insert_data(abi_obj)
        else:
            raise Exception('Directory "abis" not founded!')

    def get_all_abis(self):
        abis = self.db_driver.get_all_abis()
        abis_map = dict()
        for abi in abis:
            if abi.net not in abis_map:
                abis_map[abi.net] = dict()
            abis_map[abi.net][abi.name] = abi.abi
        return abis_map

    def get_abi(self, net: Net, name: SmartContractName) -> str | None:
        abi = self.db_driver.get_first_abi(ABIs.net == net, ABIs.name == name)
        if abi is None:
            return None
        return abi.abi
