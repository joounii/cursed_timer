import time
from collections import Counter
import config
from time_utils import format_time

class TimerTelemetry:
    # Handles all data tracking, logging, and end-game statistics.
    
    def __init__(self, starting_time):
        self.starting_time = starting_time
        self.start_wall_clock = time.time()
        
        self.total_ticks = 0
        self.total_simulated_seconds = 0.0
        self.last_tick_time = starting_time
        self.match_history = []

    def log_tick(self, category, event_name, current_time, delay_ms):
        # Records a single tick and prints real-time telemetry.
        self.total_ticks += 1
        self.total_simulated_seconds += (delay_ms / 1000.0)
        
        tick_delta = current_time - self.last_tick_time
        self.match_history.append({
            "category": category,
            "event": event_name,
            "delta": tick_delta
        })
        
        total_drift = current_time - self.starting_time
        avg_change_per_tick = total_drift / self.total_ticks
        
        real_seconds_passed = max(0.001, time.time() - self.start_wall_clock)
        true_velocity = total_drift / real_seconds_passed
        
        # Predict when the timer will finish based on chaos velocity
        if true_velocity >= 0:
            predicted_finish = "INFINITE"
        else:
            real_seconds_to_zero = current_time / abs(true_velocity)
            predicted_finish = f"{format_time(real_seconds_to_zero)} ({int(real_seconds_to_zero)}s)"
        
        formatted_current = format_time(current_time)
        
        print(
            f"[TICK {self.total_ticks:03d}] "
            f"TickSpeed: {delay_ms:4d}ms | "
            f"Event: {event_name:<13} | "
            f"Delta: {tick_delta:+d}s | "
            f"Avg/Tick: {avg_change_per_tick:+.2f}s | "
            f"TrueVelo: {true_velocity:+.2f}s/s | "
            f"PRED FINISH: {predicted_finish:<15} | "
            f"TRUE TIME: {formatted_current} ({current_time}s)"
        )
        
        self.last_tick_time = current_time

    def show_final_stats(self, final_time):
        """Processes match history and prints the end-game summary."""
        print("\n" + "="*60)
        print("                CURSED TIMER RESULTS                  ")
        print("="*60)
        
        real_time_spent = time.time() - self.start_wall_clock
        projected_play_time = real_time_spent * config.DEBUG_SPEED_MULTIPLIER if config.DEBUG_MODE else real_time_spent
            
        formatted_proj = format_time(projected_play_time)
        formatted_sim = format_time(self.total_simulated_seconds)
        
        categories_logged = [t["category"] for t in self.match_history]
        events_logged = [t["event"] for t in self.match_history]
        
        cat_counts = Counter(categories_logged)
        event_counts = Counter(events_logged)
        
        total_time_added = sum(t["delta"] for t in self.match_history if t["delta"] > 0)
        total_time_stolen = abs(sum(t["delta"] for t in self.match_history if t["delta"] < -1))
        
        most_common_event = event_counts.most_common(1)[0][0] if events_logged else "None"
        most_common_cat = cat_counts.most_common(1)[0][0] if categories_logged else "None"
        
        print(f"Total Processing Cycles (Ticks):  {self.total_ticks}")
        print(f"Simulated Runtime (Weighted):     {formatted_sim} ({int(self.total_simulated_seconds)}s)")
        print(f"Projected Normal Play Time:       {formatted_proj} ({int(projected_play_time)}s)")
        print(f"Actual Debug Real-World Runtime:  {int(real_time_spent)}s")
        print(f"Initial Starting Setpoint:        {self.starting_time}s")
        print("-" * 60)
        print(f"Total Time Bestowed (Events):     +{total_time_added}s")
        print(f"Total Time Sabotaged (Events):    -{total_time_stolen}s")
        print(f"Net Chaotic Time Variance:        {final_time - self.starting_time + self.total_ticks:+d}s")
        print("-" * 60)
        
        print("Category Distribution Analysis:")
        for cat in ["increasing", "neutral", "decreasing"]:
            count = cat_counts.get(cat, 0)
            pct = (count / self.total_ticks * 100) if self.total_ticks else 0
            print(f"  > {cat:<12}: {count:3d} times ({pct:.1f}%)")
            
        print("-" * 60)
        print(f"Primary Agent of Chaos:           {most_common_event}")
        print(f"Most Frequent Event Category:     {most_common_cat.upper()}")
        print("="*60 + "\n")