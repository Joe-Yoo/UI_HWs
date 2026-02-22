from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.metrics import dp, sp
from kivy.graphics import Line, Color, Rectangle


class ScaleWidget(Widget):
    def __init__(self, description="", on_interact=None, **kwargs):
        super().__init__(**kwargs)
        self.description = description
        self.current_percent = 0 
        self.has_interacted = False
        self.on_interact = on_interact
        
        with self.canvas:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = Rectangle()
        
        with self.canvas.after:
            Color(1, 1, 1, 1)
            self.baseline = Line(width=dp(1))
            self.ticks = []
            for i in range(21):
                tick = Line(width=dp(1))
                self.ticks.append(tick)
        
        self.label = Label(
            text=self.description,
            font_size=sp(12),
            size_hint=(1, None),
            height=dp(50),
            halign='left',
            valign='bottom'
        )
        self.label.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
        self.add_widget(self.label)
        
        self.percent_label = Label(
            text="",
            font_size=sp(12),
            size_hint=(None, None),
            width=dp(60),
            height=dp(30),
            halign='right',
            valign='middle'
        )
        self.percent_label.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
        self.add_widget(self.percent_label)
        
        self.low_label = Label(
            text="Very Low",
            font_size=sp(12),
            size_hint=(None, None),
            width=dp(80),
            height=dp(30),
            halign='left',
            valign='top'
        )
        self.low_label.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
        self.add_widget(self.low_label)
        
        self.high_label = Label(
            text="Very High",
            font_size=sp(12),
            size_hint=(None, None),
            width=dp(80),
            height=dp(30),
            halign='right',
            valign='top'
        )
        self.high_label.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
        self.add_widget(self.high_label)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        rect_height = self.height / 3
        rect_y = self.y + self.height / 3
        
        rect_width = (self.current_percent / 100) * self.width
        self.rect.pos = (self.x, rect_y)
        self.rect.size = (rect_width, rect_height)
        
        self.baseline.points = [self.x, rect_y, self.right, rect_y]
        
        tick_height = rect_height
        
        for i, tick in enumerate(self.ticks):
            x_pos = self.x + (self.width * i / 20)
            if i == 0 or i == 10 or i == 20:
                tick.points = [x_pos, rect_y + tick_height, x_pos, rect_y]
            else:
                tick.points = [x_pos, rect_y + tick_height / 2, x_pos, rect_y]
        
        # Position the question text at the TOP of the widget
        label_height = self.height / 3 - dp(5)
        self.label.height = label_height
        self.label.pos = (self.x, self.y + 2 * self.height / 3 + dp(5))
        self.label.width = self.width
        
        # Position percentage label next to the scale bar
        self.percent_label.height = rect_height
        self.percent_label.pos = (self.x - dp(65), rect_y)
        
        # Position "Very Low" and "Very High" labels at the BOTTOM
        bottom_label_height = self.height / 3 - dp(5) 
        bottom_y = self.y
        
        self.low_label.height = bottom_label_height
        self.low_label.width = self.width / 2
        self.low_label.pos = (self.x, bottom_y)
        
        self.high_label.height = bottom_label_height  
        self.high_label.width = self.width / 2
        self.high_label.pos = (self.x + self.width / 2, bottom_y)
    
    def set_percent(self, percent):
        percent = round(percent)
        percent = max(0, min(100, percent))
        self.current_percent = percent
        
        if not self.has_interacted:
            self.has_interacted = True
            if self.on_interact:
                self.on_interact()
        
        self.update_rect()
        self.percent_label.text = f"{percent}%"
    
    def update_position(self, touch):
        relative_x = touch.x - self.x
        percent = (relative_x / self.width) * 100
        self.set_percent(percent)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.update_position(touch)
            return True
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.update_position(touch)
            return True
        return super().on_touch_move(touch)
