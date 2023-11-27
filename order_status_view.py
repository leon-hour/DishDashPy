from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from controllers import SecurityController, OrderStatusController
from managers import UserRole, OrderStatus
from models import Restaurant, Table

class OrderStatusView(BoxLayout):
    content_panel = BoxLayout()
    selected_row = -1
    restaurant = Restaurant
    table = Table
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.restaurant = SecurityController.get_logged_in_user().restaurant_list[0]
        self.add_widget(self._create_order_status_components())

    def _create_order_status_components(self):
        table_panel = GridLayout(cols = 1, padding = 10,spacing = 0)
        table_panel.size_hint_x = None
        table_panel.width = 700
        self.order_status_table = self._create_order_status_table()
        self.order_status_table.bind(on_row_press=self._on_row_press)
        table_panel.add_widget(self.order_status_table)
        
        buttons_component_panel = GridLayout(cols=3, padding=20, spacing=10, size_hint=(0.2, 0.2))
        update_status_button = Button(text='Update status', size_hint=(None, None), size=(150, 40), background_color=(0, 1, 1, 1))
        revert_status_button = Button(text='Revert status', size_hint=(None, None), size=(150, 40), background_color=(0, 1, 1, 1))
        refresh_button = Button(text='Refresh', size_hint=(None, None), size=(150, 40), background_color=(0, 1, 1, 1))
        update_status_button.bind(on_press=self._update_order_status)
        revert_status_button.bind(on_press=self._revert_order_status)
        refresh_button.bind(on_press=self._refresh_order_status)
        buttons_component_panel.add_widget(update_status_button)
        buttons_component_panel.add_widget(revert_status_button)
        buttons_component_panel.add_widget(refresh_button)
        table_panel.add_widget(buttons_component_panel)

        return table_panel

    def _create_order_status_table(self):
        table_row_data = []
        tables_list = self.restaurant.table_list
        for table in tables_list:
            table_row_data.append((table.table_number, OrderStatus.QUEUE.value))
        self.order_status_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            check=True,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Table number", 80),
                ("Status", 80)
            ],
            row_data=table_row_data
        )
        return self.order_status_table

    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index/2)

    def _update_order_status(self, instance):
        if self.selected_row == -1:
            return

        current_status = self.order_status_table.row_data[self.selected_row][1]
        new_status = OrderStatusController.get_new_order_status(current_status)

        if new_status is not None:
            self.order_status_table.row_data[self.selected_row] = (
                self.order_status_table.row_data[self.selected_row][0], new_status
            )

    def _revert_order_status(self, instance):
        if self.selected_row == -1:
            return

        current_status = self.order_status_table.row_data[self.selected_row][1]
        new_status = OrderStatusController.get_reverted_order_status(current_status)

        if new_status is not None:
            self.order_status_table.row_data[self.selected_row] = (
                self.order_status_table.row_data[self.selected_row][0], new_status
            )


    def _refresh_order_status(self, instance):
        if self.selected_row != -1:
            current_status = self.order_status_table.row_data[self.selected_row][1]
            if SecurityController.get_logged_in_user().user_role == UserRole.COOK and current_status == OrderStatus.READY.value:
                self.order_status_table.row_data.pop(self.selected_row)
                self.selected_row = -1
            if SecurityController.get_logged_in_user().user_role == UserRole.WAITER and current_status == OrderStatus.PAID.value:
                self.order_status_table.row_data.pop(self.selected_row)
                
                self.selected_row = -1