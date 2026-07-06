import tkinter as tk
from tkinter import ttk

# Import our engines
from engines.truly_random import TrulyRandomEngine

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, timer_instance):
        super().__init__(parent)
        self.timer_instance = timer_instance
        
        self.title("Timer Settings")
        self.geometry("250x200")  # Made slightly taller to fit the dropdown
        self.attributes("-topmost", True)
        
        # --- UI Elements ---
        title_label = tk.Label(self, text="Settings", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=10)
        
        # Engine Selection Dropdown
        engine_frame = tk.Frame(self)
        engine_frame.pack(pady=10)
        
        tk.Label(engine_frame, text="Engine:").pack(side=tk.LEFT)
        
        self.engine_var = tk.StringVar()
        self.engine_dropdown = ttk.Combobox(engine_frame, textvariable=self.engine_var, state="readonly", width=15)
        
        # Add new engines to this tuple as you build them
        self.engine_dropdown['values'] = ("Truly Random",) 
        
        # Set the dropdown to match whatever engine is currently active in main.py
        self.engine_dropdown.set(self.timer_instance.engine.name)
        self.engine_dropdown.pack(side=tk.LEFT, padx=5)
        self.engine_dropdown.bind("<<ComboboxSelected>>", self.change_engine)
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=15)
        
        reset_btn = tk.Button(button_frame, text="Reset Timer", command=self.trigger_reset)
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        close_btn = tk.Button(button_frame, text="Close App", command=self.trigger_close)
        close_btn.pack(side=tk.LEFT, padx=10)

    def change_engine(self, event=None):
        """Swaps the active engine in the main timer based on the dropdown."""
        selection = self.engine_var.get()
        
        if selection == "Truly Random":
            self.timer_instance.engine = TrulyRandomEngine()
            
        print(f"[SETTINGS] Engine swapped to: {selection}")

    def trigger_reset(self):
        self.timer_instance.reset_timer()

    def trigger_close(self):
        self.timer_instance.root.destroy()