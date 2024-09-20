# Functions/ui/voice_model_manager.py

import tkinter as tk
from tkinter import messagebox
from ENV.config_manager import ConfigManager

class VoiceModelManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.config = self.config_manager.load_config()
        self.voice_models = self.config.get('voice_models', {})
        self.api_key = self.config.get('api_key', "")
        self.openai_api_key = self.config.get('openai_api_key', "")
        self.root = tk.Tk()
        self.root.title("Voice Model Manager")

        # Apply premium UI styling
        self.root.configure(bg="#1E1E1E")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.create_ui()
        self.root.mainloop()

    def create_ui(self):
        # Style configurations
        label_style = {"fg": "white", "bg": "#1E1E1E", "font": ("Arial", 12)}
        entry_style = {"bg": "#2E2E2E", "fg": "white", "font": ("Arial", 12)}
        button_style = {"bg": "#007ACC", "fg": "white", "font": ("Arial", 12), "relief": "flat"}

        # ElevenLabs API Key
        self.api_label = tk.Label(self.root, text="ElevenLabs API Key:", **label_style)
        self.api_label.pack(pady=5)
        self.api_entry = tk.Entry(self.root, width=50, **entry_style)
        self.api_entry.insert(0, self.api_key)
        self.api_entry.pack(pady=5)
        self.save_api_button = tk.Button(self.root, text="Save ElevenLabs API Key", command=self.save_api_key, **button_style)
        self.save_api_button.pack(pady=10)

        # OpenAI API Key
        self.openai_label = tk.Label(self.root, text="OpenAI API Key:", **label_style)
        self.openai_label.pack(pady=5)
        self.openai_entry = tk.Entry(self.root, width=50, **entry_style)
        self.openai_entry.insert(0, self.openai_api_key)
        self.openai_entry.pack(pady=5)
        self.save_openai_button = tk.Button(self.root, text="Save OpenAI API Key", command=self.save_openai_api_key, **button_style)
        self.save_openai_button.pack(pady=10)

        # Voice Models List
        self.label = tk.Label(self.root, text="Voice Models:", **label_style)
        self.label.pack(pady=5)
        self.voice_model_listbox = tk.Listbox(self.root, width=50, height=6, bg="#2E2E2E", fg="white", font=("Arial", 12), relief="flat")
        self.voice_model_listbox.pack(pady=5)
        self.update_listbox()

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.root, bg="#1E1E1E")
        self.buttons_frame.pack(pady=5)

        self.add_button = tk.Button(self.buttons_frame, text="Add", command=self.add_voice_model, **button_style)
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = tk.Button(self.buttons_frame, text="Edit", command=self.edit_voice_model, **button_style)
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(self.buttons_frame, text="Delete", command=self.delete_voice_model, **button_style)
        self.delete_button.grid(row=0, column=2, padx=5)

        # Default Voice Model
        self.default_label = tk.Label(self.root, text="Default Voice Model ID:", **label_style)
        self.default_label.pack(pady=10)
        self.default_entry = tk.Entry(self.root, width=50, **entry_style)
        self.default_entry.insert(0, self.voice_models.get("Default", ""))
        self.default_entry.pack(pady=5)
        self.save_default_button = tk.Button(self.root, text="Save Default Voice Model", command=self.save_default, **button_style)
        self.save_default_button.pack(pady=10)

    def update_listbox(self):
        self.voice_model_listbox.delete(0, tk.END)
        for name, model_id in self.voice_models.items():
            if name != "Default":
                self.voice_model_listbox.insert(tk.END, f"{name}: {model_id}")

    def add_voice_model(self):
        self.open_voice_model_window("Add Voice Model")

    def edit_voice_model(self):
        selected = self.voice_model_listbox.curselection()
        if selected:
            selected_item = self.voice_model_listbox.get(selected)
            name, model_id = selected_item.split(": ")
            self.open_voice_model_window("Edit Voice Model", name, model_id)
        else:
            messagebox.showwarning("No selection", "Please select a voice model to edit.")

    def delete_voice_model(self):
        selected = self.voice_model_listbox.curselection()
        if selected:
            selected_item = self.voice_model_listbox.get(selected)
            name, _ = selected_item.split(": ")
            del self.voice_models[name]
            self.config['voice_models'] = self.voice_models
            self.config_manager.save_config(self.config)
            self.update_listbox()
        else:
            messagebox.showwarning("No selection", "Please select a voice model to delete.")

    def open_voice_model_window(self, title, name="", model_id=""):
        self.voice_model_window = tk.Toplevel(self.root)
        self.voice_model_window.title(title)
        self.voice_model_window.configure(bg="#1E1E1E")
        self.voice_model_window.geometry("400x200")
        self.voice_model_window.resizable(False, False)

        label_style = {"fg": "white", "bg": "#1E1E1E", "font": ("Arial", 12)}
        entry_style = {"bg": "#2E2E2E", "fg": "white", "font": ("Arial", 12)}
        button_style = {"bg": "#007ACC", "fg": "white", "font": ("Arial", 12), "relief": "flat"}

        self.name_label = tk.Label(self.voice_model_window, text="Name:", **label_style)
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.voice_model_window, **entry_style)
        self.name_entry.insert(0, name)
        self.name_entry.pack(pady=5)

        self.model_id_label = tk.Label(self.voice_model_window, text="Voice Model ID:", **label_style)
        self.model_id_label.pack(pady=5)
        self.model_id_entry = tk.Entry(self.voice_model_window, **entry_style)
        self.model_id_entry.insert(0, model_id)
        self.model_id_entry.pack(pady=5)

        self.save_button = tk.Button(self.voice_model_window, text="Save", command=self.save_voice_model, **button_style)
        self.save_button.pack(pady=10)

    def save_voice_model(self):
        name = self.name_entry.get()
        model_id = self.model_id_entry.get()
        if name and model_id:
            self.voice_models[name] = model_id
            self.config['voice_models'] = self.voice_models
            self.config_manager.save_config(self.config)
            self.update_listbox()
            self.voice_model_window.destroy()
        else:
            messagebox.showerror("Error", "Both name and voice model ID are required.")

    def save_default(self):
        default_model_id = self.default_entry.get()
        if default_model_id:
            self.voice_models["Default"] = default_model_id
            self.config['voice_models'] = self.voice_models
            self.config_manager.save_config(self.config)
            messagebox.showinfo("Success", "Default voice model saved.")
        else:
            messagebox.showerror("Error", "Default voice model ID cannot be empty.")

    def save_api_key(self):
        api_key = self.api_entry.get()
        if api_key:
            self.api_key = api_key
            self.config['api_key'] = self.api_key
            self.config_manager.save_config(self.config)
            messagebox.showinfo("Success", "ElevenLabs API key saved.")
        else:
            messagebox.showerror("Error", "API key cannot be empty.")

    def save_openai_api_key(self):
        openai_api_key = self.openai_entry.get()
        if openai_api_key:
            self.openai_api_key = openai_api_key
            self.config['openai_api_key'] = self.openai_api_key
            self.config_manager.save_config(self.config)
            messagebox.showinfo("Success", "OpenAI API key saved.")
        else:
            messagebox.showerror("Error", "OpenAI API key cannot be empty.")
