import random

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.metrics import dp, sp
from utils import CAUSES, DESCRIPTIONS
from user_data import user_data
# code taken from the sample code given from the assignment lol
def choose_two(lst):
    res = []
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
        self.selected_button_index = -1
        self.current_buttons = []
        self.current_choices = []
        self.setup_nested_screens()

    def setup_nested_screens(self):
        self.nested_sm = ScreenManager()
        self.nested_sm.transition = NoTransition()

        for screen_index, screen_name in enumerate(self.choice_pair_strings):
            screen = Screen(name=screen_name)
            this_, that_ = screen_name.split("|")
            
            if random.random() < 0.5:
                this_, that_ = that_, this_

            main_layout = BoxLayout(
                orientation='vertical',
                padding=dp(20),
                spacing=dp(10)
            )

            layout = GridLayout(
                cols=1,
                rows=5,
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
                text="[b]Mouse[/b]: Click an option\n[b]Keyboard[/b]: Press tab to navigate. Press Enter to select.",
                markup=True,
                size_hint_y=0.1,
                font_size=sp(14),
                halign='center',
                valign='middle'

            )
            layout.add_widget(instructions_label)

            this_row = BoxLayout(
                orientation='horizontal',
                size_hint_y=0.3,
                spacing=dp(10)
            )
            
            this_button_container = BoxLayout(
                size_hint_x=0.5,
                padding=dp(50)
            )
            
            this_button = Button(
                text=this_,
                font_size=sp(16),
                size_hint=(0.8, 0.8),
                halign='center',
                valign='middle'
            )
            this_button.bind(on_press=lambda x, choice=this_: self.on_button_click(choice))
            this_button_container.add_widget(this_button)
            
            this_selected = Label(
                text='<',
                font_size=sp(24),
                size_hint=(0.2, 0.8),
                opacity=0,
                halign='center',
                valign='middle'
            )
            this_button_container.add_widget(this_selected)
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

            that_row = BoxLayout(
                orientation='horizontal',
                size_hint_y=0.3,
                spacing=dp(10)
            )
        
            that_button_container = BoxLayout(
                size_hint_x=0.5,
                padding=dp(50)
            )
            
            that_button = Button(
                text=that_,
                font_size=sp(16),
                size_hint=(0.8, 0.8),
                halign='center',
                valign='middle'
            )
            that_button.bind(on_press=lambda x, choice=that_: self.on_button_click(choice))
            that_button_container.add_widget(that_button)
            
            that_selected = Label(
                text='<',
                font_size=sp(24),
                size_hint=(0.2, 0.8),
                opacity=0,
                halign='center',
                valign='middle'
            )
            that_button_container.add_widget(that_selected)
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

            main_layout.add_widget(layout)

            nav_layout = GridLayout(
                cols=2,
                rows=1,
                size_hint_y=0.07,
                height=dp(50),
                spacing=dp(0)
            )
            
            if screen_index > 0:
                prev_button_container = AnchorLayout(
                    size_hint_x=0.5,
                    anchor_x='left',
                    anchor_y='center'
                )
                prev_button = Button(
                    text='Previous',
                    size_hint=(0.6, 1)
                )
                prev_button.bind(on_press=lambda x: self.previous_subscreen())
                prev_button_container.add_widget(prev_button)
                nav_layout.add_widget(prev_button_container)
            else:
                prev_button = None
                nav_layout.add_widget(Label(text='', size_hint_x=0.5))
            
            next_button_container = AnchorLayout(
                size_hint_x=0.5,
                anchor_x='right',
                anchor_y='center'
            )
            next_button = Button(
                text='Next',
                size_hint=(0.6, 1),
                disabled=True
            )
            next_button.bind(on_press=lambda x: self.next_subscreen())
            next_button_container.add_widget(next_button)
            nav_layout.add_widget(next_button_container)
            
            main_layout.add_widget(nav_layout)

            screen.button_data = {
                'buttons': [this_button, that_button],
                'choices': [this_, that_],
                'original_texts': [this_, that_],
                'original_font_size': sp(16),
                'checkmarks': [this_selected, that_selected],
                'prev_button': prev_button,
                'next_button': next_button
            }

            screen.add_widget(main_layout)
            self.nested_sm.add_widget(screen)

        self.add_widget(self.nested_sm)
        self.update_current_screen_data()
    
    def update_current_screen_data(self):
        current_screen = self.nested_sm.current_screen
        if hasattr(current_screen, 'button_data'):
            self.current_buttons = current_screen.button_data['buttons']
            self.current_choices = current_screen.button_data['choices']
            self.original_texts = current_screen.button_data['original_texts']
            self.original_font_size = current_screen.button_data['original_font_size']
            self.current_checkmarks = current_screen.button_data['checkmarks']
            self.current_prev_button = current_screen.button_data['prev_button']
            self.current_next_button = current_screen.button_data['next_button']
            
            # Build list of all focusable elements in order
            self.focusable_elements = list(self.current_buttons)  # [this_button, that_button]
            if self.current_prev_button:
                self.focusable_elements.append(self.current_prev_button)
            self.focusable_elements.append(self.current_next_button)
            
            # Store original nav button texts
            self.nav_button_texts = {}
            if self.current_prev_button:
                self.nav_button_texts[self.current_prev_button] = 'Previous'
            self.nav_button_texts[self.current_next_button] = 'Next'
            
            self.selected_button_index = -1 
            
            # Check if a selection was already made (if any checkmark is visible)
            has_selection = any(checkmark.opacity > 0 for checkmark in self.current_checkmarks)
            self.current_next_button.disabled = not has_selection
            
            self.update_button_styling()
    
    def update_button_styling(self):
        # Update choice buttons (this_ and that_)
        for i, button in enumerate(self.current_buttons):
            if i == self.selected_button_index:
                button.text = f"[size={int(self.original_font_size * 1.3)}][b]{self.original_texts[i]}[/b][/size]"
                button.markup = True
            else:
                button.text = self.original_texts[i]
                button.markup = False
        
        if self.selected_button_index >= len(self.current_buttons):
            focused_element = self.focusable_elements[self.selected_button_index]
            
            if self.current_prev_button:
                self.current_prev_button.text = 'Previous'
                self.current_prev_button.markup = False
            self.current_next_button.text = 'Next'
            self.current_next_button.markup = False
            
            original_text = self.nav_button_texts[focused_element]
            focused_element.text = f"[size={int(self.original_font_size * 1.3)}][b]{original_text}[/b][/size]"
            focused_element.markup = True
        else:
            if self.current_prev_button:
                self.current_prev_button.text = 'Previous'
                self.current_prev_button.markup = False
            self.current_next_button.text = 'Next'
            self.current_next_button.markup = False
    
    def on_button_click(self, selected_choice):
        
        option1, option2 = self.current_choices[0], self.current_choices[1]
        user_data.add_comparison_choice(option1, option2, selected_choice)
        
        for i, choice in enumerate(self.current_choices):
            if choice == selected_choice:
                self.current_checkmarks[i].opacity = 1
            else:
                self.current_checkmarks[i].opacity = 0
        
        self.current_next_button.disabled = False
    
    def on_enter(self):
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_touch_down=self.on_window_touch)
        self.update_current_screen_data()
    
    def on_leave(self):
        Window.unbind(on_key_down=self.on_key_down)
        Window.unbind(on_touch_down=self.on_window_touch)
    
    def on_window_touch(self, instance, touch):
        self.reset_button_styling()
        return False
    
    def reset_button_styling(self):
        for i, button in enumerate(self.current_buttons):
            button.text = self.original_texts[i]
            button.markup = False
        
        if self.current_prev_button:
            self.current_prev_button.text = 'Previous'
            self.current_prev_button.markup = False
        self.current_next_button.text = 'Next'
        self.current_next_button.markup = False
        
        self.selected_button_index = -1
    
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 43:  # Tab key
            if self.selected_button_index < 0:
                self.selected_button_index = 0
            else:
                original_index = self.selected_button_index
                attempts = 0
                max_attempts = len(self.focusable_elements)
                
                while attempts < max_attempts:
                    if self.selected_button_index < len(self.focusable_elements) - 1:
                        self.selected_button_index += 1
                    else:
                        self.selected_button_index = 0
                    
                    current_element = self.focusable_elements[self.selected_button_index]
                    if not hasattr(current_element, 'disabled') or not current_element.disabled:
                        break
                    
                    attempts += 1
                
            self.update_button_styling()
            return True
        elif keycode == 40:
            if 0 <= self.selected_button_index < len(self.current_choices):
                selected_choice = self.current_choices[self.selected_button_index]
                self.on_button_click(selected_choice)
            elif self.selected_button_index >= len(self.current_buttons):
                focused_element = self.focusable_elements[self.selected_button_index]
                if focused_element == self.current_prev_button:
                    self.previous_subscreen()
                elif focused_element == self.current_next_button and not self.current_next_button.disabled:
                    self.next_subscreen()
            return True
        return False
    
    def next_subscreen(self):
        if self.current_screen_index < len(self.screens) - 1:
            self.current_screen_index += 1
            self.nested_sm.current = self.screens[self.current_screen_index]
            self.update_current_screen_data()
        else:
            self.manager.current = 'questionnaire'
    
    def previous_subscreen(self):
        if self.current_screen_index > 0:
            self.current_screen_index -= 1
            self.nested_sm.current = self.screens[self.current_screen_index]
            self.update_current_screen_data()
