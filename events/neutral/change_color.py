import random

def trigger(timer):
    """Changes the font to a random hex color."""
    random_color = f"#{random.randint(0, 0xFFFFFF):06x}"
    timer.text_color = random_color
    timer.label.config(fg=random_color)
    timer.fire_popup("✨ Color Shift ✨", random_color)
    return False