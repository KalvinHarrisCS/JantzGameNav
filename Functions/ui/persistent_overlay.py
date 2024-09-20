# Functions/ui/persistent_overlay.py

import tkinter as tk
from ENV.config_manager import ConfigManager

class ScreenOverlay:
    def __init__(self, root, config_manager):
        self.root = root
        self.config_manager = config_manager

        self.top_level = tk.Toplevel(self.root)
        self.top_level.attributes('-fullscreen', True)
        self.top_level.attributes('-alpha', 0.3)
        self.top_level.attributes('-topmost', True)
        self.top_level.configure(bg='black')
        self.canvas = tk.Canvas(self.top_level, cursor="cross", bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.selection = None

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )

    def on_button_drag(self, event):
        try:
            curX, curY = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
            self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
        except Exception as e:
            print(f"Exception in on_button_drag: {e}")

    def on_button_release(self, event):
        try:
            end_x, end_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
            start_x, end_x = sorted([self.start_x, end_x])
            start_y, end_y = sorted([self.start_y, end_y])

            min_size = 10
            if (end_x - start_x) < min_size or (end_y - start_y) < min_size:
                print("Selected area is too small. Please try again.")
                self.canvas.delete(self.rect)
                self.rect = None
                return

            self.selection = {
                'start_x': int(start_x),
                'start_y': int(start_y),
                'end_x': int(end_x),
                'end_y': int(end_y)
            }

            self.save_selection()
            self.top_level.destroy()
        except Exception as e:
            print(f"Exception in on_button_release: {e}")

    def save_selection(self):
        try:
            self.config_manager.save_config({'screen_area': self.selection})
            print("Screen area saved successfully.")
        except Exception as e:
            print(f"Exception in save_selection: {e}")
