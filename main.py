# main.py

import threading
import queue
import sys
import tkinter as tk
from Functions.key_bindings import KeyBinder
from ENV.config_manager import ConfigManager
from Functions.ui.settings_manager import SettingsManager
from Functions.ui.persistent_overlay import ScreenOverlay
from Functions.ui.question_overlay import QuestionOverlay

class MainApplication:
    def __init__(self, config_manager, key_binder, command_queue):
        self.config_manager = config_manager
        self.key_binder = key_binder
        self.command_queue = command_queue

        self.root = tk.Tk()
        self.root.title("JantzGameNav")
        self.root.configure(bg="#1E1E1E")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Exception handler for Tkinter
        def tk_exception_handler(exc_type, exc_value, exc_traceback):
            import traceback
            traceback_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print(f"Tkinter exception: {traceback_details}")
            tk.messagebox.showerror("Error", f"An unexpected error occurred:\n\n{traceback_details}")

        self.root.report_callback_exception = tk_exception_handler

        # Initialize SettingsManager with the main root window
        self.settings_manager = SettingsManager(self.root, config_manager, key_binder)

        # Start processing commands
        self.root.after(100, self.process_commands)

    def process_commands(self):
        try:
            while not self.command_queue.empty():
                command, args = self.command_queue.get_nowait()
                if command == 'start_overlay':
                    self.run_overlay()
                elif command == 'process_snip':
                    self.key_binder.process_snip(**args)
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Exception in process_commands: {e}")
        self.root.after(100, self.process_commands)

    def run_overlay(self):
        try:
            overlay = ScreenOverlay(self.root, self.config_manager)
            self.root.wait_window(overlay.top_level)
            # After overlay is closed, signal to process snip
            self.command_queue.put(('process_snip', self.key_binder.snip_args))
        except Exception as e:
            print(f"Exception in run_overlay: {e}")

    def run(self):
        self.root.mainloop()

def main():
    command_queue = queue.Queue()
    config_manager = ConfigManager()
    config = config_manager.load_config()

    # Initialize KeyBinder with the command queue
    key_binder = KeyBinder(command_queue, config_manager)

    # Start the key binder thread
    key_binder_thread = threading.Thread(target=key_binder.start_listening, daemon=True)
    key_binder_thread.start()

    # Initialize and run the main application
    app = MainApplication(config_manager, key_binder, command_queue)
    app.run()

    # After the GUI is closed, exit the program
    print("Application has been closed.")
    sys.exit()

if __name__ == '__main__':
    main()
