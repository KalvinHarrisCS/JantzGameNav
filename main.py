# main.py

from Functions.key_bindings import KeyBinder
from Functions.ui.persistent_overlay import ScreenOverlay
from Functions.ui.voice_model_manager import VoiceModelManager
import threading
import time

def launch_overlay(overlay_event):
    while True:
        # Wait for the event to be set by the key binder
        overlay_event.wait()
        # Launch the overlay
        overlay = ScreenOverlay()
        overlay.run_overlay()
        # After overlay is closed, clear the event
        overlay_event.clear()

def start_key_binder(overlay_event, voice_models):
    # Initialize and start the key binder
    key_binder = KeyBinder(overlay_event, voice_models)
    key_binder.bind_key()
    key_binder.start_listening()

def main():
    # Create an event for signaling
    overlay_event = threading.Event()

    # Initialize the voice model manager
    voice_models = {
        "Abelard": "model_id_1",   # Example voice models
        "John": "model_id_2",
        "Default": "base_model_id"
    }
    api_key = ""  # Placeholder for ElevenLabs API key

    # Start the overlay listener on a separate thread
    overlay_thread = threading.Thread(target=launch_overlay, args=(overlay_event,), daemon=True)
    overlay_thread.start()

    # Start the key binder in a separate thread and pass voice_models
    key_binder_thread = threading.Thread(target=start_key_binder, args=(overlay_event, voice_models), daemon=True)
    key_binder_thread.start()

    # Run the voice model manager UI in the main thread
    VoiceModelManager(voice_models, api_key)

    print("KeyBinder is running. Press the bound key to capture screen area.")

if __name__ == '__main__':
    main()
