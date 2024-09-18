# Functions/ui/voice_model_manager.py

import tkinter as tk
from tkinter import messagebox
from ENV.config_manager import ConfigManager  # Import ConfigManager

class VoiceModelManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.config = self.config_manager.load_config()
        self.voice_models = self.config.get('voice_models', {})
        self.api_key = self.config.get('api_key', "")
        self.root = tk.Tk()
        self.root.title("Voice Model Manager")

        # Set minimalistic style with colors
        self.root.configure(bg="#2E2E2E")  # Dark gray background

        # Create the UI components
        self.create_ui()

        # Start the Tkinter mainloop
        self.root.mainloop()

    def create_ui(self):
        # Label for the API key
        self.api_label = tk.Label(self.root, text="ElevenLabs API Key:", fg="white", bg="#2E2E2E")
        self.api_label.pack(pady=5)

        # Entry for the API key
        self.api_entry = tk.Entry(self.root, width=50)
        self.api_entry.insert(0, self.api_key)
        self.api_entry.pack(pady=5)

        # Save API key button
        self.save_api_button = tk.Button(self.root, text="Save API Key", command=self.save_api_key, bg="#1ABC9C", fg="white", relief="flat")
        self.save_api_button.pack(pady=10)

        # Separator
        self.separator = tk.Frame(self.root, height=2, bd=1, relief="sunken", bg="white")
        self.separator.pack(fill="x", padx=5, pady=10)

        # Label for the voice model list
        self.label = tk.Label(self.root, text="Voice Models:", fg="white", bg="#2E2E2E")
        self.label.pack(pady=5)

        # Listbox to display the voice models
        self.voice_model_listbox = tk.Listbox(self.root, width=50, height=6, bg="#333333", fg="white", relief="flat")
        self.voice_model_listbox.pack(pady=5)

        # Populate the listbox with the voice models
        self.update_listbox()

        # Add button
        self.add_button = tk.Button(self.root, text="Add Voice Model", command=self.add_voice_model, bg="#3498DB", fg="white", relief="flat")
        self.add_button.pack(pady=5)

        # Edit button
        self.edit_button = tk.Button(self.root, text="Edit Voice Model", command=self.edit_voice_model, bg="#E67E22", fg="white", relief="flat")
        self.edit_button.pack(pady=5)

        # Delete button
        self.delete_button = tk.Button(self.root, text="Delete Voice Model", command=self.delete_voice_model, bg="#E74C3C", fg="white", relief="flat")
        self.delete_button.pack(pady=5)

        # Default model label
        self.default_label = tk.Label(self.root, text="Default Voice Model:", fg="white", bg="#2E2E2E")
        self.default_label.pack(pady=10)

        # Entry for default voice model
        self.default_entry = tk.Entry(self.root, width=50)
        self.default_entry.insert(0, self.voice_models.get("Default", ""))
        self.default_entry.pack(pady=5)

        # Save default button
        self.save_default_button = tk.Button(self.root, text="Save Default Voice Model", command=self.save_default, bg="#1ABC9C", fg="white", relief="flat")
        self.save_default_button.pack(pady=10)

    def update_listbox(self):
        # Clear the listbox and repopulate it with the voice models
        self.voice_model_listbox.delete(0, tk.END)
        for name, model_id in self.voice_models.items():
            if name != "Default":  # Don't show the default model in the listbox
                self.voice_model_listbox.insert(tk.END, f"{name}: {model_id}")

    def add_voice_model(self):
        # Open a new window to add a voice model
        self.open_voice_model_window("Add Voice Model")

    def edit_voice_model(self):
        # Open a new window to edit the selected voice model
        selected = self.voice_model_listbox.curselection()
        if selected:
            selected_item = self.voice_model_listbox.get(selected)
            name, model_id = selected_item.split(": ")
            self.open_voice_model_window("Edit Voice Model", name, model_id)
        else:
            messagebox.showwarning("No selection", "Please select a voice model to edit.")

    def delete_voice_model(self):
        # Delete the selected voice model
        selected = self.voice_model_listbox.curselection()
        if selected:
            selected_item = self.voice_model_listbox.get(selected)
            name, _ = selected_item.split(": ")
            del self.voice_models[name]
            # Save updated voice models to config
            self.config['voice_models'] = self.voice_models
            self.config_manager.save_config(self.config)
            self.update_listbox()
        else:
            messagebox.showwarning("No selection", "Please select a voice model to delete.")

    def open_voice_model_window(self, title, name="", model_id=""):
        # Create a new window for adding or editing voice models
        self.voice_model_window = tk.Toplevel(self.root)
        self.voice_model_window.title(title)
        self.voice_model_window.configure(bg="#2E2E2E")

        # Name label and entry
        self.name_label = tk.Label(self.voice_model_window, text="Name:", fg="white", bg="#2E2E2E")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.voice_model_window)
        self.name_entry.insert(0, name)
        self.name_entry.pack(pady=5)

        # Model ID label and entry
        self.model_id_label = tk.Label(self.voice_model_window, text="Voice Model ID:", fg="white", bg="#2E2E2E")
        self.model_id_label.pack(pady=5)
        self.model_id_entry = tk.Entry(self.voice_model_window)
        self.model_id_entry.insert(0, model_id)
        self.model_id_entry.pack(pady=5)

        # Save button
        self.save_button = tk.Button(self.voice_model_window, text="Save", command=self.save_voice_model, bg="#1ABC9C", fg="white", relief="flat")
        self.save_button.pack(pady=10)

    def save_voice_model(self):
        # Save the new or edited voice model
        name = self.name_entry.get()
        model_id = self.model_id_entry.get()
        if name and model_id:
            self.voice_models[name] = model_id
            # Save to config
            self.config['voice_models'] = self.voice_models
            self.config_manager.save_config(self.config)
            self.update_listbox()
            self.voice_model_window.destroy()
        else:
            messagebox.showerror("Error", "Both name and voice model ID are required.")

    def save_default(self):
        # Save the default voice model
        default_model_id = self.default_entry.get()
        if default_model_id:
            self.voice_models["Default"] = default_model_id
            # Save to config
            self.config['voice_models'] = self.voice_models
            self.config_manager.save_config(self.config)
            messagebox.showinfo("Success", "Default voice model saved.")
        else:
            messagebox.showerror("Error", "Default voice model ID cannot be empty.")

    def save_api_key(self):
        # Save the API key from the entry field
        api_key = self.api_entry.get()
        if api_key:
            self.api_key = api_key
            # Save to config
            self.config['api_key'] = self.api_key
            self.config_manager.save_config(self.config)
            messagebox.showinfo("Success", "API key saved.")
        else:
            messagebox.showerror("Error", "API key cannot be empty.")
