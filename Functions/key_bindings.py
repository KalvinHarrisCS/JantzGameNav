# Functions/key_binding.py

import keyboard
import pyautogui
from ENV.config_manager import ConfigManager
from Functions.ui.ocr import OCRProcessor
from Functions.api_integration import ElevenLabsAPI
from playsound import playsound  # For playing the audio file

class KeyBinder:
    def __init__(self):
        print("Initializing KeyBinder...")
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.bound_key = self.config.get('bound_key')  # Load existing key if available
        self.ocr_processor = OCRProcessor()
        self.api_key = self.config.get('api_key')
        self.eleven_labs_api = ElevenLabsAPI(self.api_key) if self.api_key else None

    def bind_key(self):
        if not self.bound_key:
            print("Please use the key you want to bind.")
            self.bound_key = keyboard.read_key()
            print(f"'{self.bound_key}' key is bound.")
            # Save the bound key to config
            self.config_manager.save_config({'bound_key': self.bound_key})
        else:
            print(f"Using previously bound key: '{self.bound_key}'")

    def start_listening(self):
        if not self.bound_key:
            print("No key bound. Please bind a key first.")
            return
        keyboard.add_hotkey(self.bound_key, self.on_key_press)
        print(f"Listening for '{self.bound_key}' key presses...")
        keyboard.wait()  # Keeps the listener running

    def on_key_press(self):
        print("Capturing the defined screen area...")
        image_path = self.capture_screen_area()
        if image_path:
            text = self.ocr_processor.extract_text(image_path)
            if text.strip():
                print(f"Extracted Text:\n{text}")
                if self.eleven_labs_api:
                    audio_file = self.eleven_labs_api.text_to_speech(text)
                    if audio_file:
                        print(f"Playing audio file '{audio_file}'...")
                        playsound(audio_file)
                        print("Playback finished.")
                    else:
                        print("Failed to generate audio from text.")
                else:
                    print("API key not provided. Cannot perform text-to-speech conversion.")
            else:
                print("No text found in the image.")
        else:
            print("Failed to capture the screen area.")

    def capture_screen_area(self):
        screen_area = self.config_manager.load_config().get('screen_area')
        if screen_area:
            start_x = int(screen_area['start_x'])
            start_y = int(screen_area['start_y'])
            end_x = int(screen_area['end_x'])
            end_y = int(screen_area['end_y'])
            width = end_x - start_x
            height = end_y - start_y

            # Ensure width and height are positive
            if width <= 0 or height <= 0:
                print("Invalid screen area dimensions. Please adjust the overlay rectangle.")
                return None

            try:
                screenshot = pyautogui.screenshot(region=(start_x, start_y, width, height))
                image_path = 'captured_area.png'
                screenshot.save(image_path)
                print(f"Screen area captured and saved as '{image_path}'.")
                return image_path
            except Exception as e:
                print(f"An error occurred while capturing the screen area: {e}")
                return None
        else:
            print("Screen area not defined.")
            return None
