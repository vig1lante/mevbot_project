import os

from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv('.env')

if dotenv_path:
    load_dotenv(dotenv_path)
    print(f".env found: {dotenv_path}")
else:
    print(".env not found using default variables")


PUBLIC_KEY = os.getenv("PUBLIC_KEY", default=None)

PRIVATE_KEY = os.getenv("PRIVATE_KEY", default=None)

FERNET_CRYPT_KEY = os.getenv("FERNET_CRYPT_KEY", default=None)

PANCAKE_SWAP_V3_R = os.getenv("PANCAKE_SWAP_V3_R", default=None)
PANCAKE_SWAP_V3_F = os.getenv("PANCAKE_SWAP_V3_F", default=None)
