from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

from utils import CAUSES, DESCRIPTIONS
from scale_widget import ScaleWidget
from user_data import user_data

class QuestionnaireScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = GridLayout (
            cols=2,
            rows=8,
            padding=dp(20),
            spacing=dp(10)
        )
        
        total_cells = layout.cols * layout.rows
        
        self.scale_widgets = []
        self.cause_labels = []
        self.label_highlights = []
        self.focused_label_index = -1

        mouse_label = Label(
            text="[b]Mouse[/b]: Click or drag to adjust scale bar.",
            markup=True,
            font_size=sp(12),
            size_hint_y=0.2,
            size_hint_x=0.3,
            valign='bottom',
            halign='left'
        )
        mouse_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        layout.add_widget(mouse_label)

        keyboard_label = Label(
            text="[b]Keyboard[/b]: Use up/down arrow keys or tab to navigate. Use left/right arrow keys to adjust scale bar. Press enter to submit.",
            markup=True,
            font_size=sp(12),
            size_hint_y=0.2,
            size_hint_x=0.7,
            valign='bottom',
            halign='left'
        )
        keyboard_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        layout.add_widget(keyboard_label)

        for i in range((total_cells-4) // 2):
            cause_label = Label(
                text=CAUSES[i],
                font_size=sp(20),
                size_hint_x=0.3,
                halign='left',
                valign='middle'
            )
            cause_label.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
            
            with cause_label.canvas.before:
                highlight_color = Color(0.7, 0.5, 1, 0)
                highlight_rect = Rectangle(pos=cause_label.pos, size=cause_label.size)
            
            def update_highlight(label, rect, *args):
                rect.pos = label.pos
                rect.size = (label.width * 0.85, label.size[1])
            
            cause_label.bind(pos=lambda instance, value, r=highlight_rect: update_highlight(instance, r),
                           size=lambda instance, value, r=highlight_rect: update_highlight(instance, r))
            
            self.cause_labels.append(cause_label)
            self.label_highlights.append((highlight_color, highlight_rect))
            layout.add_widget(cause_label)

            scale_widget = ScaleWidget(
                description=DESCRIPTIONS[i], 
                size_hint_x=0.7,
                on_interact=self.check_all_interacted
            )
            self.scale_widgets.append(scale_widget)
            layout.add_widget(scale_widget)

        layout.add_widget(
            Label(
                text="",
                size_hint_y=0.5,
                size_hint_x=0.3
            )
        )
        
        button_container = AnchorLayout(
            size_hint_y=0.5,
            size_hint_x=0.7,
            anchor_x='right',
            anchor_y='center'
        )
        self.submit_button = Button(
            text="Submit",
            size_hint=(0.5, 1),
            disabled=True
        )
        self.submit_button.bind(on_press=self.submit)
        button_container.add_widget(self.submit_button)
        layout.add_widget(button_container)

        self.add_widget(layout)
    
    def on_enter(self):
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_touch_down=self.on_window_touch)
    
    def on_leave(self):
        Window.unbind(on_key_down=self.on_key_down)
        Window.unbind(on_touch_down=self.on_window_touch)
    
    def on_window_touch(self, instance, touch):
        self.hide_all_highlights()
        return False
    
    def hide_all_highlights(self):
        for highlight_color, _ in self.label_highlights:
            highlight_color.a = 0
        self.focused_label_index = -1
    
    def show_highlight(self, index):
        if 0 <= index < len(self.label_highlights):
            self.hide_all_highlights()
            highlight_color, _ = self.label_highlights[index]
            highlight_color.a = 0.3
            self.focused_label_index = index
    
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 82:
            if self.focused_label_index == -1:
                self.show_highlight(0)
            elif self.focused_label_index > 0:
                self.show_highlight(self.focused_label_index - 1)
            return True
        elif keycode == 81 or keycode == 43:
            if self.focused_label_index == -1:
                self.show_highlight(0)
            elif self.focused_label_index < len(self.cause_labels) - 1:
                self.show_highlight(self.focused_label_index + 1)
            return True
        elif keycode == 79:
            if self.focused_label_index >= 0:
                scale_widget = self.scale_widgets[self.focused_label_index]
                new_percent = scale_widget.current_percent + 5
                scale_widget.set_percent(new_percent)
            return True
        elif keycode == 80:
            if self.focused_label_index >= 0:
                scale_widget = self.scale_widgets[self.focused_label_index]
                new_percent = scale_widget.current_percent - 5
                scale_widget.set_percent(new_percent)
            return True
        elif keycode == 40:
            if not self.submit_button.disabled:
                self.submit()
            return True
        return False
    
    def submit(self, instance=None):
        for i, scale_widget in enumerate(self.scale_widgets):
            cause = CAUSES[i]
            percentage = scale_widget.current_percent
            user_data.add_percent(cause, percentage)
        
        self.manager.current = 'results'
    
    def check_all_interacted(self):
        all_interacted = all(widget.has_interacted for widget in self.scale_widgets)
        if all_interacted:
            self.submit_button.disabled = False
