# Functions/key_bindings.py

import threading
from pynput import keyboard as pkb
import pyautogui
import pygame
import os
from ENV.config_manager import ConfigManager
from Functions.ui.ocr import OCRProcessor
from Functions.api_integration import ElevenLabsAPI, OpenAIAPI

class KeyBinder:
    def __init__(self, command_queue, config_manager):
        print("Initializing KeyBinder...")
        self.command_queue = command_queue
        self.config_manager = config_manager
        self.config = self.config_manager.load_config()
        self.bound_key = self.config.get('bound_key', 'f7')
        self.question_key = self.config.get('question_key', 'f9')
        self.ocr_processor = OCRProcessor()
        self.api_key = self.config.get('api_key')
        self.eleven_labs_api = ElevenLabsAPI(self.api_key) if self.api_key else None

        self.openai_api_key = self.config.get('openai_api_key')
        self.openai_api = OpenAIAPI(self.openai_api_key) if self.openai_api_key else None

        pygame.mixer.init()
        self.lock = threading.Lock()
        self.voice_models = self.config.get('voice_models', {})
        self.snipped_text = ""

        self.snip_args = {}

        # Initialize the listener
        self.listener = pkb.Listener(on_press=self.on_press)
        self.listener.daemon = True
        self.listener.start()

    def start_listening(self):
        print(f"Listening for '{self.bound_key}' and '{self.question_key}' key presses...")
        self.listener.join()  # Keep the thread alive

    def rebind_snip_to_audio(self, new_key):
        self.bound_key = new_key
        self.config['bound_key'] = self.bound_key
        self.config_manager.save_config({'bound_key': self.bound_key})
        print(f"Rebound SnipToAudio to '{self.bound_key}'.")

    def rebind_snip_to_question(self, new_key):
        self.question_key = new_key
        self.config['question_key'] = self.question_key
        self.config_manager.save_config({'question_key': self.question_key})
        print(f"Rebound SnipToQuestion to '{self.question_key}'.")

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char:
                key_char = key.char.lower()
            else:
                key_char = str(key).split('.')[-1].lower()

            if key_char == self.bound_key.lower():
                self.on_snip_key_press()
            elif key_char == self.question_key.lower():
                self.on_summarize_key_press()
        except Exception as e:
            print(f"Exception in on_press: {e}")

    def on_snip_key_press(self):
        with self.lock:
            self.reload_config()
            print("SnipToAudio key pressed! Launching screen overlay for selection...")
            self.snip_args = {'explain': True}
            self.command_queue.put(('start_overlay', None))

    def on_summarize_key_press(self):
        with self.lock:
            self.reload_config()
            print("SnipToQuestion key pressed! Launching screen overlay for selection...")
            self.snip_args = {'summarize': True}
            self.command_queue.put(('start_overlay', None))

    def process_snip(self, explain=False, summarize=False):
        try:
            screen_area = self.config_manager.load_config().get('screen_area')
            if screen_area:
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

                text = self.ocr_processor.extract_text(image_path)
                self.snipped_text = text.replace("-", "").replace("|", "")
                if self.snipped_text.strip():
                    print(f"Extracted Text:\n{self.snipped_text}")
                    if summarize:
                        self.handle_summarization(self.snipped_text)
                    elif explain:
                        self.handle_explanation(self.snipped_text)
                else:
                    print("No text found in the image.")

                if os.path.exists(image_path):
                    os.remove(image_path)
                    print(f"Deleted screenshot '{image_path}'.")
            else:
                print("Screen area not defined.")

        except Exception as e:
            print(f"Exception in process_snip: {e}")

    def handle_explanation(self, text):
        try:
            if self.openai_api:
                explanation = self.openai_api.get_explanation(text)
                if explanation:
                    print(f"Explanation:\n{explanation}")

                    if self.eleven_labs_api:
                        audio_file = self.eleven_labs_api.text_to_speech(explanation)
                        if audio_file:
                            print(f"Playing audio file '{audio_file}'...")
                            self.play_audio(audio_file)
                            print("Playback finished.")
                        else:
                            print("Failed to generate audio from text.")
                    else:
                        print("ElevenLabs API key not provided. Cannot perform text-to-speech conversion.")
                else:
                    print("Failed to get explanation from OpenAI.")
            else:
                print("OpenAI API key not provided. Cannot get explanation.")
        except Exception as e:
            print(f"Exception in handle_explanation: {e}")

    def handle_summarization(self, text):
        try:
            if self.openai_api:
                summary = self.openai_api.summarize_text(text)
                if summary:
                    print(f"Summary:\n{summary}")

                    if self.eleven_labs_api:
                        audio_file = self.eleven_labs_api.text_to_speech(summary)
                        if audio_file:
                            print(f"Playing audio file '{audio_file}'...")
                            self.play_audio(audio_file)
                            print("Playback finished.")
                        else:
                            print("Failed to generate audio from summary.")
                    else:
                        print("ElevenLabs API key not provided. Cannot perform text-to-speech conversion.")
                else:
                    print("Failed to get summary from OpenAI.")
            else:
                print("OpenAI API key not provided. Cannot get summary.")
        except Exception as e:
            print(f"Exception in handle_summarization: {e}")

    def reload_config(self):
        try:
            self.config = self.config_manager.load_config()
            self.api_key = self.config.get('api_key')
            self.eleven_labs_api = ElevenLabsAPI(self.api_key) if self.api_key else None
            self.voice_models = self.config.get('voice_models', {})
            self.openai_api_key = self.config.get('openai_api_key')
            self.openai_api = OpenAIAPI(self.openai_api_key) if self.openai_api_key else None
        except Exception as e:
            print(f"Exception in reload_config: {e}")

    def play_audio(self, audio_file):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.quit()
            pygame.mixer.init()
        except Exception as e:
            print(f"An error occurred while playing the audio file: {e}")
