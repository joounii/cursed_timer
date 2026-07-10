import tkinter as tk
import config

def create_floating_popup(parent, text, color="#ffffff", duration=750):
    """
    Creates a temporary floating label in the parent window 
    that automatically destroys itself after the specified duration.
    """
    popup = tk.Label(
        parent, 
        text=text, 
        font=("Helvetica", 12, "bold"), 
        bg=config.BG_COLOR, 
        fg=color
    )

    popup.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
    
    parent.after(duration, popup.destroy)