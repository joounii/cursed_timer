import random
import config

class TrulyRandomEngine:
    def __init__(self):
        self.name = "Truly Random"

    def process_tick(self, timer):

        # Roll for categories using the static config weights
        cat_weights = [config.CHANCE_INCREASING, config.CHANCE_NEUTRAL, config.CHANCE_DECREASING]
        chosen_category = random.choices(list(timer.categories.keys()), weights=cat_weights, k=1)[0]
        event_dict = timer.categories[chosen_category]
        
        skip_countdown = False
        event_name = "None"
        
        # Roll for specific event within the category
        if event_dict:
            event_pool, event_weights = list(event_dict.keys()), list(event_dict.values())
            chosen_event = random.choices(event_pool, weights=event_weights, k=1)[0]
            event_name = chosen_event.__name__.split('.')[-1]
            skip_countdown = chosen_event.trigger(timer)
        
        # Modify the timer's remaining time directly
        if not skip_countdown:
            timer.remaining_time -= 1
            
        return chosen_category, event_name
    