import random

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

class NASA_TLX(App):
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
        
        return self.sm

if __name__ == '__main__':
    NASA_TLX().run()

