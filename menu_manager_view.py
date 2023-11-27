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
from kivymd.uix.menu import MDDropdownMenu
from controllers import SecurityController, MenuManagerController
from models import Restaurant, Menu

class MenuManagerView(BoxLayout):
    menu_manager_controller = MenuManagerController()
    name_input = ObjectProperty(None)
    menu_table = ObjectProperty(None)
    dropdown = ObjectProperty(None)
    restaurant = Restaurant
    selected_row = -1
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.restaurant = SecurityController.get_logged_in_user().restaurant_list[0]
        self.add_widget(self._create_menu_manager_input_components())
        self.add_widget(self._create_menu_table_management_panel())
 
    def _create_menu_manager_input_components(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 270
        self.name_input = MDTextField(multiline=False, size_hint=(1.1, 1.1), font_size='18sp', hint_text=' Menu Name')
        input_data_component_panel.add_widget(self.name_input)
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel

    def _create_menu_table_management_panel(self):
        content_panel = GridLayout(cols = 1, spacing = 10)
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.size_hint_x = None
        content_panel.width = 600
        content_panel.add_widget(self._create_table_panel())
        return content_panel

    def _create_buttons_component_panel(self):
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
        return buttons_component_panel

    def _create_table_panel(self):
        table_panel = GridLayout(cols = 1, padding = 10,spacing = 0)
        self.menu_table = self._create_table()
        self.menu_table.bind(on_check_press=self._checked)
        self.menu_table.bind(on_row_press=self._on_row_press)
        table_panel.add_widget(self.menu_table)
        return table_panel

    def _create_restaurant_selector(self):
        button = Button(text='Select a restaurant', size_hint=(0.2, None), width=200, height=50, background_color=(0, 1, 1, 1))
        # Create button and drop-down list
        button.bind(on_release=self._show_menu)
        return button
    
    def _show_menu(self, button):
        menu_items =[]
        restaurants = SecurityController.get_logged_in_user().restaurant_list
        for restaurant in restaurants:
            menu_items.append ({"viewclass": "OneLineListItem",
                "text": restaurant.name ,"on_release": lambda r=restaurant: self._update_data_table(r)})
        self.dropdown = MDDropdownMenu(
            caller=button,
            items=menu_items,
            position="top",
            width_mult=6,
        )
        self.dropdown.open()


    def _create_table(self):
        table_row_data = []
        menus = self.restaurant.menu_list
        for menu in menus:
            table_row_data.append([menu.menu_name])
            self.table = MDDataTable(
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            check = True,
            use_pagination=True,
            rows_num = 10,
            column_data = [
                ("Menu name", 50)
            ],
            row_data = table_row_data
        )
        return self.table

    def _checked(self, instance_table, current_row):
        self.name_input.text = str(current_row[0])

    def _update_data_table(self, restaurant):
        self.restaurant = restaurant
        table_row_data = []
        menus = restaurant.menu_list
        for menu in menus:
            table_row_data.append(([menu.menu_name]))
        self.table.row_data =  table_row_data
        
    
    def _add_button_function(self, instance):
        menu_name = self.name_input.text
        if self._are_data_valid(menu_name):
            new_menu = Menu(menu_name, [])
            self.menu_manager_controller.add_menu(new_menu, self.restaurant)
            self.table.row_data.append([menu_name])
            self._clear_input_text_fields()
        else:
            popup = Popup(title='Invalid data ', content=Label(text='Provide mandatory data to add a new menu'), size_hint=(None, None), size=(400, 200))
            popup.open()

    def _update_button_function(self, instance):
        if self.selected_row != -1:
            new_menu_name = self.name_input.text
            if self._are_data_valid(new_menu_name):
                old_product_data = self.table.row_data[self.selected_row]
                old_menu_name = str(old_product_data[0])
                self.menu_manager_controller.update_menu(old_menu_name, new_menu_name, self.restaurant)
                self._update_data_table(self.restaurant)
                self._clear_input_text_fields()
            else:
                popup = Popup(title=' Invalid data', content=Label(text='Provide mandatory data to update the menu.'), size_hint=(None, None), size=(400, 200))
                popup.open()
        else:
            popup = Popup(title='Invalid data', content=Label(text='Select any row to update'), size_hint=(None, None), size=(400, 200))
            popup.open()

            

    
    def _on_row_press(self, instance, row):
        # Set the row index to delete when a row is pressed
        self.selected_row = int(row.index)

    def _delete_button_function(self, instance):
        menu_to_delete = self.table.row_data[self.selected_row]
        if self.selected_row != -1:
            self.menu_manager_controller.delete_menu(menu_to_delete[0], self.restaurant)
            self._update_data_table(self.restaurant)
            self._clear_input_text_fields()
        else:
            popup = Popup(title='Invalid data', content=Label(text='Select any row to delete'), size_hint=(None, None), size=(400, 200))
            popup.open()


    def _clear_input_text_fields(self):
        self.name_input.text = ""
        self.selected_row = -1
    
    def _are_data_valid(self, menu_name):
        return menu_name != ""
    