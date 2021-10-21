import json
import logging
import os
import sys

from src.utils.singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self):
        self._load_config()

    def _load_config(self):
        try:
            run_mode = os.environ['RUN_MODE']
            with open(self.get_config_path()) as f:
                config = json.load(f)

            config['run_mode'] = run_mode
            self.config = config
        except FileNotFoundError as ex:
            logger = logging.getLogger("reddit-crawler")
            logger.error("Config file not found.")
            sys.exit()

    @staticmethod
    def get_config_path():
        return f'config/config.json'

    def get(self, key):
        if key in self.config:
            return self.config[key]
        else:
            return None
