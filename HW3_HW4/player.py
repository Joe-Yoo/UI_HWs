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
from gestures import build_gesture_db, Gesture
from kivy.core.window import Window
from kivy.core.text import LabelBase

from scrollable_options import scrollable_options
import re
import os
import time
import vlc

class player(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gdb, self.gestures = build_gesture_db()
        Window.bind(on_key_down=self.on_key_down)
        self.is_playing = False
        self.words = []
        self.timestamps = []
        self.natural_wpm = None
        self.play_start_wall = 0
        self.play_start_ts = 0
        self.current_word_index = 0
        self.word_event = None
        self.vlc_player = None
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
        self.stats_label = Label(
            text=self.stats_text(),
            color=(0, 0, 0, 1),
            size_hint=(1, 1),
            halign='center',
            valign='middle'
        )
        self.stats_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        right_btn = Button(text='Settings', size_hint=(0.5, 1), width=100, color=(1, 1, 1, 1))
        right_btn.bind(on_press=self.open_settings)

        self.top_bar.add_widget(left_btn)
        self.top_bar.add_widget(self.stats_label)
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

    def on_touch_down(self, touch):
        touch.ud['gesture_points'] = [(touch.x, touch.y)]
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        touch.ud.setdefault('gesture_points', []).append((touch.x, touch.y))
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        points = touch.ud.get('gesture_points', [])
        if len(points) >= 5:
            g = Gesture()
            g.add_stroke(point_list=points)
            g.normalize()
            result = self.gdb.find(g, minscore=0.70)
            if result:
                score, matched = result
                self.on_gesture(matched)
        return super().on_touch_up(touch)

    def on_gesture(self, matched):
        if matched is self.gestures["swipe_left"]:
            self.jump_back()
        elif matched is self.gestures["swipe_right"]:
            self.jump_forward()
        elif matched is self.gestures["swipe_up"]:
            self.speed_up()
        elif matched is self.gestures["swipe_down"]:
            self.slow_down()
        elif matched is self.gestures["swipe_caret"]:
            self.font_bigger()
        elif matched is self.gestures["swipe_v"]:
            self.font_smaller()
        elif matched is self.gestures["swipe_greater"]:
            self.on_play_press(None)

    KEY_NAMES = {
        273: 'up',
        274: 'down',
        275: 'right',
        276: 'left',
        32: 'space',
        45: '-',
        43: '+',
        61: '+',
    }

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        name = self.KEY_NAMES.get(key)
        if name == 'left': 
            self.jump_back()
        elif name == 'right': 
            self.jump_forward()
        elif name == 'up': 
            self.speed_up()
        elif name == 'down': 
            self.slow_down()
        elif name == '+': 
            self.font_bigger()
        elif name == '-': 
            self.font_smaller()
        elif name == 'space': 
            self.on_play_press(None)

    def words_for_seconds(self, seconds):
        if self.use_timecodes:
            elapsed = 0
            count = 0
            i = self.current_word_index
            while elapsed < seconds and count < len(self.words):
                _, duration = self.words[i % len(self.words)]
                elapsed += duration if duration is not None else (60.0 / self.wpm)
                count += 1
                i += 1
            return count
        else:
            return max(1, round(seconds * self.wpm / 60))

    def seek_audio(self):
        if self.vlc_player and self.timestamps:
            self.vlc_player.set_time(int(self.timestamps[self.current_word_index] * 1000))

    def jump_back(self):
        if not self.words:
            return
        n = self.words_for_seconds(3)
        self.current_word_index = max(0, self.current_word_index - n)
        word, _ = self.words[self.current_word_index]
        left, right = self.format_word_with_focus(word)
        self.left_word_label.text = left
        self.word_label.text = right
        self.seek_audio()
        if self.is_playing:
            if self.word_event:
                self.word_event.cancel()
            self.reanchor()
            self.schedule_next_word()

    def jump_forward(self):
        if not self.words:
            return
        n = self.words_for_seconds(3)
        self.current_word_index = min(len(self.words) - 1, self.current_word_index + n)
        word, _ = self.words[self.current_word_index]
        left, right = self.format_word_with_focus(word)
        self.left_word_label.text = left
        self.word_label.text = right
        self.seek_audio()
        if self.is_playing:
            if self.word_event:
                self.word_event.cancel()
            self.reanchor()
            self.schedule_next_word()

    def stats_text(self):
        return f"{self.wpm} WPM\nFont {self.font_size}"

    def refresh_stats(self):
        self.stats_label.text = self.stats_text()

    def save_wpm(self):
        config = ConfigParser()
        config.read('kivy_config.ini')
        config.set('reading', 'wpm', str(self.wpm))
        config.write()

    def set_audio_rate(self):
        if self.vlc_player and self.natural_wpm:
            self.vlc_player.set_rate(self.wpm / self.natural_wpm)

    def speed_up(self):
        self.wpm += 50
        self.save_wpm()
        self.refresh_stats()
        self.set_audio_rate()
        if self.is_playing and self.word_event:
            self.word_event.cancel()
            self.reanchor()
            self.schedule_next_word()

    def slow_down(self):
        self.wpm = max(50, self.wpm - 50)
        self.save_wpm()
        self.refresh_stats()
        self.set_audio_rate()
        if self.is_playing and self.word_event:
            self.word_event.cancel()
            self.reanchor()
            self.schedule_next_word()

    def apply_font_size(self):
        self.left_word_label.font_size = dp(self.font_size)
        self.word_label.font_size = dp(self.font_size)
        config = ConfigParser()
        config.read('kivy_config.ini')
        config.set('reading', 'font_size', str(self.font_size))
        config.write()

    def font_bigger(self):
        self.font_size += 8
        self.apply_font_size()
        self.refresh_stats()

    def font_smaller(self):
        self.font_size = max(8, self.font_size - 8)
        self.apply_font_size()
        self.refresh_stats()

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
    
    def reanchor(self):
        self.play_start_wall = time.monotonic()
        self.play_start_ts = self.timestamps[self.current_word_index] if self.timestamps else 0

    def on_play_press(self, instance):
        self.is_playing = not self.is_playing
        self.update_play_button(self.play_btn, None)

        if self.is_playing:
            if self.current_word_index >= len(self.words) - 1:
                self.current_word_index = 0
                if self.vlc_player:
                    self.vlc_player.set_time(0)
            if self.words:
                self.reanchor()
                self.schedule_next_word()
            if self.vlc_player:
                self.vlc_player.play()
        else:
            if self.word_event:
                self.word_event.cancel()
                self.word_event = None
            if self.vlc_player:
                self.vlc_player.pause()

    def schedule_next_word(self):
        if self.use_timecodes and self.timestamps and self.natural_wpm:
            next_idx = (self.current_word_index + 1) % len(self.words)
            scale = self.natural_wpm / self.wpm
            target = self.play_start_wall + (self.timestamps[next_idx] - self.play_start_ts) * scale
            delay = max(0, target - time.monotonic())
        else:
            delay = self.get_word_interval(self.words[self.current_word_index])
        self.word_event = Clock.schedule_once(self.update_word, delay)

    def update_word(self, dt):
        if self.words:
            self.current_word_index += 1
            if self.current_word_index >= len(self.words):
                self.current_word_index = len(self.words) - 1
                self.is_playing = False
                self.word_event = None
                self.update_play_button(self.play_btn, None)
                if self.vlc_player:
                    self.vlc_player.pause()
                return
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
                wav_path = os.path.splitext(file_path)[0] + '.wav'
                if os.path.exists(wav_path):
                    if self.vlc_player:
                        self.vlc_player.stop()
                    self.vlc_player = vlc.MediaPlayer(wav_path)
                    self.set_audio_rate()
                else:
                    self.vlc_player = None
            else:
                if self.vlc_player:
                    self.vlc_player.stop()
                    self.vlc_player = None
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
        self.timestamps = []
        for i, (timestamp, word) in enumerate(tokens):
            t = float(timestamp)
            self.timestamps.append(t)
            if i + 1 < len(tokens):
                duration = float(tokens[i + 1][0]) - t
            else:
                duration = 0.5
            result.append((word, duration))
        if result:
            avg_duration = sum(d for _, d in result) / len(result)
            self.natural_wpm = 60.0 / avg_duration
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

