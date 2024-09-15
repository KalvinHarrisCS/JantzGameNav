# Functions/ui/persistent_overlay.py

import tkinter as tk
from ENV.config_manager import ConfigManager

class PersistentOverlay:
    def __init__(self):
        print("Initializing PersistentOverlay...")
        self.root = tk.Tk()

        # Uncomment transparency settings when ready
        # self.root.attributes('-transparentcolor', 'grey')
        # self.root.overrideredirect(True)
        self.root.title("Persistent Overlay")
        self.root.attributes('-topmost', True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.config(bg='grey')  # 'grey' background for visibility during testing

        self.canvas = tk.Canvas(self.root, bg='grey', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.config_manager = ConfigManager()
        self.rect = None  # No initial rectangle

        # Event bindings
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Variables to store the starting position
        self.start_x = None
        self.start_y = None

    def on_button_press(self, event):
        # Save the starting point
        self.start_x = event.x
        self.start_y = event.y

        # Create a new rectangle
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_button_drag(self, event):
        # Update the rectangle as the mouse is dragged
        curX, curY = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        # Final coordinates of the rectangle
        end_x = event.x
        end_y = event.y

        # Ensure coordinates are positive and start_x/y <= end_x/y
        self.start_x, self.end_x = sorted([self.start_x, end_x])
        self.start_y, self.end_y = sorted([self.start_y, end_y])

        # Check for minimum size
        min_size = 10
        if abs(self.end_x - self.start_x) < min_size or abs(self.end_y - self.start_y) < min_size:
            print("Rectangle is too small. Please draw a larger rectangle.")
            self.canvas.delete(self.rect)
            self.rect = None
            return

        # Save the rectangle coordinates
        self.save_coords()
        print("Screen area saved successfully.")

    def save_coords(self):
        config_data = {
            'screen_area': {
                'start_x': int(self.start_x),
                'start_y': int(self.start_y),
                'end_x': int(self.end_x),
                'end_y': int(self.end_y)
            }
        }
        self.config_manager.save_config(config_data)

    def run(self):
        print("Running PersistentOverlay...")
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(10, lambda: self.root.focus_force())
        self.root.mainloop()
