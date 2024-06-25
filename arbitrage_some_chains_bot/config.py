import os

from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv('.env')

if dotenv_path:
    load_dotenv(dotenv_path)
    print(f".env found: {dotenv_path}")
else:
    print(".env not found using default variables")


SOMETHING = os.getenv("", default=None)
