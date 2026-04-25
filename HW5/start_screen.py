from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp, sp


ACTIVE_COLOR = (0.2, 0.6, 1, 1)
INACTIVE_COLOR = (0.3, 0.3, 0.3, 1)
PILL_BG = (0.15, 0.15, 0.15, 1)


class PillToggle(BoxLayout):
    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint', (None, None))
        super().__init__(
            orientation='horizontal',
            size=(dp(300), dp(44)),
            **kwargs,
        )
        self.time_mode = 'Unlimited'
        self.options = ['Unlimited', 'Select Minutes']
        self.on_mode_change = None

        with self.canvas.before:
            Color(*PILL_BG)
            self.pill_bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(22)])

        self.bind(pos=self.update_bg, size=self.update_bg)

        self.btns = []
        for option in self.options:
            btn = Button(
                text=option,
                background_normal='',
                background_color=(0, 0, 0, 0),
                color=(1, 1, 1, 1),
                font_size=dp(14),
            )
            btn.bind(on_release=self.on_toggle)
            with btn.canvas.before:
                btn._color_instr = Color(*ACTIVE_COLOR if option == 'Unlimited' else INACTIVE_COLOR)
                btn._rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(22)])
            btn.bind(pos=self.update_btn_bg, size=self.update_btn_bg)
            self.add_widget(btn)
            self.btns.append(btn)

    def update_bg(self, *args):
        self.pill_bg.pos = self.pos
        self.pill_bg.size = self.size

    def update_btn_bg(self, btn, *args):
        btn._rect.pos = btn.pos
        btn._rect.size = btn.size

    def on_toggle(self, btn):
        self.time_mode = btn.text
        for b in self.btns:
            active = b.text == self.time_mode
            b._color_instr.rgba = ACTIVE_COLOR if active else INACTIVE_COLOR
        if self.on_mode_change:
            self.on_mode_change(self.time_mode)


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = 1

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))

        layout.add_widget(Widget())

        layout.add_widget(Label(text='Ataxx', font_size=sp(64)))

        selector = BoxLayout(orientation='horizontal', spacing=dp(12),
                             size_hint=(None, None), size=(dp(268), dp(160)),
                             pos_hint={'center_x': 0.5})
        left_btn = Button(text='<', size_hint=(None, None), size=(dp(32), dp(32)),
                          pos_hint={'center_y': 0.5})
        left_btn.bind(on_release=self.prev_level)

        self.level_label = Label(text='1', size_hint=(None, None), size=(dp(160), dp(160)),
                                 pos_hint={'center_y': 0.5})
        with self.level_label.canvas.before:
            Color(1, 1, 1, 1)
            self.level_box = Line(rectangle=(self.level_label.x, self.level_label.y,
                                             dp(160), dp(160)), width=1.5)
        self.level_label.bind(pos=self.update_level_box, size=self.update_level_box)

        right_btn = Button(text='>', size_hint=(None, None), size=(dp(32), dp(32)),
                           pos_hint={'center_y': 0.5})
        right_btn.bind(on_release=self.next_level)
        selector.add_widget(left_btn)
        selector.add_widget(self.level_label)
        selector.add_widget(right_btn)
        layout.add_widget(selector)

        self.pill = PillToggle(size_hint=(None, None), pos_hint={'center_x': 0.5})
        self.pill.on_mode_change = self.on_time_mode_change
        layout.add_widget(self.pill)

        self.minutes_input = TextInput(
            hint_text='Minutes',
            input_filter='int',
            multiline=False,
            halign='center',
            disabled=True,
            size_hint=(0.4, None),
            height=dp(40),
            pos_hint={'center_x': 0.5},
        )
        self.minutes_input.bind(text=self.validate_start)
        layout.add_widget(self.minutes_input)

        self.start_btn = Button(
            text='Start!',
            size_hint=(0.4, None),
            height=dp(44),
            pos_hint={'center_x': 0.5},
        )
        self.start_btn.bind(on_release=self.go_to_game)
        layout.add_widget(self.start_btn)

        layout.add_widget(Widget())

        self.add_widget(layout)

    def update_level_box(self, *args):
        self.level_box.rectangle = (*self.level_label.pos, *self.level_label.size)

    def go_to_game(self, *args):
        if self.pill.time_mode == 'Select Minutes' and self.minutes_input.text:
            time_limit = int(self.minutes_input.text) * 60
        else:
            time_limit = None
        self.manager.get_screen('game').load_level(self.level, time_limit)
        self.manager.current = 'game'

    def validate_start(self, *args):
        if self.pill.time_mode == 'Select Minutes':
            self.start_btn.disabled = not (self.minutes_input.text and int(self.minutes_input.text) > 0)

    def on_time_mode_change(self, mode):
        self.minutes_input.disabled = mode == 'Unlimited'
        self.start_btn.disabled = mode == 'Select Minutes' and not (
            self.minutes_input.text and int(self.minutes_input.text) > 0
        )

    def prev_level(self, *args):
        self.level = (self.level - 2) % 4 + 1
        self.level_label.text = str(self.level)

    def next_level(self, *args):
        self.level = self.level % 4 + 1
        self.level_label.text = str(self.level)
