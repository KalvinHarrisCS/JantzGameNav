# Functions/ui/persistent_overlay.py

import tkinter as tk
from ENV.config_manager import ConfigManager

class ScreenOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)  # Semi-transparent
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        self.canvas = tk.Canvas(self.root, cursor="cross", bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # To store the selected region
        self.selection = None

    def on_button_press(self, event):
        # Save the starting coordinates
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        # Create a rectangle
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )

    def on_button_drag(self, event):
        # Update the rectangle as the mouse is dragged
        curX, curY = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        # Final coordinates
        end_x, end_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        # Ensure coordinates are sorted
        start_x, end_x = sorted([self.start_x, end_x])
        start_y, end_y = sorted([self.start_y, end_y])

        # Minimum size check
        min_size = 10
        if (end_x - start_x) < min_size or (end_y - start_y) < min_size:
            print("Selected area is too small. Please try again.")
            self.canvas.delete(self.rect)
            self.rect = None
            return

        # Save the selection
        self.selection = {
            'start_x': int(start_x),
            'start_y': int(start_y),
            'end_x': int(end_x),
            'end_y': int(end_y)
        }

        # Save to config
        self.save_selection()

        # Close the overlay
        self.root.destroy()

    def save_selection(self):
        config_data = {
            'screen_area': self.selection
        }
        config_manager = ConfigManager()
        config_manager.save_config(config_data)
        print("Screen area saved successfully.")

    def run_overlay(self):
        self.root.mainloop()
