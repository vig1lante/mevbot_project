import os
from pathlib import Path


def get_abi(net, abi_name):
    project_dir = Path(__file__).resolve().parent
    path = os.path.join(project_dir, "abis", net, abi_name)
    if os.path.exists(path):
        with open(file=path, mode="r") as file:
            abi = file.readline()
            return abi
    raise Exception("Abi path not founded")
