import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '500')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        self.cols = 1
        self.spacing = dp(5)
        self.padding = dp(10)
        
        self.name_widget = self.createNameInput()
        self.age_widget = self.createAgeInput()
        self.gender_widget = self.createGenderInput()
        self.phone_widget = self.createPhoneInput()
        self.button_widget = self.createSubmitCancelButton()
        
        self.add_widget(self.name_widget)
        self.add_widget(self.age_widget)
        self.add_widget(self.gender_widget)
        self.add_widget(self.phone_widget)
        self.add_widget(self.button_widget)

        self.first_last_valid = False
        self.age_valid = False
        self.gender_valid = False
        self.phone_number_valid = False
        
    def update_rect(self, instance, value):
        """Update rectangle size and position when widget changes"""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    # color = (#, #, #, #) tuple
    def initGridWidget(self, columns, label, color=None, label_size_hint_x=None):
        widget = GridLayout()

        widget.cols = columns
        widget.spacing = dp(10)
        widget.padding = dp(20)

        if color is not None:
            with widget.canvas.before:
                Color(color)  
                widget.rect = Rectangle(size=widget.size, pos=widget.pos)
            widget.bind(size=self.update_rect, pos=self.update_rect)

        text_label = Label(
            text=label,
            font_size=dp(16),
            size_hint_y=1,
            size_hint_x=label_size_hint_x,
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        widget.add_widget(text_label)

        return widget
        

    def createNameInput(self):
        widget = self.initGridWidget(3, 'Name')
        
        widget.firstName = TextInput(
            hint_text='First Name',
            multiline=False,
            font_size=dp(14),
            size_hint_y=1
        )
        widget.firstName.bind(text=self.on_name_text_change)
        widget.add_widget(widget.firstName)
        
        widget.lastName = TextInput(
            hint_text='Last Name',
            multiline=False,
            font_size=dp(14),
            size_hint_y=1
        )
        widget.lastName.bind(text=self.on_name_text_change)
        widget.add_widget(widget.lastName)

        return widget
    
    def createPhoneInput(self):
        widget = self.initGridWidget(2, 'Phone Number', label_size_hint_x=0.33)
        
        widget.phone = TextInput(
            hint_text='(###) ###-####',
            multiline=False,
            font_size=dp(14),
            size_hint_x=0.67,
            size_hint_y=1
        )
        widget.phone.bind(text=self.on_phone_change)
        widget.add_widget(widget.phone)
        
        return widget
    
    def createAgeInput(self):
        widget = self.initGridWidget(2, 'Age', label_size_hint_x=0.33)

        widget.age_spinner = Spinner(
            text='Select Age Range',
            values=('Under 18','18-25','25-50','50+'),
            font_size=dp(14),
            size_hint_x=0.67,
            size_hint_y=1
        )
        widget.age_spinner.bind(text=self.on_age_change)
        widget.add_widget(widget.age_spinner)
        
        return widget
    

    def createGenderInput(self):
        widget = self.initGridWidget(3, 'Gender')
        widget.size_hint_y = 2
        
        checkbox_container = GridLayout()
        checkbox_container.cols = 1
        checkbox_container.spacing = dp(8)
        checkbox_container.size_hint_x = 0.67
        checkbox_container.size_hint_y = 1
        
        male_layout = GridLayout(cols=2, size_hint_y=1)
        widget.male_checkbox = CheckBox(
            size_hint_x=0.2,
            size_hint_y=1
        )
        widget.male_checkbox.bind(active=self.on_gender_change)
        male_label = Label(
            text='Male',
            font_size=dp(14),
            size_hint_x=0.8,
            size_hint_y=1,
            text_size=(None, None),
            halign='left'
        )
        male_layout.add_widget(widget.male_checkbox)
        male_layout.add_widget(male_label)
        
        female_layout = GridLayout(cols=2, size_hint_y=1)
        widget.female_checkbox = CheckBox(
            size_hint_x=0.2,
            size_hint_y=1
        )
        widget.female_checkbox.bind(active=self.on_gender_change)
        female_label = Label(
            text='Female',
            font_size=dp(14),
            size_hint_x=0.8,
            size_hint_y=1,
            text_size=(None, None),
            halign='left'
        )
        female_layout.add_widget(widget.female_checkbox)
        female_layout.add_widget(female_label)
        
        other_layout = GridLayout(cols=2, size_hint_y=1)
        widget.other_checkbox = CheckBox(
            size_hint_x=0.2,
            size_hint_y=1
        )
        widget.other_checkbox.bind(active=self.on_gender_change)
        other_label = Label(
            text='Other/Prefer not to say',
            font_size=dp(14),
            size_hint_x=0.8,
            size_hint_y=1,
            text_size=(None, None),
            halign='left'
        )
        other_layout.add_widget(widget.other_checkbox)
        other_layout.add_widget(other_label)

        checkbox_container.add_widget(male_layout)
        checkbox_container.add_widget(female_layout)
        checkbox_container.add_widget(other_layout)
        
        widget.add_widget(checkbox_container)
        
        return widget
    
    def createSubmitCancelButton(self):
        widget = GridLayout()
        
        widget.cols = 2
        widget.spacing = dp(10)
        widget.padding = dp(20)
        widget.size_hint_y = None

        widget.submit_button = Button(
            text='Submit',
            font_size=dp(16),
            size_hint_x=0.5,
            size_hint_y=1,
            disabled=True  # Start disabled, will be updated dynamically
        )
        widget.submit_button.bind(on_press=self.on_submit_pressed)
        widget.add_widget(widget.submit_button)
        
        widget.cancel_button = Button(
            text='Cancel',
            font_size=dp(16),
            size_hint_x=0.5,
            size_hint_y=1
        )
        widget.cancel_button.bind(on_press=self.on_cancel_pressed)
        widget.add_widget(widget.cancel_button)
        
        return widget
    
    def update_submit_button(self):
        all_valid = (self.first_last_valid and self.age_valid and self.gender_valid and self.phone_number_valid)
        self.button_widget.submit_button.disabled = not all_valid
    
    def on_name_text_change(self, instance, text):
        valid_chars = ''.join(c for c in text if c.isalpha() or c in [' ', '-', "'", '.'])
        if valid_chars != text:
            instance.text = valid_chars
            return
        
        first_name = self.name_widget.firstName.text.strip()
        last_name = self.name_widget.lastName.text.strip()
        
        first_valid = (len(first_name) > 0 and all(c.isalpha() or c in [' ', '-', "'", '.'] for c in first_name))
        last_valid = (len(last_name) > 0 and all(c.isalpha() or c in [' ', '-', "'", '.'] for c in last_name))
        
        self.first_last_valid = first_valid and last_valid
        self.update_submit_button()

    def on_age_change(self, instance, text):
        self.age_valid = text != 'Select Age Range' and text in ('Under 18', '18-25', '25-50', '50+')
        self.update_submit_button()

    def on_gender_change(self, instance, active):
        male_checked = self.gender_widget.male_checkbox.active
        female_checked = self.gender_widget.female_checkbox.active
        other_checked = self.gender_widget.other_checkbox.active
        
        self.gender_valid = male_checked or female_checked or other_checked
        self.update_submit_button()

    def on_phone_change(self, instance, text):
        digits_only = ''.join(c for c in text if c.isdigit())
        if digits_only != text:
            instance.text = digits_only
            return
        
        self.phone_number_valid = len(digits_only) == 10
        self.update_submit_button()

    def on_submit_pressed(self, instance):
        first_name = self.name_widget.firstName.text
        last_name = self.name_widget.lastName.text
        phone = self.phone_widget.phone.text
        age = self.age_widget.age_spinner.text
        
        selected_genders = []
        if self.gender_widget.male_checkbox.active:
            selected_genders.append("Male")
        if self.gender_widget.female_checkbox.active:
            selected_genders.append("Female")
        if self.gender_widget.other_checkbox.active:
            selected_genders.append("Other/Prefer not to say")
        
        # Print collected data
        print(f"Name: {first_name} {last_name}")
        print(f"Phone: {phone}")
        print(f"Age: {age}")
        print(f"Gender(s): {', '.join(selected_genders) if selected_genders else 'None selected'}")

    def on_cancel_pressed(self, instance):
        App.get_running_app().stop()

class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()