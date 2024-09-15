# main.py

from Functions.key_bindings import KeyBinder
from Functions.ui.persistent_overlay import PersistentOverlay
import threading

def start_key_binder():
    key_binder = KeyBinder()
    key_binder.bind_key()
    key_binder.start_listening()

def main():
    print("Starting the Persistent Overlay...")
    overlay = PersistentOverlay()

    print("Initializing KeyBinder in a separate thread...")
    key_binder_thread = threading.Thread(target=start_key_binder)
    key_binder_thread.daemon = True
    key_binder_thread.start()

    print("Running the Persistent Overlay mainloop...")
    overlay.run()  # Run the Tkinter mainloop in the main thread

if __name__ == '__main__':
    main()
