import os
from pathlib import Path


def get_abi(net, abi_name):
    project_dir = Path(__file__).resolve().parent
    return os.path.join(project_dir, "abis", net, abi_name)
