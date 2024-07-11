from source.abi_storage import AbiStorage, Net, SmartContractName

abi_storage = AbiStorage()
print(abi_storage.get_all_abis())
print(abi_storage.get_abi(net=Net.BNB.value, name=SmartContractName.PancakeSwapFactory.value))