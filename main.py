import tkinter as tk
import random
from events.increasing import add_time
from events.neutral import change_color
from events.decreasing import remove_time
import time

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
        
        self.DEBUG_MODE = True
        self.DEBUG_SPEED_MULTIPLIER = 100
        
        self.current_delay = 10
        
        self.resize_margin = 15
        self.is_resizing = False
        self.starting_time = duration_seconds
        self.last_tick_time = duration_seconds
        self.total_ticks = 0
        self.total_simulated_seconds = 0.0
        self.start_wall_clock = time.time()
        self.match_history = []
        
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
            
    def show_stats(self):
        import time
        from collections import Counter
        
        print("\n" + "="*60)
        print("                 CURSED TIMER RESULTS                  ")
        print("="*60)
        
        real_time_spent = time.time() - self.start_wall_clock
        
        projected_play_time = real_time_spent
        if self.DEBUG_MODE:
            projected_play_time = real_time_spent * self.DEBUG_SPEED_MULTIPLIER
            
        proj_m, proj_s = divmod(int(projected_play_time), 60)
        sim_m, sim_s = divmod(int(self.total_simulated_seconds), 60)
        
        categories_logged = [t["category"] for t in self.match_history]
        events_logged = [t["event"] for t in self.match_history]
        
        cat_counts = Counter(categories_logged)
        event_counts = Counter(events_logged)
        
        total_time_added = sum(t["delta"] for t in self.match_history if t["delta"] > 0)
        total_time_stolen = abs(sum(t["delta"] for t in self.match_history if t["delta"] < -1))
        
        most_common_event = event_counts.most_common(1)[0][0] if events_logged else "None"
        most_common_cat = cat_counts.most_common(1)[0][0] if categories_logged else "None"
        
        print(f"Total Processing Cycles (Ticks):  {self.total_ticks}")
        print(f"Simulated Runtime (Weighted):     {sim_m:02d}:{sim_s:02d} ({int(self.total_simulated_seconds)}s)")
        print(f"Projected Normal Play Time:       {proj_m:02d}:{proj_s:02d} ({int(projected_play_time)}s)")
        print(f"Actual Debug Real-World Runtime:  {int(real_time_spent)}s")
        print(f"Initial Starting Setpoint:        {self.starting_time}s")
        print("-"*60)
        print(f"Total Time Bestowed (Events):     +{total_time_added}s")
        print(f"Total Time Sabotaged (Events):    -{total_time_stolen}s")
        print(f"Net Chaotic Time Variance:        {self.remaining_time - self.starting_time + self.total_ticks:+d}s")
        print("-"*60)
        print("Category Distribution Analysis:")
        for cat in ["increasing", "neutral", "decreasing"]:
            count = cat_counts.get(cat, 0)
            pct = (count / self.total_ticks * 100) if self.total_ticks else 0
            print(f"  > {cat:<12}: {count:3d} times ({pct:.1f}%)")
        print("-"*60)
        print(f"Primary Agent of Chaos:           {most_common_event}")
        print(f"Most Frequent Event Category:     {most_common_cat.upper()}")
        print("="*60 + "\n")
        
        self.label.config(text="00:00\nDone!", fg="#ff5555")

    def update_timer(self):
        import time
        
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
                
            default_behavior = not skip_countdown
            
            if default_behavior:
                self.remaining_time -= 1
            
            # --- TELEMETRY CALCULATIONS ---
            self.total_ticks += 1
            self.total_simulated_seconds += (self.current_delay / 1000.0)
            tick_delta = self.remaining_time - self.last_tick_time
            delta_str = f"{tick_delta:+d}s"
            
            # Record this tick's data to history for end-game statistics
            self.match_history.append({
                "category": chosen_category,
                "event": chosen_event_name,
                "delta": tick_delta
            })
            
            total_drift = self.remaining_time - self.starting_time
            avg_change_per_tick = total_drift / self.total_ticks
            
            real_seconds_passed = max(0.001, time.time() - self.start_wall_clock)
            true_velocity = total_drift / real_seconds_passed
            
            if true_velocity >= 0:
                predicted_finish = "INFINITE"
            else:
                real_seconds_to_zero = self.remaining_time / abs(true_velocity)
                pred_mins, pred_secs = divmod(int(real_seconds_to_zero), 60)
                predicted_finish = f"{pred_mins:02d}:{pred_secs:02d} ({int(real_seconds_to_zero)}s)"
            
            true_mins, true_secs = divmod(self.remaining_time, 60)
            formatted_true_time = f"{true_mins:02d}:{true_secs:02d}"
            
            log_msg = (
                f"[TICK {self.total_ticks:03d}] "
                f"TickSpeed: {self.current_delay:4d}ms | "
                f"Event: {chosen_event_name:<13} | "
                f"Delta: {delta_str:<5} | "
                f"Avg/Tick: {avg_change_per_tick:+.2f}s | "
                f"TrueVelo: {true_velocity:+.2f}s/s | "
                f"PRED FINISH: {predicted_finish:<15} | "
                f"TRUE TIME: {formatted_true_time} ({self.remaining_time}s)"
            )
            print(log_msg)
            
            self.last_tick_time = self.remaining_time
            
            mins, secs = divmod(self.remaining_time, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")
                
            execution_delay = self.current_delay
            if self.DEBUG_MODE:
                execution_delay = max(5, int(self.current_delay / self.DEBUG_SPEED_MULTIPLIER))
                
            self.timer_id = self.root.after(execution_delay, self.update_timer)
        else:
            # --- THE TIMER FINISHED ---
            self.show_stats()
            print("[GAME OVER] Timer hit 0 or went negative.")
            self.label.config(text="00:00\nDone!", fg="#ff5555")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    timer = CursedTimer(300)
    timer.run()