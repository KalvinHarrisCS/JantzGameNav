# ENV/config_manager.py

import json
import os
import threading

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_path = os.path.join(os.path.dirname(__file__), config_file)
        self.lock = threading.Lock()

    def load_config(self):
        with self.lock:
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
        with self.lock:
            with open(self.config_path, 'w') as f:
                json.dump(new_config, f, indent=4)
