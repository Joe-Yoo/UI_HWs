import random

# Import and configure kivy BEFORE any other kivy modules
from kivy_config_helper import config_kivy
config_kivy(window_width=800, window_height=600)

import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.core.window import Window
from questionnaire import QuestionnaireScreen
from comparison import ComparisonScreen
from results import ResultsScreen
from kivy.metrics import dp, sp

class DemoApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screens = ['comparison', 'questionnaire', 'results']
        self.current_screen_index = 0
    
    def build(self):
        self.sm = ScreenManager()
        self.sm.transition = NoTransition()
        
        comparison = ComparisonScreen(name='comparison')
        questionnaire = QuestionnaireScreen(name='questionnaire')
        results = ResultsScreen(name='results')
        
        self.sm.add_widget(comparison)
        self.sm.add_widget(questionnaire)
        self.sm.add_widget(results)
        
        Window.bind(on_key_down=self.on_key_down)
        
        return self.sm
    
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # print(keycode)
        if keycode == 29:
            self.previous_screen()
            return True
        elif keycode == 27:
            self.next_screen() 
            return True
        return False
    
    def next_screen(self):
        if not self.current_screen_index + 1 == len(self.screens): 
            self.current_screen_index = (self.current_screen_index + 1)
            self.sm.current = self.screens[self.current_screen_index]
    
    def previous_screen(self):
        if not self.current_screen_index == 0: 
            self.current_screen_index = (self.current_screen_index - 1) % len(self.screens)
            self.sm.current = self.screens[self.current_screen_index]

    # sp for fonts
    # dp for scaling, padding, etc.

if __name__ == '__main__':
    DemoApp().run()

