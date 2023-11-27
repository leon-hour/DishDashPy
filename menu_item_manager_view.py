from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from controllers import SecurityController,MenuItemManagerController
from models import Restaurant, Menu, Product

class MenuItemManagerView(BoxLayout):
    menu_item_manager_controller = MenuItemManagerController()
    id_input = ObjectProperty(None)
    name_input = ObjectProperty(None)
    price_input = ObjectProperty(None)
    menu_item_table = ObjectProperty(None)
    restaurant = Restaurant
    menu = Menu
    selected_row = -1
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.restaurant = SecurityController.get_logged_in_user().restaurant_list[0]
        self.add_widget(self._create_menu_item_manager_input_components())
        self.add_widget(self._create_menu_table_panel())
 
    def _create_menu_item_manager_input_components(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 270
        self.id_input = MDTextField(multiline=False, size_hint=(1.1, 1.1), font_size='18sp', hint_text=' Menu item Id')
        input_data_component_panel.add_widget(self.id_input)
        self.name_input = MDTextField(multiline=False, size_hint=(1.1, 1.1), font_size='18sp', hint_text='Menu item name')
        input_data_component_panel.add_widget(self.name_input)
        self.price_input = MDTextField(multiline=False, size_hint=(1.1, 1.1), font_size='18sp', hint_text=' Menu item price')
        input_data_component_panel.add_widget(self.price_input)

        buttons_component_panel = GridLayout(cols=3, padding=0, spacing=10)
        add_button = Button(text='Add', size_hint=(None, None), size=(70, 40), background_color=(0, 1, 1, 1))
        update_button = Button(text='Update', size_hint=(None, None), size=(70, 40), background_color=(0, 1, 1, 1))
        delete_button = Button(text='Delete', size_hint=(None, None), size=(70, 40), background_color=(0, 1, 1, 1))
        add_button.bind(on_press = self.add_button_function)
        update_button.bind(on_press = self.update_button_function)
        delete_button.bind(on_press = self.delete_button_function)
        buttons_component_panel.add_widget(add_button)
        buttons_component_panel.add_widget(update_button)
        buttons_component_panel.add_widget(delete_button)

        input_data_component_panel.add_widget(buttons_component_panel)

        return input_data_component_panel

    def _create_menu_table_panel(self):
        content_panel = GridLayout(cols = 1, spacing = 10)
        self.restaurant = SecurityController.get_logged_in_user().restaurant_list[0]
        self.menu = self.restaurant.menu_list[0]
        restaurant_selector = self.create_restarant_selector()
        content_panel.add_widget(restaurant_selector)
        menu_selector = self.create_menu_selector()
        content_panel.add_widget(menu_selector)
        content_panel.size_hint_x = None
        content_panel.width = 400
        self.menu_item_table = self.create_table(self.menu)
        self.menu_item_table.bind(on_check_press=self.checked)
        self.menu_item_table.bind(on_row_press=self.on_row_press)
        content_panel.add_widget(self.menu_item_table)
        return content_panel

    def create_restarant_selector(self):
        select_restaurant_button = Button(text='Select a restaurant', size_hint=(0.2, None), width=200, height=50)
        select_restaurant_button.bind(on_release=self.show_restautant_list)   
        return select_restaurant_button
    
    def create_menu_selector(self):
        select_restaurant_button = Button(text='Select a menu', size_hint=(0.2, None), width=200, height=50)
        select_restaurant_button.bind(on_release=self.show_menu_list)  
        return select_restaurant_button

    def show_restautant_list(self, button):
        menu_items =[]
        restaurant_list = SecurityController.get_logged_in_user().restaurant_list
        for restaurant in restaurant_list:
            menu_items.append ({"viewclass": "OneLineListItem",
                "text": restaurant.name ,"on_release": lambda r=restaurant: self.update_menu_dropdown_list(r)})
        self.dropdown = MDDropdownMenu(
            caller=button,
            items=menu_items,
            position="top",
            width_mult=6,
        )
        self.dropdown.open()

    def show_menu_list(self, button):
        menu_items =[]
        restaurant_menu_list = self.restaurant.menu_list
        for menu in restaurant_menu_list:
            menu_items.append ({"viewclass": "OneLineListItem",
                "text": menu.menu_name ,"on_release": lambda r=menu: self.update_menu_item_table(r)})
        self.dropdown = MDDropdownMenu(
            caller=button,
            items=menu_items,
            position="top",
            width_mult=6,
        )
        self.dropdown.open()

    def update_menu_dropdown_list(self, restaurant):
        menu_items =[]
        self.restaurant = restaurant
        for menu in restaurant.menu_list:
            menu_items.append ({"viewclass": "OneLineListItem",
                "text": menu.menu_name ,"on_release": lambda r=menu: self.update_menu_item_table(r)})
        self.menu = self.restaurant.menu_list[0]
        self.update_menu_item_table(self.menu)
    
    def create_table(self, menu):
        table_row_data = []
        menu_items = menu.menu_items
        for menu_item in menu_items:
            table_row_data.append((menu_item.id, menu_item.name, menu_item.price))
            self.menu_item_table = MDDataTable(
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            check = True,
            use_pagination=True,
            rows_num = 10,
            column_data = [
                ("Product id", 30),
                ("Product name", 30),
                ("Product price", 30),
            ],
            row_data = table_row_data
        )
        return self.menu_item_table

    def checked(self, instance_table, current_row):
        self.id_input.text = str(current_row[0])
        self.name_input.text = str(current_row[1])
        self.price_input.text = str(current_row[2])

    def update_menu_item_table(self, menu):
        table_row_data = []
        menu_items = menu.menu_items
        for menu_item in menu_items:
            table_row_data.append((menu_item.id, menu_item.name, menu_item.price))
        self.menu_item_table.row_data =  table_row_data
        
    
    def add_button_function(self, instance):
        menu_item_id = self.id_input.text
        menu_item_name = self.name_input.text
        menu_item_price = self.price_input.text
        menu_item_data = []
        menu_item_data.append(menu_item_id)
        menu_item_data.append(menu_item_name)
        menu_item_data.append(menu_item_price)
        if self.are_data_valid(menu_item_data):
            menu_item_to_add = Product(menu_item_id, menu_item_name, menu_item_price)
            self.menu_item_manager_controller.add_menu_item(menu_item_to_add, self.menu)
            self.menu_item_table.row_data.append(menu_item_data)
            self.clear_input_text_fields()
        else:
            popup = Popup(title='Invalid data ', content=Label(text='Provide mandatory data to add a new menu item'), size_hint=(None, None), size=(400, 200))
            popup.open()

    def update_button_function(self, instance):
        if self.selected_row != -1:
            menu_item_id = self.id_input.text
            menu_item_name = self.name_input.text
            menu_item_price = self.price_input.text
            price = self.price_input.text
            menu_item_data = []
            menu_item_data.append(menu_item_id)
            menu_item_data.append(menu_item_name)
            menu_item_data.append(price)
            if self.are_data_valid(menu_item_data):
                old_product_data = self.menu_item_table.row_data[self.selected_row]
                old_menu_item = Product(old_product_data[0], old_product_data[1], old_product_data[2])
                new_menu_item = Product(menu_item_id, menu_item_name, menu_item_price)
                self.menu_item_manager_controller.update_menu_item(old_menu_item, new_menu_item, self.menu)
                self.update_menu_item_table(self.menu)
                self.clear_input_text_fields()
            else:
                popup = Popup(title=' Invalid data', content=Label(text='Provide mandatory data to update the menu item'), size_hint=(None, None), size=(400, 200))
                popup.open()
        else:
            popup = Popup(title='Invalid data', content=Label(text='Select any row to update'), size_hint=(None, None), size=(400, 200))
            popup.open()

            

    
    def on_row_press(self, instance, row):
        # Set the row index to delete when a row is pressed
        self.selected_row = int(row.index/3)

    def delete_button_function(self, instance):
        menu_item_to_delete_data = self.menu_item_table.row_data[self.selected_row]
        if self.selected_row != -1:
            old_menu_item = Product(menu_item_to_delete_data[0], menu_item_to_delete_data[1], menu_item_to_delete_data[2])
            self.menu_item_manager_controller.delete_menu_item(old_menu_item, self.menu)
            self.update_menu_item_table(self.menu)
            self.clear_input_text_fields()
        else:
            popup = Popup(title='Invalid data', content=Label(text='Select any row to delete'), size_hint=(None, None), size=(400, 200))
            popup.open()


    def clear_input_text_fields(self):
        self.id_input.text = ""
        self.name_input.text = ""
        self.price_input.text = ""
        self.selected_row = -1

    def are_data_valid(self, menu_item_data):
        return menu_item_data[0] != "" and menu_item_data[1] != "" and menu_item_data[2] != ""