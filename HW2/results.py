from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text='Results Page', font_size=24)
        self.add_widget(label)
