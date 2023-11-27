from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from data_providers import UserDataProvider
from controllers import SecurityController
from managers import  UserFeatureLabelResolver, AuthorizationService, UserFeatures

import sys
sys.path.append('C:/Users/User/Documents/internship_python/restaurantpoint-reference-app')

from admin_view import restaurant_manager_view, menu_manager_view, menu_item_manager_view, table_manager_view
from cook_view import order_status_view
from waiter_view import table_orders_view
# Import the UserDataProvider class from the previous code snippet


class LoginView(Screen):
    # Create ObjectProperty for the username and password inputs
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoginView, self).__init__(**kwargs)
        self.add_widget(self._create_login_components())

    def _create_login_components(self):
        # Create an instance of the UserDataProvider
        self.user_data_provider = UserDataProvider()
        layout = GridLayout(cols=1, padding=120, spacing=20)
        self._create_username_component()
        layout.add_widget(self.username_input)
        self._create_password_components()
        layout.add_widget(self.password_input)
        layout.add_widget(self._create_show_password_component())
        layout.add_widget(self.show_password_checkbox)
        layout.add_widget(self._create_log_in_button())
        layout.add_widget(self._create_forgot_password_component())

        return layout
    def _create_username_component(self):
        self.username_input = MDTextField(multiline=False, size_hint=(1.1, 1.1), font_size='18sp', hint_text='Username')

    def _create_password_components(self):
        self.password_input = MDTextField(password=True, multiline=False, size_hint=(1.1, 1.1), size=(100,50), font_size='18sp', hint_text='Password', radius=[20,20,20,20])
        self.password_input.bind(on_text_validate=lambda instance: self.login_with_provided_user_credentials())
    
    def _create_show_password_component(self):
        show_password_lable = MDLabel(text='Show Password:', font_size='20sp')
        self.show_password_checkbox = CheckBox(active=False, size_hint=(None, None), size=(30, 30), color=(0,0,0,1))#CheckBox(active=False, color=(0,0,0,1))
        self.show_password_checkbox.bind(active=self.on_checkbox_active)
        return show_password_lable

    def _create_log_in_button(self):
        button = Button(text='Log In', size_hint=(None, None), size=(100, 50), background_color=(0, 0.7, 0.9, 1))
        button.bind(on_press=lambda instance: self.login_with_provided_user_credentials())
        return button

    def _create_forgot_password_component(self):
        forgot_password_label = MDLabel(text="[ref=contact_support]Forgot Password?[/ref]", markup=True, size_hint=(1.1, 1.1) )
        forgot_password_label.bind(on_ref_press=self.forgot_password)
        return forgot_password_label
    
    def on_checkbox_active(self, checkbox, value):
        # Toggle the password visibility based on the checkbox state
        if value:
            self.password_input.password = False
        else:
            self.password_input.password = True


    def forgot_password(self, *args):
        popup = Popup(title='Forgot password?', content=Label(text='Please contact support'), size_hint=(None, None), size=(400, 200))
        popup.open()

    def login_with_provided_user_credentials(self):
        # Get the input values from the username and password inputs
        username = self.username_input.text
        password = self.password_input.text

        # Check if the input values match any of the users in the user_data_provider
        if(self.is_credentials_provided(username, password)):
            SecurityController.login_user(self,username, password)
            user = SecurityController.get_logged_in_user()
            if(user == None):
                popup = Popup(title='Log in failed', content=Label(text='Invalid username or password.'),
                                size_hint=(None, None), size=(400, 200))
                self.username_input._delete_line(0)
                self.password_input._delete_line(0)
                popup.open()
            else:
                navigation_bar_content = UserRoleView()
                self.add_widget(navigation_bar_content)
                

    def is_credentials_provided(self, username, password):
        if SecurityController.is_string_null_or_blank(username):
            popup = Popup(title='Log in failed ', content=Label(text='Please provide your username.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return False
        elif SecurityController.is_string_null_or_blank(password):
            popup = Popup(title='Log in failed ', content=Label(text='Please provide your password.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return False
        return True

class NavigationBarBuilder(GridLayout):
    def __init__(self, user_role_view, **kwargs):
        self.user_role_view = user_role_view
        super().__init__(**kwargs)
        self.add_widget(self.create_navigation_bar_components())

    def create_navigation_bar_components(self):
        navigation_bar_panel = GridLayout(cols=1, spacing=20, size_hint=(None, None), size=(250, 500))
        with navigation_bar_panel.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # set the background color
            self.rect1 = Rectangle(size=navigation_bar_panel.size, pos=navigation_bar_panel.pos)
        navigation_bar_panel.size_hint_x = None
        navigation_bar_panel.width = 250
        navigation_bar_panel.bind(size=self._update_rect, pos=self._update_rect)
        button_list = self.create_navigation_bar_items()
        for button in button_list:
            navigation_bar_panel.add_widget(button)
        return navigation_bar_panel
    
    def create_navigation_bar_items(self):
        self.button_list = []
        user_role = SecurityController.get_logged_in_user().user_role
        authorization_service = AuthorizationService()
        self.user_features = authorization_service.get_user_feature_by_user_role(user_role)

        for feature in self.user_features:
            button = Button(text=UserFeatureLabelResolver.get_user_feature_label(feature),
                            background_color=(0.2, 0.6, 0.9, 1),
                            color=(1, 1, 1, 1),
                            font_size=18,
                            size_hint=(1, None),
                            padding = (5, 5))
            button.size = (250, 60)
            button.feature = feature  # store feature in button for later use
            button.bind(on_press=self.user_role_view._change_content_panel)
            self.button_list.append(button)
        return self.button_list


    def _update_rect(self, instance, value):
        self.rect1.pos = instance.pos
        self.rect1.size = instance.size 

class UserRoleView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (950, 500)
        self.add_widget(NavigationBarBuilder(user_role_view=self))
        self.add_widget(self._create_content_panel())

    def _create_content_panel(self):
        self.content_panel = GridLayout(cols=1, spacing=20)
        with self.content_panel.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # set the background color
            self.rect2 = Rectangle(size=self.content_panel.size, pos=self.content_panel.pos)
        self.content_panel.size_hint_x = None
        self.content_panel.width = 700
        self.content_panel.bind(size=self._update_rect, pos=self._update_rect)
        self.content_panel_content = Label(text="WELCOME!", size_hint=(1, 1), color=(0, 0, 0, 1))
        self.content_panel.add_widget(self.content_panel_content)
        return self.content_panel

    def _update_rect(self, instance, value):
        self.rect2.pos = instance.pos
        self.rect2.size = instance.size


    def _change_content_panel(self, instance):
        if instance.feature == UserFeatures.RESTAURANT_MANAGER:
            self.content_panel.clear_widgets()
            self.content_panel.add_widget(restaurant_manager_view.RestaurantManagerView())

        if instance.feature == UserFeatures.MENU_MANAGER:
            self.content_panel.clear_widgets()
            self.content_panel.add_widget(menu_manager_view.MenuManagerView())

        if instance.feature == UserFeatures.MENU_ITEM_MANAGER:
            self.content_panel.clear_widgets()
            self.content_panel.add_widget(menu_item_manager_view.MenuItemManagerView())

        if instance.feature == UserFeatures.TABLE_MANAGER:
            self.content_panel.clear_widgets()
            self.content_panel.add_widget(table_manager_view.TableManagerView())


        if instance.feature == UserFeatures.TABLE_ORDERS:
            self.content_panel.clear_widgets()
            self.content_panel.add_widget(table_orders_view.TableOrdersView())

        if instance.feature == UserFeatures.ORDER_STATUS:
            self.content_panel.clear_widgets()
            self.content_panel.add_widget(order_status_view.OrderStatusView())

        if instance.feature == UserFeatures.SIGN_OUT:
            self.content_panel.clear_widgets()
            sign_out_panel = BoxLayout(orientation='vertical', padding=100, spacing=100)
            sign_out_panel.add_widget(MDLabel(text='Are you sure you want to sign out?', halign='center', font_style='H6'))
            button_box = BoxLayout(spacing=10, size_hint=(0.5, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.5})
            confirm_button = Button(text='Sign out', size=(50, 40), background_color=(1, 0, 0, 1))
            confirm_button.bind(on_press=lambda instance: SecurityController().sign_out(self.content_panel.parent.parent))
            button_box.add_widget(confirm_button)
            sign_out_panel.add_widget(button_box)
            self.content_panel.add_widget(sign_out_panel)



class UserRoleScreen(Screen):

    def __init__(self, **kwargs):
        super(UserRoleScreen, self).__init__(**kwargs)
        two_panel_layout = UserRoleView()
        self.add_widget(two_panel_layout)

        # Set the window size
        self.size_hint = (None, None)  # Disable automatic size calculation
        self.size = (6000, 4000)  # Set the window size
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Center the window
