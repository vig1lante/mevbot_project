from dotenv import load_dotenv
import os
import json


class CONSTANTS:

    def get_list_from_config(self, field, config):
        if field not in config:
            raise Exception(f"{field} not founded in config.json")

        config_value = config[field]
        if config_value is not None and config_value != "" and len(config_value) != 0:
            return config_value
        else:
            raise Exception(f"{field} in config.json equal None or '' or []")

    def get_int_from_config(self, field, config):
        if field not in config:
            raise Exception(f"{field} not founded in config.json")

        config_value = config[field]
        if config_value is not None and isinstance(config_value, int):
            return config_value
        else:
            raise Exception(f"{field} in config.json equal None or not int")

    def get_bool_from_config(self, field, config):
        if field not in config:
            raise Exception(f"{field} not founded in config.json")

        config_value = config[field]
        if config_value is not None and isinstance(config_value, bool):
            return config_value
        else:
            raise Exception(f"{field} in config.json equal None or not int")

    def get_str_from_config(self, field, config):
        if field not in config:
            raise Exception(f"{field} not founded in config.json")

        config_value = config[field]
        if (
            config_value is not None
            and config_value != ""
            and isinstance(config_value, str)
        ):
            return config_value
        else:
            raise Exception(f"{field} in config.json equal None or or '' or not str")

    def get_str_from_env(self, field):
        env_var = os.environ.get(field)
        if env_var is not None and env_var != "":
            return env_var
        else:
            raise Exception(f"{field} in .env equal None or ''")

    def get_int_from_env(self, field):
        env_var = os.environ.get(field)
        if env_var is not None and env_var != "":
            return int(env_var)
        else:
            raise Exception(f"{field} in .env equal None or ''")

    def get_float_from_env(self, field):
        env_var = os.environ.get(field)
        if env_var is not None and env_var != "":
            return float(env_var)
        else:
            raise Exception(f"{field} in .env equal None or ''")

    def get_bool_from_env(self, field):
        env_var = os.environ.get(field)
        if env_var is not None and env_var != "":
            bool_value = env_var.lower()
            if bool_value != "true" and bool_value != "false":
                raise Exception(f"{field} in .env not equal True or False")
            if bool_value == "true":
                return True
            return False
        else:
            raise Exception(f"{field} in .env equal None or ''")


class SERVICE_SETTINGS(CONSTANTS):
    BNB_USDT_CONTRACT_ADDRESS = "0x55d398326f99059fF775485246999027B3197955"
    PRODUCTION_MODE = False
    FERNET_CRYPT_KEY = ""

    def __init__(self, config):
        if config is not None:
            self.BNB_USDT_CONTRACT_ADDRESS = self.get_str_from_config(
                "BNB_USDT_CONTRACT_ADDRESS", config
            )
            self.PRODUCTION_MODE = self.get_bool_from_config("PRODUCTION_MODE", config)

        self.FERNET_CRYPT_KEY = self.get_str_from_env("FERNET_CRYPT_KEY")


dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

with open(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
) as config_file:
    config = json.load(config_file)

service_settings = SERVICE_SETTINGS(config)
