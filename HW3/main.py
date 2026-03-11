import random

from kivy_config_helper import config_kivy
config_kivy(window_width=500, window_height=300)

import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp, sp
from Player import Player

class RSVP(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None
    
    def build(self):
        self.screen_manager = ScreenManager(transition=NoTransition())
        
        player_screen = Player(name='player')
        self.screen_manager.add_widget(player_screen)
        
        return self.screen_manager

if __name__ == '__main__':
    RSVP().run()

