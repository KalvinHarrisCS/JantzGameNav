# main.py

from Functions.key_bindings import KeyBinder
from Functions.ui.persistent_overlay import ScreenOverlay
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

def main():
    # Create an event for signaling
    overlay_event = threading.Event()

    # Start the overlay listener on a separate thread
    overlay_thread = threading.Thread(target=launch_overlay, args=(overlay_event,), daemon=True)
    overlay_thread.start()

    # Initialize and start the key binder in a separate thread
    key_binder = KeyBinder(overlay_event)
    key_binder.bind_key()
    key_binder_thread = threading.Thread(target=key_binder.start_listening, daemon=True)
    key_binder_thread.start()

    print("KeyBinder is running. Press the bound key to capture screen area.")

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\nExiting application.")

if __name__ == '__main__':
    main()
