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
        # Determine the appropriate directory to store the config file
        if sys.platform.startswith('win'):
            # Use AppData directory on Windows
            appdata = os.getenv('APPDATA')
            config_dir = os.path.join(appdata, 'MyApp')  # Replace 'MyApp' with your application name
        else:
            # Use home directory on other platforms
            home_dir = os.path.expanduser("~")
            config_dir = os.path.join(home_dir, '.my_app')  # Replace 'my_app' with your application name

        # Create the directory if it doesn't exist
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        # Return the full path to the config file
        return os.path.join(config_dir, self.config_file)

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
