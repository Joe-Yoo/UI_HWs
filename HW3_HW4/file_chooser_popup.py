from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.metrics import dp
import os

class FileChooserPopup(Popup):
    def __init__(self, on_file_select=None, **kwargs):
        super().__init__(**kwargs)
        self.on_file_select = on_file_select
        
        self.title = 'Choose a file'
        self.size_hint = (0.9, 0.9)
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        self.file_chooser = FileChooserListView()
        self.file_chooser.path = os.path.abspath('.')
        self.file_chooser.filters = [self.is_valid_file]
        layout.add_widget(self.file_chooser)
        
        button_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=self.dismiss)
        
        select_btn = Button(text='Select')
        select_btn.bind(on_press=self.select_file)
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(select_btn)
        
        layout.add_widget(button_layout)
        
        self.content = layout
    
    def is_valid_file(self, folder, filename):
        filepath = os.path.join(folder, filename)
        if os.path.isdir(filepath):
            return True
        return filename.endswith('.txt') or filename.endswith('.timecode')
    
    def select_file(self, instance):
        if self.file_chooser.selection:
            selected_file = self.file_chooser.selection[0]
            if self.on_file_select:
                self.on_file_select(selected_file)
            self.dismiss()
