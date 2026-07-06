import tkinter as tk
import random
import config
import tkinter.font as tkfont
from telemetry import TimerTelemetry
from time_utils import format_time
from event_registry import EVENT_CATEGORIES
from settings.main_settings import SettingsWindow
from engines.truly_random import TrulyRandomEngine

class CursedTimer:
    def __init__(self, duration_seconds):
        # UI Window Setup
        self.root = tk.Tk()
        self.root.title("Cursed Resizable Timer")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        self.width, self.height = 250, 100
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"{self.width}x{self.height}+{screen_width - self.width - 50}+50")
        self.root.configure(bg=config.BG_COLOR)
        self.dynamic_font = tkfont.Font(family="Helvetica", size=24, weight="bold")

        self.label = tk.Label(
            self.root, text="", font=self.dynamic_font, 
            bg=config.BG_COLOR, fg=config.TEXT_COLOR
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        self.resize_margin = 15
        self.is_resizing = False
        
        # Keep track of the settings window instance
        self.settings_window = None 

        self.label.bind("<Motion>", self.check_cursor_zone)
        self.label.bind("<Button-1>", self.start_drag_or_resize)
        self.label.bind("<B1-Motion>", self.do_drag_or_resize)

        self.root.bind("<Button-3>", self.open_settings)
        self.root.bind("<Configure>", self.resize_text)

        self.remaining_time = duration_seconds
        self.current_delay = config.DEFAULT_TICK_DELAY_MS
        self.timer_id = None
        self.telemetry = TimerTelemetry(duration_seconds)

        self.engine = globals()[config.DEFAULT_ENGINE]()
        
        self.categories = EVENT_CATEGORIES
        
        self.update_timer()

    # --- Window Manipulation Methods ---
    
    def check_cursor_zone(self, event):
        in_resize_zone = (event.x >= self.root.winfo_width() - self.resize_margin and 
                          event.y >= self.root.winfo_height() - self.resize_margin)
        self.label.config(cursor="size_nw_se" if in_resize_zone else "arrow")

    def start_drag_or_resize(self, event):
        self.is_resizing = (event.x >= self.root.winfo_width() - self.resize_margin and 
                            event.y >= self.root.winfo_height() - self.resize_margin)
        if not self.is_resizing:
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def do_drag_or_resize(self, event):
        if self.is_resizing:
            new_width = max(150, event.x_root - self.root.winfo_x())
            new_height = max(60, event.y_root - self.root.winfo_y())
            self.root.geometry(f"{new_width}x{new_height}")
        else:
            x = self.root.winfo_x() + (event.x - self.drag_start_x)
            y = self.root.winfo_y() + (event.y - self.drag_start_y)
            self.root.geometry(f"+{x}+{y}")

    def resize_text(self, event=None):
        if event and event.widget == self.root:
            win_width, win_height = event.width, event.height
        else:
            win_width, win_height = self.root.winfo_width(), self.root.winfo_height()

        if win_width <= 1 or win_height <= 1:
            return
            
        current_text = self.label.cget("text")
        if not current_text:
            return

        target_width = win_width - 20
        target_height = win_height - 20

        test_size = 10
        self.dynamic_font.config(size=test_size)
        
        lines = current_text.split('\n')
        max_pixel_width = max(self.dynamic_font.measure(line) for line in lines)
        total_pixel_height = self.dynamic_font.metrics("linespace") * len(lines)

        if max_pixel_width == 0 or total_pixel_height == 0:
            return

        width_ratio = target_width / max_pixel_width
        height_ratio = target_height / total_pixel_height

        new_size = int(test_size * min(width_ratio, height_ratio))
        
        self.dynamic_font.config(size=max(8, new_size))

    def open_settings(self, event=None):
        """Spawns the settings window if it isn't already open."""
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self.root, self)
        else:
            self.settings_window.lift()

    # --- Core Timer Logic ---

    def update_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        if self.remaining_time <= 0:
            self.end_timer()
            return

        chosen_category, event_name = self.engine.process_tick(self)

        # Update telemetry
        self.telemetry.log_tick(chosen_category, event_name, self.remaining_time, self.current_delay)

        # Update UI
        self.label.config(text=format_time(self.remaining_time))
        self.resize_text()
            
        # Schedule next tick
        execution_delay = self.current_delay
        if config.DEBUG_MODE:
            execution_delay = max(5, int(self.current_delay / config.DEBUG_SPEED_MULTIPLIER))
            
        self.timer_id = self.root.after(execution_delay, self.update_timer)
        
    def reset_timer(self):
        """Called by the settings window to restart the chaos."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
            
        self.remaining_time = config.DEFAULT_START_TIME
        self.current_delay = config.DEFAULT_TICK_DELAY_MS
        
        self.label.config(
            text=format_time(self.remaining_time), 
            fg=config.TEXT_COLOR, 
            bg=config.BG_COLOR
        )
        self.resize_text()
        
        self.telemetry = TimerTelemetry(self.remaining_time)
        
        print("[GAME RESET] Timer restarted. Waiting 1 second for first tick...")
        self.timer_id = self.root.after(1000, self.update_timer)

    def end_timer(self):
        self.telemetry.show_final_stats(self.remaining_time)
        print("[GAME OVER] Timer hit 0 or went negative.")
        self.label.config(text=format_time(self.remaining_time) + "\nDone!", fg=config.DONE_COLOR)
        self.resize_text()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    timer = CursedTimer(config.DEFAULT_START_TIME)
    timer.run()