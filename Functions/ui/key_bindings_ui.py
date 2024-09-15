# Functions/key_binding.py

import keyboard
import pyautogui
from ENV.config_manager import ConfigManager

class KeyBinder:
    def __init__(self):
        self.bound_key = None
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()

    def bind_key(self):
        print("Please use the key you want to bind.")
        self.bound_key = keyboard.read_key()
        print(f"'{self.bound_key}' key is bound.")
        # Save the bound key to config
        self.config_manager.save_config({'bound_key': self.bound_key})

    def start_listening(self):
        keyboard.add_hotkey(self.bound_key, self.on_key_press)
        print(f"Listening for {self.bound_key} key presses...")
        keyboard.wait()  # Keeps the listener running

    def on_key_press(self):
        print("Capturing the defined screen area...")
        self.capture_screen_area()

    def capture_screen_area(self):
        screen_area = self.config_manager.load_config().get('screen_area')
        if screen_area:
            start_x = screen_area['start_x']
            start_y = screen_area['start_y']
            width = screen_area['end_x'] - start_x
            height = screen_area['end_y'] - start_y

            # Ensure width and height are positive
            if width < 0 or height < 0:
                print("Invalid screen area dimensions.")
                return

            screenshot = pyautogui.screenshot(region=(start_x, start_y, width, height))
            screenshot.save('captured_area.png')
            print("Screen area captured and saved as 'captured_area.png'.")
        else:
            print("Screen area not defined.")
