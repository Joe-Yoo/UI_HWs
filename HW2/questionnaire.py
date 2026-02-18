from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class QuestionnaireScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text='Questionnaire Page', font_size=24)
        self.add_widget(label)
