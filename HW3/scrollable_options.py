from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import SettingOptions
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

class scrollable_options(SettingOptions):
    def _create_popup(self, instance):
        super()._create_popup(instance)
        # Replace the content with a scrollable version
        content = self.popup.content
        self.popup.dismiss()

        layout = BoxLayout(orientation='vertical', spacing='5dp', size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        from kivy.uix.togglebutton import ToggleButton
        for option in self.options:
            btn = ToggleButton(
                text=option,
                state='down' if option == self.value else 'normal',
                group='options',
                size_hint_y=None,
                height=dp(44)
            )
            btn.bind(on_press=lambda x: (setattr(self, 'value', x.text), self.popup.dismiss()))
            layout.add_widget(btn)

        scroll = ScrollView()
        scroll.add_widget(layout)

        from kivy.uix.popup import Popup
        self.popup = Popup(
            title=self.title,
            content=scroll,
            size_hint=(0.8, 0.6)
        )
        self.popup.open()