from data_providers import UserDataProvider
from models import Restaurant, Menu, Product, Table
from managers import OrderStatus, UserRole

class SecurityController:
    logged_in_user = None
    
    # singleton variable
    __instance = None
    def __init__(self):
        if SecurityController.__instance is  None:
            SecurityController.__instance = self

    @staticmethod
    def get_instance():
        if SecurityController.__instance is None:
            SecurityController()
        return SecurityController.__instance
 

    def login_user(self, username, password):
        user_data_provider = UserDataProvider()
        user_list = user_data_provider.users
        for user in user_list:
            if user.username == username and user.password == password:
                # login successfully as username and password are correct
                SecurityController.logged_in_user = user

    @staticmethod
    def get_logged_in_user():
        return SecurityController.logged_in_user
    
    @staticmethod
    def is_string_null_or_blank( string):
        if(string == ""):
            return True
        else:
            return False

    def sign_out(self, parent):
        from views import LoginView
        SecurityController.logged_in_user = None
        parent.clear_widgets()
        login_view = LoginView()
        parent.add_widget(login_view)
        
    
class RestaurantManagerController():
    def __init__(self) -> None:
        #empty constructor
        pass
    @staticmethod
    def add_restaurant(restaurant: Restaurant) -> None:
        SecurityController.get_logged_in_user().restaurant_list.append(restaurant)

    @staticmethod
    def update_restaurant(old_name: str, old_address: str, new_restaurant: Restaurant) -> None:
        restaurants = SecurityController.get_logged_in_user().restaurant_list
        for restaurant in restaurants:
            if restaurant.name == old_name and restaurant.address == old_address:
                restaurant.name = new_restaurant.name
                restaurant.address = new_restaurant.address
                return
        SecurityController.get_logged_in_user().restaurant_list = restaurants

    @staticmethod
    def delete_restaurant( name: str, address: str) -> None:
        restaurants =SecurityController.get_logged_in_user().restaurant_list
        for restaurant in restaurants:
            if restaurant.name == name and restaurant.address == address:
                restaurants.remove(restaurant)
                return 
        SecurityController.get_logged_in_user().restaurant_list = restaurants


class MenuManagerController():
    def __init__(self) -> None:
        #empty constructor
        pass
    @staticmethod
    def add_menu( new_menu: Menu, restaurant: Restaurant) -> None:
        menus = restaurant.menu_list
        menus.append(new_menu)
        restaurant.menu_list = menus

    @staticmethod
    def update_menu(old_menu_name: str, new_menu_name : str, restaurant: Restaurant) -> None:
        menus = restaurant.menu_list
        for menu in menus:
            if menu.menu_name == old_menu_name:
               menu.menu_name = new_menu_name
               return
        restaurant.menu_list = menus

    @staticmethod
    def delete_menu( menu_to_delete_name: str, restaurant: Restaurant) -> None:
        menus = restaurant.menu_list
        for menu in menus:
            if menu.menu_name == menu_to_delete_name:
                menus.remove(menu)
                return
        restaurant.menu_list = menus


class MenuItemManagerController():
    def __init__(self) -> None:
        #empty constructor
        pass
    @staticmethod
    def add_menu_item(menu_item: Product, selected_menu: Menu) -> None:
            product_item_list = selected_menu.menu_items
            product_item_list.append(menu_item)
            selected_menu.menu_items = product_item_list
    @staticmethod
    def update_menu_item(old_product: Product, new_product: Product, selected_menu: Menu) -> None:
        selcted_menu_item_list = selected_menu.menu_items
        for menu_item in selcted_menu_item_list:
            if menu_item.id == old_product.id and menu_item.name == old_product.name and menu_item.price == old_product.price:
                menu_item.id = new_product.id
                menu_item.name = new_product.name
                menu_item.price = new_product.price
                return
        selected_menu.menu_items = selcted_menu_item_list

    @staticmethod
    def delete_menu_item( menu_item_to_delete: Product, selected_menu: Menu ) -> None:
        selcted_menu_item_list = selected_menu.menu_items
        for menu_item in selcted_menu_item_list:
            if menu_item.id == menu_item_to_delete.id and menu_item.name == menu_item_to_delete.name and menu_item.price == menu_item_to_delete.price:
                selcted_menu_item_list.remove(menu_item)
                return
        selected_menu.menu_items = selcted_menu_item_list

class TableManagerController():
    def __init__(self) -> None:
        #empty constructor
        pass
    @staticmethod
    def add_table( new_table: Table, restaurant: Restaurant) -> None:
        tables = restaurant.table_list
        tables.append(new_table)
        restaurant.table_list = tables

    @staticmethod
    def update_table(old_table: Table, new_table:Table, restaurant: Restaurant) -> None:
        tables = restaurant.table_list
        for table in tables:
            if table.table_number == old_table.table_number and table.seats == old_table.seats:
                table.table_number = new_table.table_number
                table.seats = new_table.seats
                return
        restaurant.table_list = tables

    @staticmethod
    def delete_table( table_to_delete:Table, restaurant: Restaurant) -> None:
        tables = restaurant.table_list
        for table in tables:
            if table.table_number == table_to_delete.table_number and table.seats == table_to_delete.seats:
                tables.remove(table)
                return 
        restaurant.table_list = tables

class TableOrdersController():
    def __init__(self) -> None:
        #empty constructor
        pass


class OrderStatusController():
    def __init__(self) -> None:
        #empty constructor
        pass

    @staticmethod
    def get_new_order_status(current_status):
        user_role = SecurityController.get_logged_in_user().user_role

        if user_role == UserRole.WAITER:
            if current_status == OrderStatus.QUEUE.value:
                return OrderStatus.IN_PROGRESS.value
            elif current_status == OrderStatus.IN_PROGRESS.value:
                return OrderStatus.READY.value
            elif current_status == OrderStatus.READY.value:
                return OrderStatus.DELIVERED.value
            elif current_status == OrderStatus.DELIVERED.value:
                return OrderStatus.PAID.value
        elif user_role == UserRole.COOK:
            if current_status == OrderStatus.QUEUE.value:
                return OrderStatus.IN_PROGRESS.value
            elif current_status == OrderStatus.IN_PROGRESS.value:
                return OrderStatus.READY.value

        return None

    @staticmethod
    def get_reverted_order_status(current_status):
        user_role = SecurityController.get_logged_in_user().user_role

        if user_role == UserRole.WAITER:
            if current_status == OrderStatus.IN_PROGRESS.value:
                return OrderStatus.QUEUE.value
            elif current_status == OrderStatus.READY.value:
                return OrderStatus.IN_PROGRESS.value
            elif current_status == OrderStatus.DELIVERED.value:
                return OrderStatus.READY.value
            elif current_status == OrderStatus.PAID.value:
                return OrderStatus.DELIVERED.value
        elif user_role == UserRole.COOK:
            if current_status == OrderStatus.IN_PROGRESS.value:
                return OrderStatus.QUEUE.value
            elif current_status == OrderStatus.READY.value:
                return OrderStatus.IN_PROGRESS.value

        return None
