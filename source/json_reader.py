import json
from typing import Any, Dict, Union, Optional


class JsonReader:
    def __init__(self, data):
        self._raw_data = data

    @staticmethod
    def read_from_file(self) -> Optional[Union[Dict[str, Any], list]]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data
        except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
            print(f"Error reading JSON: {e}")
            return None

    @property
    def bot_settings(self) -> Optional[dict]:
        return self._raw_data.get("bot_settings")

    @property
    def net1(self):
        return self.bot_settings.get("net1")

    @property
    def pairs(self):
        return self.bot_settings.get("pairs")
