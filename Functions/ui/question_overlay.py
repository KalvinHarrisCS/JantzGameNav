# Functions/ui/question_overlay.py

import tkinter as tk
from tkinter import messagebox
from ENV.config_manager import ConfigManager
from Functions.api_integration import ElevenLabsAPI, OpenAIAPI
import pygame

class QuestionOverlay:
    def __init__(self, root, config_manager):
        self.root = root
        self.config_manager = config_manager
        self.config = self.config_manager.load_config()
        self.openai_api_key = self.config.get('openai_api_key')
        self.api_key = self.config.get('api_key')
        self.snipped_text = self.config.get('snipped_text', "")
        self.openai_api = OpenAIAPI(self.openai_api_key) if self.openai_api_key else None
        self.eleven_labs_api = ElevenLabsAPI(self.api_key) if self.api_key else None

        self.top_level = tk.Toplevel(self.root)
        self.top_level.title("Ask a Question")
        self.top_level.attributes('-topmost', True)
        self.top_level.geometry("400x200")
        self.top_level.configure(bg="#1E1E1E")
        self.top_level.resizable(False, False)

        self.create_ui()

    def create_ui(self):
        try:
            entry_style = {"bg": "#2E2E2E", "fg": "white", "font": ("Arial", 12)}
            button_style = {"bg": "#007ACC", "fg": "white", "font": ("Arial", 12), "relief": "flat"}

            self.question_entry = tk.Entry(self.top_level, width=50, **entry_style)
            self.question_entry.pack(pady=10)

            self.ask_button = tk.Button(self.top_level, text="Ask", command=self.ask_question, **button_style)
            self.ask_button.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating Question Overlay UI: {e}")
            print(f"Exception in create_ui: {e}")

    def ask_question(self):
        try:
            question = self.question_entry.get()
            if question:
                if self.openai_api:
                    answer = self.openai_api.answer_question(self.snipped_text, question)
                    if answer:
                        print(f"Answer:\n{answer}")

                        if self.eleven_labs_api:
                            audio_file = self.eleven_labs_api.text_to_speech(answer)
                            if audio_file:
                                self.play_audio(audio_file)
                            else:
                                print("Failed to generate audio from answer.")
                        else:
                            print("ElevenLabs API key not provided. Cannot perform text-to-speech conversion.")
                    else:
                        print("Failed to get answer from OpenAI.")
                else:
                    print("OpenAI API key not provided. Cannot get answer.")
                self.top_level.destroy()
            else:
                messagebox.showwarning("Input Error", "Please enter a question.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while asking the question: {e}")
            print(f"Exception in ask_question: {e}")

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
