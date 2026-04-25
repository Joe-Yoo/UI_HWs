import random

from kivy_config_helper import config_kivy
config_kivy(window_width=800, window_height=800)

import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp, sp

from start_screen import StartScreen
from game_screen import GameScreen
from results_screen import ResultsScreen


class Ataxx(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(ResultsScreen(name='results'))
        return sm

if __name__ == '__main__':
    Ataxx().run()

