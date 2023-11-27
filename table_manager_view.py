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
from controllers import SecurityController, TableManagerController
from models import Restaurant, Table

class TableManagerView(BoxLayout):
    table_manager_controller = TableManagerController()
    id_input = ObjectProperty(None)
    seats_input = ObjectProperty(None)
    table = ObjectProperty(None)
    dropdown = ObjectProperty(None)
    restaurant = Restaurant
    selected_row = -1
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.restaurant = SecurityController.get_logged_in_user().restaurant_list[0]
        self.add_widget(self._create_table_manager_input_components())
        self.add_widget(self._create_table_management_panel())
 
    def _create_table_manager_input_components(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 270
        self.id_input = MDTextField(multiline=False, size_hint=(1.1, 1.1), font_size='18sp', hint_text=' Table Id')
        input_data_component_panel.add_widget(self.id_input)
        self.seats_input = MDTextField(multiline=False, size_hint=(1.1, 1.1), font_size='18sp', hint_text='Seats')
        input_data_component_panel.add_widget(self.seats_input)
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel

    def _create_table_management_panel(self):
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
        add_button.bind(on_press=self.add_button_function)
        delete_button.bind(on_press = self.delete_button_function)
        update_button.bind(on_press = self.update_button_function)
        buttons_component_panel.add_widget(add_button)
        buttons_component_panel.add_widget(update_button)
        buttons_component_panel.add_widget(delete_button)
        return buttons_component_panel

    def _create_table_panel(self):
        table_panel = GridLayout(cols = 1, padding = 10,spacing = 0)
        self.table = self.create_table()
        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_row_press=self.on_row_press)
        table_panel.add_widget(self.table)
        return table_panel

    def _create_restaurant_selector(self):
        button = Button(text='Select an restaurant', size_hint=(0.2, None), width=200, height=50, background_color=(0, 1, 1, 1))
        # Create button and drop-down list
        button.bind(on_release=self._show_menu)
        return button
    
    def _show_menu(self, button):
        menu_items =[]
        restaurants = SecurityController.get_logged_in_user().restaurant_list
        for restaurant in restaurants:
            menu_items.append ({"viewclass": "OneLineListItem",
                "text": restaurant.name ,"on_release": lambda r=restaurant: self.update_data_table(r)})
        self.dropdown = MDDropdownMenu(
            caller=button,
            items=menu_items,
            position="top",
            width_mult=6,
        )
        self.dropdown.open()


    def create_table(self):
        table_row_data = []
        tables = self.restaurant.table_list
        for table in tables:
            table_row_data.append((table.table_number, table.seats))
            self.table = MDDataTable(
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            check = True,
            use_pagination=True,
            rows_num = 10,
            column_data = [
                ("Table id", 30),
                ("Seats", 30)
            ],
            row_data = table_row_data
        )
        return self.table

    def checked(self, instance_table, current_row):
        self.id_input.text = str(current_row[0])
        self.seats_input.text = str(current_row[1])

    def update_data_table(self, restaurant):
        self.restaurant = restaurant
        table_row_data = []
        tables = restaurant.table_list
        for table in tables:
            table_row_data.append((table.table_number, table.seats))
        self.table.row_data =  table_row_data
        
    
    def add_button_function(self, instance):
        table_id = self.id_input.text
        seats = self.seats_input.text
        new_table_data = []
        new_table_data.append(table_id)
        new_table_data.append(seats)
        if self.are_data_valid(new_table_data):
            new_table = Table(table_id, seats)
            self.table_manager_controller.add_table(new_table, self.restaurant)
            self.table.row_data.append(new_table_data)
            self.clear_input_text_fields()
        else:
            popup = Popup(title='Invalid data ', content=Label(text='Provide mandatory data to add a new table'), size_hint=(None, None), size=(400, 200))
            popup.open()

    def update_button_function(self, instance):
        if self.selected_row != -1:
            table_id = self.id_input.text
            seats = self.seats_input.text
            new_table_data = []
            new_table_data.append(table_id)
            new_table_data.append(seats)
            if self.are_data_valid(new_table_data):
                old_product_data = self.table.row_data[self.selected_row]
                old_table = Table(old_product_data[0], old_product_data[1])
                new_table = Table(table_id, seats)
                self.table_manager_controller.update_table(old_table, new_table, self.restaurant)
                self.update_data_table(self.restaurant)
                self.clear_input_text_fields()
            else:
                popup = Popup(title=' Invalid data', content=Label(text='Provide mandatory data to update the table.'), size_hint=(None, None), size=(400, 200))
                popup.open()
        else:
            popup = Popup(title='Invalid data', content=Label(text='Select any row to update'), size_hint=(None, None), size=(400, 200))
            popup.open()

            

    
    def on_row_press(self, instance, row):
        # Set the row index to delete when a row is pressed
        self.selected_row = int(row.index/2)

    def delete_button_function(self, instance):
        table_to_delete_data = self.table.row_data[self.selected_row]
        if self.selected_row != -1:
            old_table = Table(table_to_delete_data[0], table_to_delete_data[1])
            self.table_manager_controller.delete_table(old_table, self.restaurant)
            self.update_data_table(self.restaurant)
            self.clear_input_text_fields()
        else:
            popup = Popup(title='Invalid data', content=Label(text='Select any row to delete'), size_hint=(None, None), size=(400, 200))
            popup.open()


    def clear_input_text_fields(self):
        self.id_input.text = ""
        self.seats_input.text = ""
        self.selected_row = -1
    
    def are_data_valid(self, table_data):
        return table_data[0] != "" and table_data[1] != ""