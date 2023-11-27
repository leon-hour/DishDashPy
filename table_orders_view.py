from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from controllers import SecurityController
from models import Restaurant, Menu

class TableOrdersView(BoxLayout):
    menu_item_table = ObjectProperty(None)
    orders_table = ObjectProperty(None)
    restaurant = Restaurant
    menu = Menu
    selected_row = -1
    orders_data = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.restaurant = SecurityController.get_logged_in_user().restaurant_list[0]
        self.add_widget(self._create_table_orders_table())
        self.add_widget(self._create_table_orders_overview())

    def _create_table_orders_table(self):
        content_panel = GridLayout(cols = 1, spacing = 20)
        self.restaurant = SecurityController.get_logged_in_user().restaurant_list[0]
        self.menu = self.restaurant.menu_list[0]
        menu_selector = self.create_menu_selector()
        content_panel.add_widget(menu_selector)
        content_panel.size_hint_x = None
        content_panel.width = 320
        self.menu_item_table = self.create_table(self.menu)
        self.menu_item_table.bind(on_row_press=self.on_row_press)
        content_panel.add_widget(self.menu_item_table)

        buttons_component_panel = GridLayout(cols=3, padding=10, spacing=10, size_hint=(0.1, None))
        add_button = Button(text='Add', size_hint=(None, None), size=(70, 40), background_color=(0, 1, 1, 1))
        delete_button = Button(text='Delete', size_hint=(None, None), size=(70, 40), background_color=(0, 1, 1, 1))
        print_invoice_button = Button(text='Print invoice', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        add_button.bind(on_press = self.add_button_function)
        delete_button.bind(on_press = self.delete_button_function)
        print_invoice_button.bind(on_press=self.print_invoice_popup)
        buttons_component_panel.add_widget(add_button)
        buttons_component_panel.add_widget(delete_button)
        buttons_component_panel.add_widget(print_invoice_button)
        content_panel.add_widget(buttons_component_panel)
        return content_panel
    
    def _create_table_orders_overview(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.size_hint_x = None
        content_panel.width = 370

        label = MDLabel(text="Orders Overview", size_hint=(1, 0.2), font_style="Subtitle1", halign="center", pos_hint={"center_x": 0.5})
        content_panel.add_widget(label)

        self.orders_table = self.create_orders_table()
        content_panel.add_widget(self.orders_table)

        # Add a new label widget to show the total price
        self.total_price_label = MDLabel(text=f"Total price: $0.00", size_hint=(1, 0.3), font_style="Subtitle2", bold=True, halign="center", pos_hint={"center_x": 0.5})
        content_panel.add_widget(self.total_price_label)

        buttons_component_panel = GridLayout(cols=3, padding=10, spacing=10, size_hint=(0.1, None))
        order_button = Button(text='Order', size_hint=(None, None), size=(70, 40), background_color=(0, 1, 1, 1))
        buttons_component_panel.add_widget(order_button)

        content_panel.add_widget(buttons_component_panel)


        self.update_total_price_label()

        return content_panel

    def update_total_price_label(self):
        sub_total = sum(order[3] for order in self.orders_data)
        vat = sub_total * 0.18
        total_price = sub_total + vat
        self.total_price_label.text = f"Subtotal: ${sub_total:.2f}\nVAT: ${vat:.2f}\nTotal price: ${total_price:.2f}"

    
    def create_menu_selector(self):
        select_restaurant_button = Button(text='Select a menu', size_hint=(0.2, None), width=200, height=50)
        select_restaurant_button.bind(on_release=self.show_menu_list)  
        return select_restaurant_button
    
    def show_menu_list(self, button):
        menu_items =[]
        restaurant_menu_list = self.restaurant.menu_list
        for menu in restaurant_menu_list:
            menu_items.append({"viewclass": "OneLineListItem",
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
            table_row_data.append((menu_item.name, menu_item.price))
            self.menu_item_table = MDDataTable(
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            check = True,
            use_pagination=True,
            rows_num = 10,
            column_data = [
                ("Name", 30),
                ("Price", 30),
            ],
            row_data = table_row_data
        )
        return self.menu_item_table
    
    def create_orders_table(self):
        table = MDDataTable(
            use_pagination=True,
            rows_num = 10,
            check=True,
            column_data=[
                ("Name", dp(30)),
                ("Price", dp(30)),
                ("Quantity", dp(30)),
                ("Total", dp(30))
            ],
            row_data=self.orders_data,)
        return table


    def update_menu_item_table(self, menu):
        table_row_data = []
        menu_items = menu.menu_items
        for menu_item in menu_items:
            table_row_data.append((menu_item.name, menu_item.price))
        self.menu_item_table.row_data =  table_row_data
        self.menu = menu

    def on_row_press(self, instance, row):
        self.selected_row = int(row.index/2)

    def update_orders_table(self):
        self.orders_table.row_data = self.orders_data
  

    def add_button_function(self, button):
        if self.selected_row != -1:
            selected_menu_item = self.menu.menu_items[self.selected_row]
            item_name = selected_menu_item.name
            item_price = selected_menu_item.price
            item_quantity = 1
            item_total_price = item_price

            # Check if the same item is already present
            for order_data in self.orders_data:
                if order_data[0] == item_name:
                    item_quantity += order_data[2]
                    item_total_price += order_data[3]
                    self.orders_data.remove(order_data)
                    break

            # Add the item to the orders overview table
            order_data = [item_name, item_price, item_quantity, item_total_price]
            self.orders_data.append(order_data)

            self.update_orders_table()
            self.update_total_price_label()
            self.selected_row = -1

    def delete_button_function(self, instance):
        if self.selected_row == -1:
            return

        # Remove selected row from orders data
        if len(self.orders_data) > self.selected_row:
            item = self.orders_data[self.selected_row]
            if item[2] > 1:
                item[2] -= 1
                item[3] = item[1] * item[2]
            else:
                self.orders_data.pop(self.selected_row)
                if self.selected_row > 0:
                    self.selected_row -= 1
                elif len(self.orders_data) == 0:
                    self.selected_row = -1
            self.update_orders_table()
            self.update_total_price_label()



    def print_invoice_popup(self, instance):
        popup_label = Label(text="Invoice printed!")
        close_button = Button(text="Close", size_hint=(None, None), size=(100, 40))
        popup_content = BoxLayout(orientation="vertical", padding=10)
        popup_content.add_widget(popup_label)
        popup_content.add_widget(close_button)
        popup = Popup(title="Print Invoice", content=popup_content, size_hint=(0.5, 0.5))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

        #TODO we need to add a new dorpDownMenu for orders 
        #TODO create a controller that will lake the data from the dorder table and then will return a list with products.
