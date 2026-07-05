def trigger(timer):
    """Subtracts 5 seconds from the timer."""
    timer.remaining_time -= 5
    return True