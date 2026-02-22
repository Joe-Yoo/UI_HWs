import random

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.metrics import dp, sp
from utils import CAUSES, DESCRIPTIONS
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

        choice_pairs = choose_two(CAUSES)
        choice_pairs = shuffle(choice_pairs)
        # print(choice_pairs)

        self.choice_pair_strings = [x[0] + "|" + x[1] for x in choice_pairs]
        self.screens = self.choice_pair_strings
        self.current_screen_index = 0
        self.setup_nested_screens()

    def setup_nested_screens(self):
        self.nested_sm = ScreenManager()
        self.nested_sm.transition = NoTransition()

        for screen_name in self.choice_pair_strings:
            screen = Screen(name=screen_name)
            this_, that_ = screen_name.split("|")
            
            if random.random() < 0.5:
                this_, that_ = that_, this_

            layout = GridLayout(
                cols=1,
                rows=5,
                padding=dp(20),
                spacing=dp(10)
            )
            
            name_label = Label(
                text="Please select the item that in your opinion\ncontributes more torwards the workload of the task you completed.",
                font_size=sp(24),
                size_hint_y=0.1,
                halign='center',
                valign='middle'
            )
            layout.add_widget(name_label)

            instructions_label = Label(
                text="[b]Mouse[/b]: Click an option\n[b]Keyboard[/b]: Use up and down arrow keys and the enter key to choose an option.",
                markup=True,
                size_hint_y=0.1,
                font_size=sp(14),
                halign='center',
                valign='middle'

            )
            layout.add_widget(instructions_label)

            # First choice: button on left, description on right
            this_row = BoxLayout(
                orientation='horizontal',
                size_hint_y=0.3,
                spacing=dp(10)
            )
            
            # Button container with padding
            this_button_container = BoxLayout(
                size_hint_x=0.5,
                padding=dp(10)
            )
            
            this_button = Button(
                text=this_,
                font_size=sp(16),
                size_hint=(1, 0.8),
                halign='center',
                valign='middle'
            )
            this_button.bind(on_press=lambda x: self.on_button_click(this_))
            this_button_container.add_widget(this_button)
            this_row.add_widget(this_button_container)
            
            this_index = CAUSES.index(this_)
            this_desc_label = Label(
                text=DESCRIPTIONS[this_index],
                font_size=sp(16),
                size_hint_x=0.5,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            this_desc_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
            this_row.add_widget(this_desc_label)
            
            layout.add_widget(this_row)

            or_label = Label(
                text="Or",
                font_size=sp(24),
                size_hint_y=0.1,
                halign='center',
                valign='middle'
            )
            layout.add_widget(or_label)

            # Second choice: button on left, description on right
            that_row = BoxLayout(
                orientation='horizontal',
                size_hint_y=0.3,
                spacing=dp(10)
            )
            
            # Button container with padding
            that_button_container = BoxLayout(
                size_hint_x=0.5,
                padding=dp(10)
            )
            
            that_button = Button(
                text=that_,
                font_size=sp(16),
                size_hint=(1, 0.8),
                halign='center',
                valign='middle'
            )
            that_button.bind(on_press=lambda x: self.on_button_click(that_))
            that_button_container.add_widget(that_button)
            that_row.add_widget(that_button_container)
            
            that_index = CAUSES.index(that_)
            that_desc_label = Label(
                text=DESCRIPTIONS[that_index],
                font_size=sp(16),
                size_hint_x=0.5,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            that_desc_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
            that_row.add_widget(that_desc_label)
            
            layout.add_widget(that_row)

            screen.add_widget(layout)
            self.nested_sm.add_widget(screen)

        self.add_widget(self.nested_sm)
    
    def on_button_click(self, selected_choice):
        """Handle button click - store choice and advance to next screen"""
        # TODO: Store the selected choice for later analysis
        print(f"Selected: {selected_choice}")
        
        # Check if this is the last comparison
        if self.current_screen_index >= len(self.screens) - 1:
            # Last comparison - go to next page (results)
            if hasattr(self.manager, 'current'):
                self.manager.current = 'questionnaire'  # Assuming next screen is 'results'
        else:
            # Go to next comparison
            self.next_subscreen()
    
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
