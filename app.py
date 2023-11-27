from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from views import LoginView


class RestaurantPointApp(MDApp):
    def build(self):
        # Create a ScreenManager with the login and role-specific screens
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginView(name='login_view'))
        Window.size = (950, 500)

        return screen_manager

    
if __name__ == '__main__':
    RestaurantPointApp().run()