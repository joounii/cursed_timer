def trigger(timer):
    """Subtracts 5 seconds from the timer."""
    timer.remaining_time -= 5
    timer.fire_popup("-5 Seconds!", "#ff5555")
    return True