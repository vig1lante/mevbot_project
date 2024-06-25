import logging
import os.path
from datetime import datetime
from colorlog import ColoredFormatter
from .constants import service_settings
from datetime import datetime


class TracebackInfoFilter(logging.Filter):
    def __init__(self, show_traceback=True):
        super().__init__()
        self.show_traceback = show_traceback

    def filter(self, record):
        if not self.show_traceback:
            record.exc_info = None
            record.exc_text = None
        return True


class Logger:
    console_format = ColoredFormatter(
        '%(log_color)s%(levelname)s%(reset)s - %(message_log_color)s%(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={
            'message': {
                'ERROR': 'red'
            }
        }
    )

    def __init__(self, name, path, production_mode=False):
        self._name = name
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(logging.DEBUG)

        if production_mode:
            self._traceback_filter = TracebackInfoFilter(show_traceback=False)
            console_handler.addFilter(self._traceback_filter)
            file_handler.addFilter(self._traceback_filter)
            console_handler.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
            self._logger.setLevel(logging.INFO)

        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(self.console_format)
        file_handler.setFormatter(file_format)

        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value


today = datetime.today()
arbitrage_one_chain_bot_logger = Logger("arbitrage_one_chain_bot",
                                        os.path.join(
                                            os.path.dirname(os.path.dirname(__file__)),
                                            "logs",
                                            "arbitrage_one_chain_bot.log"
                                        ),
                                        production_mode=service_settings.PRODUCTION_MODE).logger

arbitrage_some_chains_bot_logger = Logger("arbitrage_some_chains_bot",
                                          os.path.join(
                                              os.path.dirname(os.path.dirname(__file__)),
                                              "logs",
                                              "arbitrage_some_chains_bot.log"
                                          ),
                                          production_mode=service_settings.PRODUCTION_MODE).logger
