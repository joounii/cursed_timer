from events.increasing import add_time
from events.neutral import change_color
from events.decreasing import remove_time

EVENT_CATEGORIES = {
    "increasing": {
        add_time: 10,
    },
    "neutral": {
        change_color: 50,
    },
    "decreasing": {
        remove_time: 10,
    }
}
