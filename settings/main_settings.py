import tkinter as tk

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, timer_instance):
        super().__init__(parent)
        self.timer_instance = timer_instance
        
        self.title("Timer Settings")
        self.geometry("250x150")
        self.attributes("-topmost", True)
        
        # --- UI Elements ---
        title_label = tk.Label(self, text="Settings", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=10)
        
        button_frame = tk.Frame(self)
        button_frame.pack(pady=15)
        
        # Reset Button
        reset_btn = tk.Button(button_frame, text="Reset Timer", command=self.trigger_reset)
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        # Close Button
        close_btn = tk.Button(button_frame, text="Close App", command=self.trigger_close)
        close_btn.pack(side=tk.LEFT, padx=10)

    def trigger_reset(self):
        """Calls the reset method handled inside main.py"""
        self.timer_instance.reset_timer()

    def trigger_close(self):
        """Destroys the main application root, closing everything."""
        self.timer_instance.root.destroy()