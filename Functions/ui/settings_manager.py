# Functions/ui/settings_manager.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ENV.config_manager import ConfigManager
from pynput import keyboard as pkb

class SettingsManager:
    def __init__(self, root, config_manager, key_binder):
        self.root = root
        self.config_manager = config_manager
        self.key_binder = key_binder
        self.config = self.config_manager.load_config()
        self.voice_models = self.config.get('voice_models', {})
        self.api_key = self.config.get('api_key', "")
        self.openai_api_key = self.config.get('openai_api_key', "")
    
        self.create_ui()
    
    def create_ui(self):
        try:
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(expand=True, fill='both')
    
            style = ttk.Style()
            style.theme_use('default')
            style.configure('TNotebook.Tab', background="#2E2E2E", foreground="white", font=('Arial', 12))
            style.configure('TFrame', background="#1E1E1E")
            style.map("TNotebook.Tab", background=[("selected", "#1E1E1E")])
    
            self.snip_to_audio_frame = ttk.Frame(self.notebook)
            self.snip_to_question_frame = ttk.Frame(self.notebook)
            self.rebind_keys_frame = ttk.Frame(self.notebook)
    
            self.notebook.add(self.snip_to_audio_frame, text='Snip to Audio')
            self.notebook.add(self.snip_to_question_frame, text='Snip to Question')
            self.notebook.add(self.rebind_keys_frame, text='Rebind Keys')
    
            self.create_snip_to_audio_ui()
            self.create_snip_to_question_ui()
            self.create_rebind_keys_ui()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the UI: {e}")
            print(f"Exception in create_ui: {e}")
    
    def create_snip_to_audio_ui(self):
        try:
            label_style = {"foreground": "white", "background": "#1E1E1E", "font": ("Arial", 12)}
            entry_style = {"background": "#2E2E2E", "foreground": "white", "font": ("Arial", 12)}
            button_style = {"background": "#007ACC", "foreground": "white", "font": ("Arial", 12), "relief": "flat"}
    
            frame = self.snip_to_audio_frame
    
            # ElevenLabs API Key
            self.api_label = tk.Label(frame, text="ElevenLabs API Key:", **label_style)
            self.api_label.pack(pady=5)
            self.api_entry = tk.Entry(frame, width=50, **entry_style)
            self.api_entry.insert(0, self.api_key)
            self.api_entry.pack(pady=5)
            self.save_api_button = tk.Button(frame, text="Save ElevenLabs API Key", command=self.save_api_key, **button_style)
            self.save_api_button.pack(pady=10)
    
            # Voice Models List
            self.label = tk.Label(frame, text="Voice Models:", **label_style)
            self.label.pack(pady=5)
            self.voice_model_listbox = tk.Listbox(frame, width=50, height=6, bg="#2E2E2E", fg="white", font=("Arial", 12), relief="flat")
            self.voice_model_listbox.pack(pady=5)
            self.update_listbox()
    
            # Buttons Frame
            self.buttons_frame = tk.Frame(frame, bg="#1E1E1E")
            self.buttons_frame.pack(pady=5)
    
            self.add_button = tk.Button(self.buttons_frame, text="Add", command=self.add_voice_model, **button_style)
            self.add_button.grid(row=0, column=0, padx=5)
    
            self.edit_button = tk.Button(self.buttons_frame, text="Edit", command=self.edit_voice_model, **button_style)
            self.edit_button.grid(row=0, column=1, padx=5)
    
            self.delete_button = tk.Button(self.buttons_frame, text="Delete", command=self.delete_voice_model, **button_style)
            self.delete_button.grid(row=0, column=2, padx=5)
    
            # Default Voice Model
            self.default_label = tk.Label(frame, text="Default Voice Model ID:", **label_style)
            self.default_label.pack(pady=10)
            self.default_entry = tk.Entry(frame, width=50, **entry_style)
            self.default_entry.insert(0, self.voice_models.get("Default", ""))
            self.default_entry.pack(pady=5)
            self.save_default_button = tk.Button(frame, text="Save Default Voice Model", command=self.save_default, **button_style)
            self.save_default_button.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating Snip to Audio UI: {e}")
            print(f"Exception in create_snip_to_audio_ui: {e}")
    
    def create_snip_to_question_ui(self):
        try:
            label_style = {"foreground": "white", "background": "#1E1E1E", "font": ("Arial", 12)}
            entry_style = {"background": "#2E2E2E", "foreground": "white", "font": ("Arial", 12)}
            button_style = {"background": "#007ACC", "foreground": "white", "font": ("Arial", 12), "relief": "flat"}
    
            frame = self.snip_to_question_frame
    
            # OpenAI API Key
            self.openai_label = tk.Label(frame, text="OpenAI API Key:", **label_style)
            self.openai_label.pack(pady=5)
            self.openai_entry = tk.Entry(frame, width=50, **entry_style)
            self.openai_entry.insert(0, self.openai_api_key)
            self.openai_entry.pack(pady=5)
            self.save_openai_button = tk.Button(frame, text="Save OpenAI API Key", command=self.save_openai_api_key, **button_style)
            self.save_openai_button.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating Snip to Question UI: {e}")
            print(f"Exception in create_snip_to_question_ui: {e}")
    
    def create_rebind_keys_ui(self):
        try:
            label_style = {"foreground": "white", "background": "#1E1E1E", "font": ("Arial", 12)}
            button_style = {"background": "#007ACC", "foreground": "white", "font": ("Arial", 12), "relief": "flat"}
    
            frame = self.rebind_keys_frame
    
            self.rebind_snip_to_audio_button = tk.Button(frame, text="Rebind SnipToAudio", command=self.rebind_snip_to_audio, **button_style)
            self.rebind_snip_to_audio_button.pack(pady=20)
    
            self.rebind_snip_to_question_button = tk.Button(frame, text="Rebind SnipToQuestion", command=self.rebind_snip_to_question, **button_style)
            self.rebind_snip_to_question_button.pack(pady=20)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating Rebind Keys UI: {e}")
            print(f"Exception in create_rebind_keys_ui: {e}")
    
    def rebind_snip_to_audio(self):
        try:
            messagebox.showinfo("Rebind SnipToAudio", "Please press the key you want to bind for SnipToAudio.")
            new_key = self.wait_for_key_press()
            if new_key:
                self.config['bound_key'] = new_key
                self.config_manager.save_config({'bound_key': new_key})
                messagebox.showinfo("Success", f"SnipToAudio key bound to '{new_key}'.")
                self.key_binder.rebind_snip_to_audio(new_key)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while rebinding SnipToAudio key: {e}")
            print(f"Exception in rebind_snip_to_audio: {e}")
    
    def rebind_snip_to_question(self):
        try:
            messagebox.showinfo("Rebind SnipToQuestion", "Please press the key you want to bind for SnipToQuestion.")
            new_key = self.wait_for_key_press()
            if new_key:
                self.config['question_key'] = new_key
                self.config_manager.save_config({'question_key': new_key})
                messagebox.showinfo("Success", f"SnipToQuestion key bound to '{new_key}'.")
                self.key_binder.rebind_snip_to_question(new_key)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while rebinding SnipToQuestion key: {e}")
            print(f"Exception in rebind_snip_to_question: {e}")
    
    def wait_for_key_press(self):
        key_pressed = []
    
        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char:
                    key_pressed.append(key.char.lower())
                else:
                    key_pressed.append(str(key).split('.')[-1].lower())
                return False  # Stop listener
            except Exception as e:
                print(f"Exception in wait_for_key_press: {e}")
                return False
    
        with pkb.Listener(on_press=on_press) as listener:
            listener.join()
    
        return key_pressed[0] if key_pressed else None
    
    def update_listbox(self):
        try:
            self.voice_model_listbox.delete(0, tk.END)
            for name, model_id in self.voice_models.items():
                if name != "Default":
                    self.voice_model_listbox.insert(tk.END, f"{name}: {model_id}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating the voice model list: {e}")
            print(f"Exception in update_listbox: {e}")
    
    def add_voice_model(self):
        self.open_voice_model_window("Add Voice Model")
    
    def edit_voice_model(self):
        try:
            selected = self.voice_model_listbox.curselection()
            if selected:
                selected_item = self.voice_model_listbox.get(selected)
                name, model_id = selected_item.split(": ")
                self.open_voice_model_window("Edit Voice Model", name, model_id)
            else:
                messagebox.showwarning("No selection", "Please select a voice model to edit.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while editing the voice model: {e}")
            print(f"Exception in edit_voice_model: {e}")
    
    def delete_voice_model(self):
        try:
            selected = self.voice_model_listbox.curselection()
            if selected:
                selected_item = self.voice_model_listbox.get(selected)
                name, _ = selected_item.split(": ")
                del self.voice_models[name]
                self.config['voice_models'] = self.voice_models
                self.config_manager.save_config({'voice_models': self.voice_models})
                self.update_listbox()
            else:
                messagebox.showwarning("No selection", "Please select a voice model to delete.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the voice model: {e}")
            print(f"Exception in delete_voice_model: {e}")
    
    def open_voice_model_window(self, title, name="", model_id=""):
        try:
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
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the voice model window: {e}")
            print(f"Exception in open_voice_model_window: {e}")
    
    def save_voice_model(self):
        try:
            name = self.name_entry.get()
            model_id = self.model_id_entry.get()
            if name and model_id:
                self.voice_models[name] = model_id
                self.config['voice_models'] = self.voice_models
                self.config_manager.save_config({'voice_models': self.voice_models})
                self.update_listbox()
                self.voice_model_window.destroy()
            else:
                messagebox.showerror("Error", "Both name and voice model ID are required.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the voice model: {e}")
            print(f"Exception in save_voice_model: {e}")
    
    def save_default(self):
        try:
            default_model_id = self.default_entry.get()
            if default_model_id:
                self.voice_models["Default"] = default_model_id
                self.config['voice_models'] = self.voice_models
                self.config_manager.save_config({'voice_models': self.voice_models})
                messagebox.showinfo("Success", "Default voice model saved.")
            else:
                messagebox.showerror("Error", "Default voice model ID cannot be empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the default voice model: {e}")
            print(f"Exception in save_default: {e}")
    
    def save_api_key(self):
        try:
            api_key = self.api_entry.get()
            if api_key:
                self.api_key = api_key
                self.config['api_key'] = self.api_key
                self.config_manager.save_config({'api_key': self.api_key})
                messagebox.showinfo("Success", "ElevenLabs API key saved.")
            else:
                messagebox.showerror("Error", "API key cannot be empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the API key: {e}")
            print(f"Exception in save_api_key: {e}")
    
    def save_openai_api_key(self):
        try:
            openai_api_key = self.openai_entry.get()
            if openai_api_key:
                self.openai_api_key = openai_api_key
                self.config['openai_api_key'] = self.openai_api_key
                self.config_manager.save_config({'openai_api_key': self.openai_api_key})
                messagebox.showinfo("Success", "OpenAI API key saved.")
            else:
                messagebox.showerror("Error", "OpenAI API key cannot be empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the OpenAI API key: {e}")
            print(f"Exception in save_openai_api_key: {e}")
