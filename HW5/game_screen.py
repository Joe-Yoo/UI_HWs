import json
import os

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.metrics import dp, sp
from kivy.clock import Clock

from board import Board, EMPTY, WALL
from player import Player

ROWS = 7
COLS = 7

TEAL        = (0, 0.75, 0.75, 1)
ORANGE      = (1, 0.5,  0,    1)
TEAL_HEX    = '#00BFBF'
ORANGE_HEX  = '#FF8000'


class BlackWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class Cell(Widget):
    def __init__(self, row, col, on_tap=None, **kwargs):
        super().__init__(**kwargs)
        self.row = row
        self.col = col
        self.state = EMPTY
        self.highlighted = False
        self.on_tap = on_tap
        self.bind(pos=self.redraw, size=self.redraw)

    def set_state(self, state):
        self.state = state
        self.redraw()

    def redraw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=self.pos, size=self.size)

            if self.state == WALL:
                Color(0.45, 0.45, 0.45, 1)
                Rectangle(pos=self.pos, size=self.size)
            elif self.state == 1:
                Color(*TEAL)
                pad = self.width * 0.15
                Ellipse(pos=(self.x + pad, self.y + pad),
                        size=(self.width - pad * 2, self.height - pad * 2))
            elif self.state == 2:
                Color(*ORANGE)
                pad = self.width * 0.15
                Ellipse(pos=(self.x + pad, self.y + pad),
                        size=(self.width - pad * 2, self.height - pad * 2))
            elif self.highlighted:
                Color(0.5, 0.5, 0.5, 1)
                pad = self.width * 0.25
                Ellipse(pos=(self.x + pad, self.y + pad),
                        size=(self.width - pad * 2, self.height - pad * 2))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.on_tap:
                self.on_tap(self.row, self.col)
            return True
        return super().on_touch_down(touch)


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = 1
        self.current_player = 1
        self.selected_cell = None
        self.time_limit = None
        self.p1_time = 0
        self.p2_time = 0
        self.game_started = False
        self._timer_event = None
        self.board = Board(ROWS, COLS)
        self.players = [
            Player(color=TEAL),
            Player(color=ORANGE),
        ]

        self.levels_path = os.path.join(os.path.dirname(__file__), 'levels-1.txt')

        root = BoxLayout(orientation='vertical', spacing=2, padding=0)
        with root.canvas.before:
            Color(1, 1, 1, 1)
            self.root_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self.update_root_rect, size=self.update_root_rect)

        top_area = AnchorLayout(size_hint=(1, 0.8), anchor_x='center', anchor_y='center')
        with top_area.canvas.before:
            Color(0, 0, 0, 1)
            self.top_rect = Rectangle(pos=top_area.pos, size=top_area.size)
        top_area.bind(pos=self.update_top_rect, size=self.update_top_rect)

        self.grid = GridLayout(
            cols=COLS, rows=ROWS,
            spacing=2, padding=2,
            size_hint=(None, None),
            size=(dp(280), dp(280)),
            col_default_width=dp(38),
            row_default_height=dp(38),
            col_force_default=True,
            row_force_default=True,
        )
        with self.grid.canvas.before:
            Color(1, 1, 1, 1)
            self.grid_rect = Rectangle(pos=self.grid.pos, size=self.grid.size)
        self.grid.bind(pos=self.update_grid_rect, size=self.update_grid_rect)

        self.cells = {}
        for row in range(ROWS):
            for col in range(COLS):
                cell = Cell(row, col, on_tap=self.handle_tap)
                self.grid.add_widget(cell)
                self.cells[(row, col)] = cell

        top_area.add_widget(self.grid)

        def resize_grid(*args):
            pad = dp(24)
            side = min(top_area.width - pad * 2, top_area.height - pad * 2)
            if side <= 0:
                return
            cell_size = (side - 4 - 2 * (COLS - 1)) / COLS
            self.grid.col_default_width = cell_size
            self.grid.row_default_height = cell_size
            self.grid.size = (side, side)
            for c in self.cells.values():
                c.redraw()

        top_area.bind(size=resize_grid)
        Clock.schedule_once(resize_grid, 0)

        bottom_row = BoxLayout(orientation='horizontal', spacing=2, size_hint=(1, 0.2))
        with bottom_row.canvas.before:
            Color(1, 1, 1, 1)
            self.bottom_rect = Rectangle(pos=bottom_row.pos, size=bottom_row.size)
        bottom_row.bind(pos=self.update_bottom_rect, size=self.update_bottom_rect)

        left_panel = BoxLayout(orientation='vertical', size_hint_x=0.25)
        with left_panel.canvas.before:
            Color(0, 0, 0, 1)
            self._left_rect = Rectangle(pos=left_panel.pos, size=left_panel.size)
        left_panel.bind(pos=lambda i, v: setattr(self._left_rect, 'pos', i.pos),
                        size=lambda i, v: setattr(self._left_rect, 'size', i.size))
        left_panel.add_widget(Label(text='Player 1', color=TEAL, font_size=sp(22), bold=True))
        self.p1_count_label = Label(text='0', color=(1, 1, 1, 1), font_size=sp(20))
        self.p1_timer_label = Label(text='00:00', color=(1, 1, 1, 1), font_size=sp(20))
        left_panel.add_widget(self.p1_count_label)
        left_panel.add_widget(self.p1_timer_label)

        mid_panel = BoxLayout(orientation='vertical', size_hint_x=0.5)
        with mid_panel.canvas.before:
            Color(0, 0, 0, 1)
            self._mid_rect = Rectangle(pos=mid_panel.pos, size=mid_panel.size)
        mid_panel.bind(pos=lambda i, v: setattr(self._mid_rect, 'pos', i.pos),
                       size=lambda i, v: setattr(self._mid_rect, 'size', i.size))
        self.turn_label = Label(
            text=f'[b][color={TEAL_HEX}]Player 1[/color] [color=#FFFFFF]Turn[/color][/b]',
            markup=True,
            font_size=sp(28),
        )
        mid_panel.add_widget(self.turn_label)

        right_panel = BoxLayout(orientation='vertical', size_hint_x=0.25)
        with right_panel.canvas.before:
            Color(0, 0, 0, 1)
            self._right_rect = Rectangle(pos=right_panel.pos, size=right_panel.size)
        right_panel.bind(pos=lambda i, v: setattr(self._right_rect, 'pos', i.pos),
                         size=lambda i, v: setattr(self._right_rect, 'size', i.size))
        right_panel.add_widget(Label(text='Player 2', color=ORANGE, font_size=sp(22), bold=True))
        self.p2_count_label = Label(text='0', color=(1, 1, 1, 1), font_size=sp(20))
        self.p2_timer_label = Label(text='00:00', color=(1, 1, 1, 1), font_size=sp(20))
        right_panel.add_widget(self.p2_count_label)
        right_panel.add_widget(self.p2_timer_label)

        bottom_row.add_widget(left_panel)
        bottom_row.add_widget(mid_panel)
        bottom_row.add_widget(right_panel)

        root.add_widget(top_area)
        root.add_widget(bottom_row)
        self.add_widget(root)

    def handle_tap(self, row, col):
        state = self.board.get(row, col)
        if self.selected_cell and self.cells[(row, col)].highlighted:
            self.execute_move(row, col)
        elif state == self.current_player:
            if self.selected_cell == (row, col):
                self.clear_highlights()
                self.selected_cell = None
            else:
                self.clear_highlights()
                self.selected_cell = (row, col)
                self.show_moves(row, col)
        else:
            self.clear_highlights()
            self.selected_cell = None

    def execute_move(self, row, col):
        sr, sc = self.selected_cell
        dist = max(abs(row - sr), abs(col - sc))

        self.board.set(row, col, self.current_player)
        self.cells[(row, col)].set_state(self.current_player)

        if dist == 2:
            self.board.set(sr, sc, EMPTY)
            self.cells[(sr, sc)].set_state(EMPTY)

        enemy = 2 if self.current_player == 1 else 1
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.board.in_bounds(r, c) and self.board.get(r, c) == enemy:
                    self.board.set(r, c, self.current_player)
                    self.cells[(r, c)].set_state(self.current_player)

        self.clear_highlights()
        self.selected_cell = None
        self.current_player = 2 if self.current_player == 1 else 1
        self.update_counts()
        self.update_turn_label()
        if not self.game_started and self.time_limit is not None:
            self.game_started = True
            self._timer_event = Clock.schedule_interval(self.tick, 1)
        self.check_game_over()

    def update_counts(self):
        p1 = sum(self.board.get(r, c) == 1 for r in range(ROWS) for c in range(COLS))
        p2 = sum(self.board.get(r, c) == 2 for r in range(ROWS) for c in range(COLS))
        self.p1_count_label.text = str(p1)
        self.p2_count_label.text = str(p2)

    def has_moves(self, player):
        for r in range(ROWS):
            for c in range(COLS):
                if self.board.get(r, c) == player:
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if self.board.in_bounds(nr, nc) and self.board.is_empty(nr, nc):
                                return True
        return False

    def check_game_over(self):
        p1 = sum(self.board.get(r, c) == 1 for r in range(ROWS) for c in range(COLS))
        p2 = sum(self.board.get(r, c) == 2 for r in range(ROWS) for c in range(COLS))
        walls = sum(self.board.is_wall(r, c) for r in range(ROWS) for c in range(COLS))

        board_full = (p1 + p2 + walls) == ROWS * COLS
        no_pieces = p1 == 0 or p2 == 0

        if board_full or no_pieces:
            self.end_game(p1, p2)
            return

        if not self.has_moves(self.current_player):
            other = 2 if self.current_player == 1 else 1
            if self.has_moves(other):
                self.current_player = other
                self.update_turn_label()
            else:
                self.end_game(p1, p2)

    def end_game(self, p1, p2):
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None
        winner = 1 if p1 > p2 else (2 if p2 > p1 else 0)
        self.manager.get_screen('results').show_result(winner, p1, p2)
        self.manager.current = 'results'

    def update_turn_label(self):
        color_hex = TEAL_HEX if self.current_player == 1 else ORANGE_HEX
        self.turn_label.text = (
            f'[b][color={color_hex}]Player {self.current_player}[/color]'
            f' [color=#FFFFFF]Turn[/color][/b]'
        )

    def show_moves(self, row, col):
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.board.in_bounds(r, c) and self.board.is_empty(r, c):
                    self.cells[(r, c)].highlighted = True
                    self.cells[(r, c)].redraw()

    def clear_highlights(self):
        for cell in self.cells.values():
            if cell.highlighted:
                cell.highlighted = False
                cell.redraw()

    def fmt_time(self, secs):
        secs = max(0, int(secs))
        return f'{secs // 60:02d}:{secs % 60:02d}'

    def tick(self, dt):
        if self.current_player == 1:
            self.p1_time = max(0.0, self.p1_time - dt)
            self.p1_timer_label.text = self.fmt_time(self.p1_time)
            if self.p1_time <= 0:
                self.end_by_timeout()
        else:
            self.p2_time = max(0.0, self.p2_time - dt)
            self.p2_timer_label.text = self.fmt_time(self.p2_time)
            if self.p2_time <= 0:
                self.end_by_timeout()

    def end_by_timeout(self):
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None
        p1 = sum(self.board.get(r, c) == 1 for r in range(ROWS) for c in range(COLS))
        p2 = sum(self.board.get(r, c) == 2 for r in range(ROWS) for c in range(COLS))
        winner = 2 if self.current_player == 1 else 1
        self.manager.get_screen('results').show_result(winner, p1, p2, reason='timeout')
        self.manager.current = 'results'



    def load_level(self, level, time_limit=None):
        self.level = level
        self.current_player = 1
        self.selected_cell = None
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None
        self.game_started = False
        self.time_limit = time_limit
        self.p1_time = time_limit or 0
        self.p2_time = time_limit or 0
        with open(self.levels_path) as f:
            levels = json.load(f)
        self.board.load(levels[level - 1]['board'])
        for (row, col), cell in self.cells.items():
            cell.highlighted = False
            cell.set_state(self.board.get(row, col))
        self.update_counts()
        self.update_turn_label()
        if time_limit is not None:
            timer_text = f'{time_limit // 60:02d}:{time_limit % 60:02d}'
            self.p1_timer_label.text = timer_text
            self.p2_timer_label.text = timer_text
            self.p1_timer_label.opacity = 1
            self.p2_timer_label.opacity = 1
        else:
            self.p1_timer_label.opacity = 0
            self.p2_timer_label.opacity = 0

    def update_root_rect(self, instance, value):
        self.root_rect.pos = instance.pos
        self.root_rect.size = instance.size

    def update_top_rect(self, instance, value):
        self.top_rect.pos = instance.pos
        self.top_rect.size = instance.size

    def update_grid_rect(self, instance, value):
        self.grid_rect.pos = instance.pos
        self.grid_rect.size = instance.size

    def update_bottom_rect(self, instance, value):
        self.bottom_rect.pos = instance.pos
        self.bottom_rect.size = instance.size
