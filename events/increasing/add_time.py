def trigger(timer):
    """Adds 5 seconds to the timer."""
    timer.remaining_time += 5
    return True