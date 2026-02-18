import random

from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.core.window import Window

# code taken from the sample code given from the assignment lol
def choose_two(lst):
    res = []
    res_str = []
    for i in range(len(lst)-1):
        for j in range(i+1, len(lst)):
            tup = (lst[i], lst[j])
            res.append(tup)
    return res

def shuffle(lst):
    clst = lst.copy()
    res = []
    while len(clst) > 0:
        index = random.randint(0, len(clst) - 1)
        res.append(clst[index])
        del clst[index]
    return res

class ComparisonScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        choices = ['Mental Demand', 'Physical Demand', 'Temporal Demand', 'Performance', 'Effort', 'Frustration']
        choice_pairs = choose_two(choices)
        choice_pairs = shuffle(choice_pairs)
        # print(choice_pairs)

        self.choice_pair_strings = [x[0] + " vs " + x[1] for x in choice_pairs]
        self.screens = ['main'] + self.choice_pair_strings
        self.current_screen_index = 0
        self.setup_nested_screens()

    def setup_nested_screens(self):
        self.nested_sm = ScreenManager()
        self.nested_sm.transition = NoTransition()

        main_screen = Screen(name='main')
        main_label = Label(text='Comparison page', font_size=24)
        main_screen.add_widget(main_label)

        self.nested_sm.add_widget(main_screen)
        
        for screen_name in self.choice_pair_strings:
            screen = Screen(name=screen_name)
            label = Label(text=screen_name, font_size=24)
            screen.add_widget(label)
            self.nested_sm.add_widget(screen)

        
        self.add_widget(self.nested_sm)
    
    def on_enter(self):
        # Bind keyboard events when entering this screen
        Window.bind(on_key_down=self.on_key_down)
    
    def on_leave(self):
        # Unbind keyboard events when leaving this screen
        Window.unbind(on_key_down=self.on_key_down)
    
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # Only handle up/down arrows
        if keycode == 82:  # Up arrow
            self.previous_subscreen()
            return True
        elif keycode == 81:  # Down arrow
            self.next_subscreen()
            return True
        return False  # Let other screens handle left/right arrows
    
    def next_subscreen(self):
        if self.current_screen_index < len(self.screens) - 1:
            self.current_screen_index += 1
            self.nested_sm.current = self.screens[self.current_screen_index]
    
    def previous_subscreen(self):
        if self.current_screen_index > 0:
            self.current_screen_index -= 1
            self.nested_sm.current = self.screens[self.current_screen_index]
