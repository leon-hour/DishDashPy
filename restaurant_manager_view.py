from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
# Import the User and UserRole classes from the previous code snippet
from models import  Restaurant
# Import the UserDataProvider class from the previous code snippet
from controllers import SecurityController, RestaurantManagerController

class RestaurantManagerView(BoxLayout):
    name_input = ObjectProperty(None)
    address_input = ObjectProperty(None)
    restaurant_table = ObjectProperty(None)
    content_panel = BoxLayout()
    selected_row = -1
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self._create_restaurant_manager_input_components())
        self.add_widget(self._create_restaurant_table_panel())

    def _create_restaurant_manager_input_components(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 270
        self.name_input = MDTextField(multiline=False, size_hint=(1.1, 1.1), font_size='18sp', hint_text='Name')
        input_data_component_panel.add_widget(self.name_input)
        self.address_input = MDTextField(multiline=False, size_hint=(1.1, 1.1), font_size='18sp', hint_text='Address')
        input_data_component_panel.add_widget(self.address_input)

        buttons_component_panel = GridLayout(cols=3, padding=0, spacing=10)
        add_button = Button(text='Add', size_hint=(None, None), size=(70, 40), background_color=(0, 1, 1, 1))
        update_button = Button(text='Update', size_hint=(None, None), size=(70, 40), background_color=(0, 1, 1, 1))
        delete_button = Button(text='Delete', size_hint=(None, None), size=(70, 40), background_color=(0, 1, 1, 1))
        add_button.bind(on_press=self._add_button_function)
        delete_button.bind(on_press = self._delete_button_function)
        update_button.bind(on_press = self._update_button_function)
        buttons_component_panel.add_widget(add_button)
        buttons_component_panel.add_widget(update_button)
        buttons_component_panel.add_widget(delete_button)

        input_data_component_panel.add_widget(buttons_component_panel)

        return input_data_component_panel

    def _create_restaurant_table_panel(self):
        table_panel = GridLayout(cols = 1, padding = 10,spacing = 0)
        table_panel.size_hint_x = None
        table_panel.width = 430
        self.restaurant_table = self._create_restaurant_data_table()
        self.restaurant_table.bind(on_check_press=self._checked)
        self.restaurant_table.bind(on_row_press=self._on_row_press)
        table_panel.add_widget(self.restaurant_table)
        return table_panel

    def _create_restaurant_data_table(self):
        table_row_data = []
        restaurant_list = SecurityController.get_logged_in_user().restaurant_list
        for restaurant in restaurant_list:
             table_row_data.append((restaurant.name, restaurant.address))
        self.restaurant_table = MDDataTable(
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            check = True,
            use_pagination=True,
            rows_num = 10,
            column_data = [
                ("Name", 40),
                ("Address", 40)
            ],
            row_data = table_row_data
        )
        return self.restaurant_table

    def _checked(self, instance_table, current_row):
        selected_restaurant = Restaurant(current_row[0], current_row[1], [],[])
        self.name_input.text = str(selected_restaurant.name)
        self.address_input.text = str(selected_restaurant.address)

    def _update_data_table(self):
        table_row_data = []
        restaurants = SecurityController.get_logged_in_user().restaurant_list
        for restaurant in restaurants:
             table_row_data.append((restaurant.name, restaurant.address))
        self.restaurant_table.row_data = table_row_data
        
    
    def _add_button_function(self, instance):
        name = self.name_input.text
        address = self.address_input.text
        restaurant_data = []
        restaurant_data.append(name)
        restaurant_data.append(address)
        if self._are_data_valid(restaurant_data):
            RestaurantManagerController.add_restaurant(Restaurant(restaurant_data[0], restaurant_data[1],[],[]))
            self._update_data_table()
            self._clear_text_field_content()
        else:
            popup = Popup(title='Invalid data ', content=Label(text='Provide mandatory data to add a new restaurant'), size_hint=(None, None), size=(400, 200))
            popup.open()

    def _update_button_function(self, instance):
        if self.selected_row != -1:
            name = self.name_input.text
            address = self.address_input.text
            restaurant_data = []
            restaurant_data.append(name)
            restaurant_data.append(address)
            if self._are_data_valid(restaurant_data):
                restaurant_to_remove = self.restaurant_table.row_data[self.selected_row]
                del self.restaurant_table.row_data[self.selected_row]
                RestaurantManagerController.delete_restaurant(restaurant_to_remove[0], restaurant_to_remove[1] )
                RestaurantManagerController.add_restaurant(Restaurant(restaurant_data[0], restaurant_data[1],[],[]))
                self._update_data_table()
                self._clear_text_field_content()
            else:
                popup = Popup(title=' Invalid data ', content=Label(text='Provide mandatory data to update the restaurant'), size_hint=(None, None), size=(400, 200))
                popup.open()
        else:
            popup = Popup(title=' Invalid data', content=Label(text='Select any row to update'), size_hint=(None, None), size=(400, 200))
            popup.open()
    
    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index/2)

    def _delete_button_function(self, instance):
        if self.selected_row != -1:
            restaurant_to_remove = self.restaurant_table.row_data[self.selected_row]
            RestaurantManagerController.delete_restaurant(restaurant_to_remove[0], restaurant_to_remove[1] )
            self._update_data_table()
            self._clear_text_field_content()
        else:
            popup = Popup(title='Invalid  data', content=Label(text='Select any row to delete'), size_hint=(None, None), size=(400, 200))
            popup.open()


    def _clear_text_field_content(self):
        self.name_input.text = ""
        self.address_input.text = ""
        self.selected_row = -1
        self.restaurant_table.selected = []

    def _are_data_valid(self, restaurant_data):
        return restaurant_data[0] != "" and restaurant_data[1] != "" 