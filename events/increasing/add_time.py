def trigger(timer):
    """Adds 5 seconds to the timer."""
    timer.remaining_time += 5
    timer.fire_popup("+5 Seconds!", "#55ff55")
    return True