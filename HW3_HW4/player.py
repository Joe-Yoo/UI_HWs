from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Triangle, Ellipse
from file_chooser_popup import FileChooserPopup
from kivy.clock import Clock
from kivy.uix.settings import SettingsWithSidebar
from kivy.config import ConfigParser
from kivy.uix.popup import Popup
from kivy.utils import escape_markup
from kivy.graphics import Line
from kivy.uix.settings import SettingOptions

from scrollable_options import scrollable_options
import re
import os

class player(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_playing = False
        self.words = []
        self.current_word_index = 0
        self.word_event = None
        self.wpm = 450
        self.font_size = 50
        self.font_name = "Roboto"

        self.font_name = "Roboto"
        self.get_available_fonts()

        root = BoxLayout(orientation='vertical')
        with root.canvas.before:
            Color(1, 1, 1, 1)
            root.bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda instance, value: setattr(instance.bg_rect, 'pos', value))
        root.bind(size=lambda instance, value: setattr(instance.bg_rect, 'size', value))

        self.top_bar = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.25),
            padding=[dp(15), dp(15), dp(15), dp(15)]
        )
        left_btn = Button(text='Choose File', size_hint=(0.5, 1), width=100, color=(1, 1, 1, 1))
        left_btn.bind(on_press=self.open_file_chooser)
        spacer = Widget()
        right_btn = Button(text='Settings', size_hint=(0.5, 1), width=100, color=(1, 1, 1, 1))
        right_btn.bind(on_press=self.open_settings)

        self.top_bar.add_widget(left_btn)
        self.top_bar.add_widget(spacer)
        self.top_bar.add_widget(right_btn)

        top_line = Widget(size_hint=(1, None), height=dp(2))
        with top_line.canvas:
            Color(0, 0, 0, 1)
            top_line.rect = Rectangle(pos=top_line.pos, size=top_line.size)
        top_line.bind(pos=lambda instance, value: setattr(instance.rect, 'pos', value))
        top_line.bind(size=lambda instance, value: setattr(instance.rect, 'size', value))

        self.middle = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.50),
            padding=[0, 0, 0, dp(40)]
        )
        self.middle.bind(pos=self.draw_alignment_line, size=self.draw_alignment_line)

        self.word_split = BoxLayout(orientation='horizontal', size_hint=(1, 1))
        self.left_container = BoxLayout(size_hint=(0.35, 1))
        self.right_container = BoxLayout(size_hint=(0.65, 1))

        self.left_word_label = Label(
            text='',
            color=(0, 0, 0, 1),
            font_size=dp(36),
            halign='right',
            valign='bottom'
        )
        self.left_word_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))

        self.word_label = Label(
            text='',
            color=(0, 0, 0, 1),
            font_size=dp(36),
            markup=True,
            halign='left',
            valign='bottom'
        )
        self.word_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))

        self.left_container.add_widget(self.left_word_label)
        self.right_container.add_widget(self.word_label)
        self.word_split.add_widget(self.left_container)
        self.word_split.add_widget(self.right_container)
        self.middle.add_widget(self.word_split)

        bottom_line = Widget(size_hint=(1, None), height=dp(2))
        with bottom_line.canvas:
            Color(0, 0, 0, 1)
            bottom_line.rect = Rectangle(pos=bottom_line.pos, size=bottom_line.size)
        bottom_line.bind(pos=lambda instance, value: setattr(instance.rect, 'pos', value))
        bottom_line.bind(size=lambda instance, value: setattr(instance.rect, 'size', value))

        self.bottom_bar = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.25),
            padding=[dp(15), dp(15), dp(15), dp(15)]
        )

        spacer2 = Widget()
        spacer3 = Widget()
        
        self.play_btn = Button(
            size_hint=(None, None),
            size=(dp(60), dp(60)),
            background_color=(0, 0, 0, 0),
            disabled=True
        )
        self.play_btn.bind(on_press=self.on_play_press)
        self.play_btn.bind(pos=self.update_play_button)
        self.play_btn.bind(size=self.update_play_button)
        self.update_play_button(self.play_btn, None)
        
        self.bottom_bar.add_widget(spacer2)
        self.bottom_bar.add_widget(self.play_btn)
        self.bottom_bar.add_widget(spacer3)

        root.add_widget(self.top_bar)
        root.add_widget(top_line)
        root.add_widget(self.middle)
        root.add_widget(bottom_line)
        root.add_widget(self.bottom_bar)

        self.add_widget(root)

    def draw_alignment_line(self, instance, value):
        instance.canvas.after.clear()
        with instance.canvas.after:
            pad_left, _, pad_right, pad_bottom = instance.padding
            content_left = instance.x + pad_left
            content_right = instance.right - pad_right
            content_top = instance.top
            content_bottom = instance.y + pad_bottom
            marker_x = content_left + ((content_right - content_left) * 0.35) + dp(12)
            tick_len = dp(28)

            Color(0, 0, 0, 1)
            
            Line(points=[marker_x, content_top, marker_x, content_top - tick_len], width=2)
            Line(points=[marker_x, instance.y, marker_x, instance.y + tick_len], width=2)

            baseline_y = content_bottom + (self.word_label.font_size * 0.18)
            Color(0, 0, 0, 0.20)
            Line(points=[content_left + dp(12), baseline_y, content_right - dp(12), baseline_y], width=1)
    
    def update_play_button(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0, 0, 0, 1)
            center_x = instance.center_x
            center_y = instance.center_y - dp(10)
            
            if self.is_playing:
                bar_width = dp(4)
                bar_height = dp(20)
                spacing = dp(6)
                instance.pause_bar1 = Rectangle(
                    pos=(center_x - spacing/2 - bar_width, center_y - bar_height/2),
                    size=(bar_width, bar_height)
                )
                instance.pause_bar2 = Rectangle(
                    pos=(center_x + spacing/2, center_y - bar_height/2),
                    size=(bar_width, bar_height)
                )
            else:
                triangle_size = dp(20)
                instance.triangle = Triangle(points=[
                    center_x - triangle_size/3, center_y - triangle_size/2,
                    center_x - triangle_size/3, center_y + triangle_size/2,
                    center_x + triangle_size*2/3, center_y
                ])

    def get_word_interval(self, word_tuple):
        word, duration = word_tuple
        if self.use_timecodes and duration is not None:
            avg_duration = sum(d for _, d in self.words) / len(self.words)
            natural_wpm = 60.0 / avg_duration
            scale = natural_wpm / self.wpm
            scaled = duration * scale
            avg_scaled = avg_duration * scale
            dampened = avg_scaled + (scaled - avg_scaled) * 0.5
            return dampened
        else:
            char_count = len(word) if word else 1
            ratio = char_count / self.avg_word_len
            dampened = 1.0 + (ratio - 1.0) * 0.5
            return (60.0 / self.wpm) * dampened
    
    def on_play_press(self, instance):
        self.is_playing = not self.is_playing
        self.update_play_button(self.play_btn, None)
        
        if self.is_playing:
            if self.words:
                self.schedule_next_word()
        else:
            if self.word_event:
                self.word_event.cancel()
                self.word_event = None

    def schedule_next_word(self):
        interval = self.get_word_interval(self.words[self.current_word_index])
        self.word_event = Clock.schedule_once(self.update_word, interval)

    def update_word(self, dt):
        if self.words:
            self.current_word_index = (self.current_word_index + 1) % len(self.words)
            word, _ = self.words[self.current_word_index]
            left_text, right_text = self.format_word_with_focus(word)
            self.left_word_label.text = left_text
            self.word_label.text = right_text
            if self.is_playing:
                self.schedule_next_word()
    
    def open_file_chooser(self, instance):
        popup = FileChooserPopup(on_file_select=self.on_file_selected)
        popup.open()

    def apply_font_size_from_config(self):
        config = ConfigParser()
        config.read('kivy_config.ini')
        if config.has_section('reading') and config.has_option('reading', 'font_size'):
            try:
                new_font_size = config.getint('reading', 'font_size')
                if new_font_size > 0:
                    self.font_size = new_font_size
                    self.left_word_label.font_size = dp(self.font_size)
                    self.word_label.font_size = dp(self.font_size)
            except (ValueError, TypeError):
                pass

    def get_focus_index(self, word):
        positions = [i for i, c in enumerate(word) if c.isalnum()]
        if not positions:
            return 0
        n = len(positions)
        highlighted_ind = min(4, (n + 1) // 4)
        return positions[highlighted_ind]

    def format_word_with_focus(self, word):
        if not word:
            return '', ''
        highlighted_ind = self.get_focus_index(word)
        before = escape_markup(word[:highlighted_ind])
        focus = escape_markup(word[highlighted_ind])
        after = escape_markup(word[highlighted_ind + 1:])
        return before, f"[color=#cc0000]{focus}[/color]{after}"
    
    def on_file_selected(self, file_path):
        try:
            self.apply_font_size_from_config()
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            if file_path.endswith('.timecode'):
                self.words = self.parse_timecode(content)
                self.use_timecodes = True
            else:
                content = re.sub(r'\[t[\d.]+\]', '', content)
                content = re.sub('\n', ' ', content)
                raw_words = [w for w in content.split(' ') if w]
                self.avg_word_len = sum(len(w) for w in raw_words) / len(raw_words)
                self.words = [(w, None) for w in raw_words]
                self.use_timecodes = False

            self.current_word_index = 0

            if self.words:
                left_text, right_text = self.format_word_with_focus(self.words[0][0])
                self.left_word_label.text = left_text
                self.word_label.text = right_text
                self.play_btn.disabled = False
            else:
                self.left_word_label.text = ''
                self.word_label.text = ''
                self.play_btn.disabled = True

        except Exception as e:
            print(f"Error reading file: {e}")
            self.play_btn.disabled = True

    def parse_timecode(self, content):
        tokens = re.findall(r'\[t([\d.]+)\](\S+)', content)
        result = []
        for i, (timestamp, word) in enumerate(tokens):
            t = float(timestamp)
            if i + 1 < len(tokens):
                next_t = float(tokens[i + 1][0])
                duration = next_t - t
            else:
                duration = 0.5  # fallback for last word
            result.append((word, duration))
        return result

    def open_settings(self, instance):
        settings = SettingsWithSidebar()
        settings.register_type('scrollable_options', scrollable_options)

        config = ConfigParser()
        config.read('kivy_config.ini')
        config.setdefaults('reading', {
            'wpm': '450',
            'font_size': '50',
            'font': 'Roboto'
        })

        available_fonts = self.get_available_fonts()
        options_str = str(available_fonts).replace('"', '\\"')

        import json
        with open('settings.json', 'r') as f:
            settings_data = json.load(f)

        for entry in settings_data:
            if entry.get('key') == 'font':
                entry['options'] = available_fonts
                break

        settings.add_json_panel('Reading', config, data=json.dumps(settings_data))

        popup = Popup(
            title='Settings',
            content=settings,
            size_hint=(0.8, 0.8)
        )

        def on_close(*args):
            config.write()
            new_wpm = config.getint('reading', 'wpm')
            if new_wpm > 0 and new_wpm != self.wpm:
                self.wpm = new_wpm
                if self.is_playing and self.word_event:
                    self.word_event.cancel()
                    self.schedule_next_word()
            new_font_size = config.getint('reading', 'font_size')
            if new_font_size > 0 and new_font_size != self.font_size:
                self.font_size = new_font_size
                self.left_word_label.font_size = dp(self.font_size)
                self.word_label.font_size = dp(self.font_size)
            new_font = config.get('reading', 'font')
            if new_font and new_font != self.font_name:
                self.font_name = new_font
                self.left_word_label.font_name = new_font
                self.word_label.font_name = new_font
            popup.dismiss()

        settings.bind(on_close=on_close)
        popup.open()

    def get_available_fonts(self):
        from kivy.core.text import LabelBase
        fonts_dir = os.path.join(os.path.dirname(__file__), 'Fonts')
        font_names = []
        seen = set()
        if os.path.isdir(fonts_dir):
            for f in os.listdir(fonts_dir):
                if f.lower().endswith(('.ttf', '.otf')):
                    name = os.path.splitext(f)[0]
                    if name in seen:
                        continue
                    seen.add(name)
                    try:
                        LabelBase.register(name, os.path.join(fonts_dir, f))
                        font_names.append(name)
                    except Exception as e:
                        print(f"Failed to register font {name}: {e}")
        return font_names

