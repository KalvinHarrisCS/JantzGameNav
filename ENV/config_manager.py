# ENV/config_manager.py

import json
import os

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_path = os.path.join(os.path.dirname(__file__), config_file)
        self.config = self.load_config()

    def load_config(self):
        # Check if the file exists and is not empty
        if not os.path.exists(self.config_path) or os.path.getsize(self.config_path) == 0:
            print("Config file is empty or does not exist. Using default configuration.")
            return {}
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Config file contains invalid JSON. Using default configuration.")
            return {}

    def save_config(self, new_config):
        self.config.update(new_config)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
