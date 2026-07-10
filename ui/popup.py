# ui/popup.py
import tkinter as tk
import config

def create_floating_popup(parent, text, color="#ffffff", duration=750, font_size=16):
    """
    Creates a borderless floating Toplevel window that automatically 
    tracks the parent's position and scales its font size dynamically.
    """
    popup = tk.Toplevel(parent)
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    
    trans_color = "#000001"
    popup.configure(bg=trans_color)
    
    try:
        popup.attributes("-transparentcolor", trans_color)
    except tk.TclError:
        pass 

    label = tk.Label(
        popup, 
        text=text, 
        font=("Helvetica", font_size, "bold"), 
        bg=trans_color, 
        fg=color
    )
    label.pack()

    popup.update_idletasks()
    
    def track_parent_position():
        if not popup.winfo_exists() or not parent.winfo_exists():
            return
            
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        
        popup_width = popup.winfo_reqwidth()
        popup_height = popup.winfo_reqheight()
        
        pos_x = parent_x + (parent_width // 2) - (popup_width // 2)
        pos_y = parent_y - popup_height - 15 
        
        popup.geometry(f"+{pos_x}+{pos_y}")
        popup.after(16, track_parent_position)

    track_parent_position()
    parent.after(duration, popup.destroy)