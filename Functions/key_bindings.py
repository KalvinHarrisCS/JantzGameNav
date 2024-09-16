# Functions/key_binding.py

import keyboard
import pyautogui
from ENV.config_manager import ConfigManager
from Functions.ui.ocr import OCRProcessor
from Functions.api_integration import ElevenLabsAPI
import pygame  # Import pygame for audio playback
import threading

class KeyBinder:
    def __init__(self, overlay_event):
        print("Initializing KeyBinder...")
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.bound_key = self.config.get('bound_key')  # Load existing key if available
        self.ocr_processor = OCRProcessor()
        self.api_key = self.config.get('api_key')
        self.eleven_labs_api = ElevenLabsAPI(self.api_key) if self.api_key else None

        # Initialize pygame mixer
        pygame.mixer.init()

        # Initialize a lock to prevent concurrent key presses
        self.lock = threading.Lock()

        # Event to signal when overlay has been used
        self.overlay_event = overlay_event

    def bind_key(self):
        if not self.bound_key:
            print("Please press the key you want to bind.")
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
        with self.lock:
            print("Key pressed! Launching screen overlay for selection...")
            # Signal the main thread to launch the overlay
            self.overlay_event.set()

            # Wait until the overlay has been used
            # This ensures that the overlay has completed its task before proceeding
            while self.overlay_event.is_set():
                # Small sleep to prevent busy waiting
                threading.Event().wait(0.1)

            # After the overlay is closed, proceed with capturing and processing
            screen_area = self.config_manager.load_config().get('screen_area')
            if screen_area:
                # Capture the selected screen area
                try:
                    screenshot = pyautogui.screenshot(
                        region=(
                            screen_area['start_x'],
                            screen_area['start_y'],
                            screen_area['end_x'] - screen_area['start_x'],
                            screen_area['end_y'] - screen_area['start_y']
                        )
                    )
                    image_path = 'captured_area.png'
                    screenshot.save(image_path)
                    print(f"Screen area captured and saved as '{image_path}'.")
                except Exception as e:
                    print(f"An error occurred while capturing the screen area: {e}")
                    return

                # Perform OCR on the captured image
                text = self.ocr_processor.extract_text(image_path)
                # Filter out dashes from the text
                filtered_text = text.replace("-", "")
                if filtered_text.strip():
                    print(f"Extracted Text:\n{filtered_text}")
                    if self.eleven_labs_api:
                        audio_file = self.eleven_labs_api.text_to_speech(filtered_text)
                        if audio_file:
                            print(f"Playing audio file '{audio_file}'...")
                            self.play_audio(audio_file)
                            print("Playback finished.")
                        else:
                            print("Failed to generate audio from text.")
                    else:
                        print("API key not provided. Cannot perform text-to-speech conversion.")
                else:
                    print("No text found in the image.")
            else:
                print("Screen area not defined.")

    def play_audio(self, audio_file):
        try:
            # Stop any currently playing audio
            pygame.mixer.music.stop()

            # Load the audio file
            pygame.mixer.music.load(audio_file)

            # Play the audio file
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Reinitialize the mixer to release the file
            pygame.mixer.quit()
            pygame.mixer.init()
        except Exception as e:
            print(f"An error occurred while playing the audio file: {e}")
