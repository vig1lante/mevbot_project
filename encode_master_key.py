from cryptography.fernet import Fernet
from service_settings import (
    FERNET_CRYPT_KEY,
    PRIVATE_KEY,
)

################################

if not PRIVATE_KEY.startswith("0x"):
    PRIVATE_KEY = "0x" + PRIVATE_KEY

an_integer = int(PRIVATE_KEY, 16)
hex_value = hex(an_integer)

################################
encrypter = Fernet(FERNET_CRYPT_KEY)
encrypted_key = encrypter.encrypt(bytes(hex_value, encoding="utf-8"))
encrypted_key = encrypted_key.decode(encoding="utf-8")
print(f"Your encrypted private key -> \n{encrypted_key}")
################################
print("Проверка на расшифрование ключа:")
decrypter = Fernet(FERNET_CRYPT_KEY)
private_key = decrypter.decrypt(bytes(encrypted_key, encoding="utf-8")).decode(
        encoding="utf-8")

if private_key == PRIVATE_KEY:
    print("Проверка прошла успешно")
else:
    print("Ключ зашифровался или расшифровался неверно")