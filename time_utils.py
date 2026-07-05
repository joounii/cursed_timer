# ==========================================
# Time Formatting Utility
# ==========================================

def format_time(total_seconds):
    """
    Converts seconds into a responsive D:HH:MM:SS format.
    Days and Hours only appear if they are greater than 0.
    Minutes and Seconds are always displayed.
    """
    is_negative = total_seconds < 0
    total_seconds = abs(int(total_seconds))
    
    # Cascade the time upwards
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    
    # Build the string dynamically based on size
    if d > 0:
        formatted_time = f"{d}:{h:02d}:{m:02d}:{s:02d}"
    elif h > 0:
        formatted_time = f"{h:02d}:{m:02d}:{s:02d}"
    else:
        formatted_time = f"{m:02d}:{s:02d}"
        
    return f"-{formatted_time}" if is_negative else formatted_time