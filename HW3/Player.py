from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import sp, dp
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class Player(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation='vertical')

        self.top_bar = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.25),
            padding=[dp(15), dp(15), dp(15), dp(15)]
        )
        left_btn = Button(text='Choose File', size_hint=(0.5, 1), width=100)
        spacer = Widget()
        right_btn = Button(text='Settings', size_hint=(0.5, 1), width=100)

        self.top_bar.add_widget(left_btn)
        self.top_bar.add_widget(spacer)
        self.top_bar.add_widget(right_btn)

        top_line = Widget(size_hint=(1, None), height=dp(2))
        with top_line.canvas:
            Color(1, 1, 1, 1)
            top_line.rect = Rectangle(pos=top_line.pos, size=top_line.size)
        top_line.bind(pos=lambda instance, value: setattr(instance.rect, 'pos', value))
        top_line.bind(size=lambda instance, value: setattr(instance.rect, 'size', value))

        self.middle = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.50)
        )
        self.middle.add_widget(Label(text='Middle Text'))

        bottom_line = Widget(size_hint=(1, None), height=dp(2))
        with bottom_line.canvas:
            Color(1, 1, 1, 1)
            bottom_line.rect = Rectangle(pos=bottom_line.pos, size=bottom_line.size)
        bottom_line.bind(pos=lambda instance, value: setattr(instance.rect, 'pos', value))
        bottom_line.bind(size=lambda instance, value: setattr(instance.rect, 'size', value))

        self.bottom_bar = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.25)
        )
        self.bottom_bar.add_widget(Label(text='Bottom Section'))

        root.add_widget(self.top_bar)
        root.add_widget(top_line)
        root.add_widget(self.middle)
        root.add_widget(bottom_line)
        root.add_widget(self.bottom_bar)

        self.add_widget(root)