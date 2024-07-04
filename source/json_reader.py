import json
from typing import Any, Dict, Union, Optional


class JsonReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._raw_data: Optional[Dict[str, Any]] = None
        self._load_data()

    def _load_data(self) -> None:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self._raw_data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
            print(f"Error reading JSON from {self.file_path}: {e}")
            self._raw_data = None

    def read_from_file(self) -> Optional[Union[Dict[str, Any], list]]:
        return self._raw_data

    @property
    def bot_settings(self) -> Optional[Dict[str, Any]]:
        return self._raw_data.get("bot_settings")

    @property
    def net1(self) -> Optional[Any]:
        return self.bot_settings.get("net1")

    @property
    def net2(self) -> Optional[Any]:
        return self.bot_settings.get("net2")

    @property
    def pairs(self) -> Optional[dict]:

        return self.bot_settings.get("pairs")
