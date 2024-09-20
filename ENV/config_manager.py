# ENV/config_manager.py

import json
import os
import threading
import sys

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.lock = threading.Lock()
        self.config_file = config_file
        self.config_path = self.get_config_path()

    def get_config_path(self):
        if sys.platform.startswith('win'):
            appdata = os.getenv('APPDATA')
            if not appdata:
                print("Error: APPDATA environment variable not found.")
                appdata = os.path.expanduser("~\\AppData\\Roaming")
            config_dir = os.path.join(appdata, 'JantzGameNav')
        else:
            home_dir = os.path.expanduser("~")
            config_dir = os.path.join(home_dir, '.jantz_game_nav')

        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir)
            except Exception as e:
                print(f"Error creating config directory: {e}")
                config_dir = os.getcwd()  # Fallback to current directory

        return os.path.join(config_dir, self.config_file)

    def load_config(self):
        with self.lock:
            try:
                if not os.path.exists(self.config_path) or os.path.getsize(self.config_path) == 0:
                    print("Config file is empty or does not exist. Using default configuration.")
                    return {}
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Config file contains invalid JSON. Using default configuration. Error: {e}")
                return {}
            except Exception as e:
                print(f"Error loading config file: {e}")
                return {}

    def save_config(self, new_config):
        with self.lock:
            try:
                existing_config = self.load_config()
                existing_config.update(new_config)
                with open(self.config_path, 'w') as f:
                    json.dump(existing_config, f, indent=4)
            except Exception as e:
                print(f"Error saving config file: {e}")
