from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.metrics import sp, dp

TEAL_HEX   = '#00BFBF'
ORANGE_HEX = '#FF8000'


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20))
        layout.add_widget(Widget())

        self.result_label  = Label(text='', font_size=sp(48), bold=True, markup=True)
        self.reason_label  = Label(text='', font_size=sp(22), markup=True, opacity=0)
        self.p1_score_label = Label(text='', font_size=sp(28), markup=True)
        self.p2_score_label = Label(text='', font_size=sp(28), markup=True)
        layout.add_widget(self.result_label)
        layout.add_widget(self.reason_label)
        layout.add_widget(self.p1_score_label)
        layout.add_widget(self.p2_score_label)

        layout.add_widget(Widget())

        play_again_btn = Button(
            text='Play Again',
            size_hint=(0.4, None),
            height=dp(48),
            pos_hint={'center_x': 0.5},
        )
        play_again_btn.bind(on_release=self.go_to_start)
        layout.add_widget(play_again_btn)

        layout.add_widget(Widget())
        self.add_widget(layout)

    def show_result(self, winner, p1_count, p2_count, reason=None):
        if winner == 1:
            self.result_label.text = f'[color={TEAL_HEX}]Player 1 Wins![/color]'
        elif winner == 2:
            self.result_label.text = f'[color={ORANGE_HEX}]Player 2 Wins![/color]'
        else:
            self.result_label.text = "[color=#FFFFFF]It's a Tie![/color]"

        if reason == 'timeout':
            loser = 1 if winner == 2 else 2
            loser_hex = TEAL_HEX if loser == 1 else ORANGE_HEX
            self.reason_label.text = (
                f'[color={loser_hex}]Player {loser}[/color] ran out of time'
            )
            self.reason_label.opacity = 1
        else:
            self.reason_label.text = ''
            self.reason_label.opacity = 0

        self.p1_score_label.text = f'[color={TEAL_HEX}]Player 1[/color]: {p1_count}'
        self.p2_score_label.text = f'[color={ORANGE_HEX}]Player 2[/color]: {p2_count}'

    def go_to_start(self, *args):
        self.manager.current = 'start'
