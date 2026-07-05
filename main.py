import tkinter as tk

class ResizableTimer:
    def __init__(self, duration_seconds):
        self.root = tk.Tk()
        self.root.title("Resizable Timer Base")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        self.width = 250
        self.height = 100
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"{self.width}x{self.height}+{screen_width - self.width - 50}+50")
        
        self.bg_color = "#2e2e2e"
        self.text_color = "#ffffff"
        self.root.configure(bg=self.bg_color)
        
        self.remaining_time = duration_seconds
        
        self.label = tk.Label(
            self.root, 
            text="", 
            font=("Helvetica", 24, "bold"), 
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        # --- Interactivity Bindings ---
        self.label.bind("<Motion>", self.check_cursor_zone)
        self.label.bind("<Button-1>", self.start_drag_or_resize)
        self.label.bind("<B1-Motion>", self.do_drag_or_resize)
        
        # Close (Right Click)
        self.root.bind("<Button-3>", lambda e: self.root.destroy())
        
        self.root.bind("<Configure>", self.resize_text)
        self.resize_margin = 15
        self.is_resizing = False
        
        self.update_timer()

    def check_cursor_zone(self, event):
        """ Checks if the mouse is in the resize zone and changes the cursor icon """
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        if event.x >= window_width - self.resize_margin and \
           event.y >= window_height - self.resize_margin:
            self.label.config(cursor="size_nw_se")
        else:
            self.label.config(cursor="arrow")

    def start_drag_or_resize(self, event):
        if event.x >= self.root.winfo_width() - self.resize_margin and \
           event.y >= self.root.winfo_height() - self.resize_margin:
            self.is_resizing = True
        else:
            self.is_resizing = False
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def do_drag_or_resize(self, event):
        if self.is_resizing:
            new_width = max(150, event.x_root - self.root.winfo_x())
            new_height = max(60, event.y_root - self.root.winfo_y())
            self.root.geometry(f"{new_width}x{new_height}")
        else:
            deltax = event.x - self.drag_start_x
            deltay = event.y - self.drag_start_y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")

    def resize_text(self, event):
        if event.widget == self.root:
            new_font_size = max(12, int(event.height * 0.45))
            self.label.config(font=("Helvetica", new_font_size, "bold"))

    def update_timer(self):
        if self.remaining_time >= 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.label.config(text="Time's Up!", fg="#ff5555")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    timer = ResizableTimer(300)
    timer.run()