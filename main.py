import tkinter as tk
import random
from events.increasing import add_time
from events.neutral import change_color
from events.decreasing import remove_time

class CursedTimer:
    def __init__(self, duration_seconds):
        self.root = tk.Tk()
        self.root.title("Cursed Resizable Timer")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # Geometry Setup
        self.width = 250
        self.height = 100
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"{self.width}x{self.height}+{screen_width - self.width - 50}+50")
        
        # Default Styles
        self.bg_color = "#2e2e2e"
        self.text_color = "#ffffff"
        self.root.configure(bg=self.bg_color)
        
        self.remaining_time = duration_seconds
        
        # =========================================================================
        # Category Odds
        self.chance_increasing = 33
        self.chance_neutral    = 34
        self.chance_decreasing = 33
        
        # 2. Event Weights
        self.categories = {
            "increasing": {
                add_time: 10,
            },
            "neutral": {
                change_color: 50,
            },
            "decreasing": {
                remove_time: 20,
            }
        }
        # =========================================================================

        # UI Elements
        self.label = tk.Label(
            self.root, 
            text="", 
            font=("Helvetica", 24, "bold"), 
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        # Window Interactivity Bindings
        self.label.bind("<Motion>", self.check_cursor_zone)
        self.label.bind("<Button-1>", self.start_drag_or_resize)
        self.label.bind("<B1-Motion>", self.do_drag_or_resize)
        self.root.bind("<Button-3>", lambda e: self.root.destroy())
        self.root.bind("<Configure>", self.resize_text)
        
        self.resize_margin = 15
        self.is_resizing = False
        
        self.update_timer()

    def check_cursor_zone(self, event):
        if event.x >= self.root.winfo_width() - self.resize_margin and \
           event.y >= self.root.winfo_height() - self.resize_margin:
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
            font_by_height = int(event.height * 0.45)
            
            font_by_width = int((event.width * 0.85) / 3.5)
            
            new_font_size = max(12, min(font_by_height, font_by_width))
            
            self.label.config(font=("Helvetica", new_font_size, "bold"))

    def update_timer(self):
        if hasattr(self, 'timer_id') and self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        if self.remaining_time > 0:
            
            cat_pool = ["increasing", "neutral", "decreasing"]
            cat_weights = [self.chance_increasing, self.chance_neutral, self.chance_decreasing]
            
            chosen_category = random.choices(cat_pool, weights=cat_weights, k=1)[0]
            
            event_dict = self.categories[chosen_category]
            
            skip_countdown = False
            chosen_event_name = "None"
            
            if event_dict:
                event_pool = list(event_dict.keys())
                event_weights = list(event_dict.values())
                
                chosen_event = random.choices(event_pool, weights=event_weights, k=1)[0]
                chosen_event_name = chosen_event.__name__.split('.')[-1]

                skip_countdown = chosen_event.trigger(self)
                
            # skip countdown if the event requested it
            if not skip_countdown:
                self.remaining_time -= 1
            
            # display time
            mins, secs = divmod(self.remaining_time, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")
            
            
            # Debuging output
            default_behavior = not skip_countdown
            true_mins, true_secs = divmod(self.remaining_time, 60)
            formatted_true_time = f"{true_mins:02d}:{true_secs:02d}"
            
            log_msg = (
                f"[TICK] "
                f"Cat: {chosen_category:<11} | "
                f"Event: {chosen_event_name:<15} | "
                f"Default behavior: {str(default_behavior):<5} | "
                f"TRUE TIME: {formatted_true_time} ({self.remaining_time}s)"
            )
            print(log_msg)
                
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.label.config(text="Time's Up!", fg="#ff5555")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    timer = CursedTimer(300)
    timer.run()