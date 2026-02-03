from kivy.config import Config

def config_kivy(enable_simulation=False):

    if enable_simulation:
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    else:
        Config.set('input', 'mouse', 'mouse,disable_multitouch')
        Config.set('graphics', 'show_cursor', '1')
        
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '500')