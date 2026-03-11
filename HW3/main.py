import random

from kivy_config_helper import config_kivy
config_kivy(window_width=800, window_height=600)

import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp, sp

class RSVP(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def build(self):
        pass

if __name__ == '__main__':
    RSVP().run()

