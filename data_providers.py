from models import User, Restaurant, Table, Menu, Product, Meal, Drink
from managers import UserRole
from typing import List


class UserDataProvider:
    def __init__(self):
        self.users = []
        self.restaurant_data_provider = RestaurantDataProvider()
        self.create_users()

    def create_users(self):
        self.create_restaurant_admin_users()
        self.create_waiter_users()
        self.create_cook_users()

    def create_restaurant_admin_users(self):
        # Create restaurant admin users and add restaurants to their restaurant lists
        restaurant_admin_user1 = User("admin1", "admin11", UserRole.ADMIN)
        restaurant_admin_user1.restaurant_list.append(self.restaurant_data_provider.restaurants[0])
        restaurant_admin_user1.restaurant_list.append(self.restaurant_data_provider.restaurants[1])
        restaurant_admin_user2 = User("1", "1", UserRole.ADMIN)
        restaurant_admin_user2.restaurant_list.append(self.restaurant_data_provider.restaurants[0])
        restaurant_admin_user2.restaurant_list.append(self.restaurant_data_provider.restaurants[1])
        restaurant_admin_user2.restaurant_list.append(self.restaurant_data_provider.restaurants[2])
        restaurant_admin_user2.restaurant_list.append(self.restaurant_data_provider.restaurants[3])

        # Add the users to the list of all users
        self.users.append(restaurant_admin_user1)
        self.users.append(restaurant_admin_user2)

    def create_waiter_users(self):
        # Create waiter users and add restaurants to their restaurant lists
        waiter1 = User("waiter1", "waiter11", UserRole.WAITER)
        waiter1.restaurant_list.append(self.restaurant_data_provider.restaurants[0])
        

        waiter2 = User("waiter2", "waiter22", UserRole.WAITER)
        waiter2.restaurant_list.append(self.restaurant_data_provider.restaurants[2])

        # Add the users to the list of all users
        self.users.append(waiter1)
        self.users.append(waiter2)

    def create_cook_users(self):
        # Create cook users and add restaurants to their restaurant lists
        cook1 = User("cook1", "cook11", UserRole.COOK)
        cook1.restaurant_list.append(self.restaurant_data_provider.restaurants[0])

        cook2 = User("cook2", "cook22", UserRole.COOK)
        cook2.restaurant_list.append(self.restaurant_data_provider.restaurants[1])

        # Add the users to the list of all users
        self.users.append(cook1)
        self.users.append(cook2)

    def get_users(self):
        # Return the list of all users
        return self.users



class RestaurantDataProvider:
    def __init__(self):
        self.restaurants = []
        self.create_restaurants()

    def create_restaurants(self):
        restaurant1 = self._create_restaurant_1()
        restaurant2 = self._create_restaurant_2()
        restaurant3 = self._create_restaurant_3()
        restaurant4 = self._create_restaurant_4()
        # Add the restaurants to the list of all restaurants
        self.restaurants.append(restaurant1)
        self.restaurants.append(restaurant2)
        self.restaurants.append(restaurant3)
        self.restaurants.append(restaurant4)

    def _create_restaurant_1(self):
        menus = self._create_menu_group_1()
        tables = self._create_table_group_1()
        restaurant_1 = Restaurant("Test Restuarant 1", " test Address 1", menus, tables)
        return restaurant_1

    def _create_table_group_1(self):
        table1 = Table(11,2)
        table2 = Table(12,4)
        table3 = Table(13,6)
        table4 = Table(14,8)
        table_list = [table1, table2, table3, table4]
        return table_list
    
    def _create_menu_group_1(self):

        breakfast_menu = Menu("Breakfast Menu", self._create_breakfast_menu_items())
        lunch_menu = Menu("Lunch Menu", self._create_lunch_menu_items())
        dinner_menu = Menu("Dinner Menu", self._create_dinner_menu_items())
        menu_list = [breakfast_menu, lunch_menu, dinner_menu]
        return menu_list
    
    def _create_breakfast_menu_items(self):
        product1 = Meal(100, "Egg Sandwich",40, "Sandwich with eggs")
        product2 = Meal(101, "Cheese Sandwich",45, "Sandwich with cheese")
        product3 = Meal(102, "Tuna sandwich",30, "Sandwich with tuna")
        product4 = Meal(103, "Vegetarian sandwich", 55, "Sandwich with tomato and cucumbre")
        product_menu =[product1, product2, product3, product4]
        return product_menu

    def _create_dinner_menu_items(self):
        product1 = Meal(200, "Hamburger",40, "Angus beef patty, tomato, red onion")
        product2 = Meal(201, "Cheeseburger",45, "Angus beef patty, cheese, tomato, red onion")
        product3 = Meal(202, "Sandwich",30, "Chicken, mayonnaise, peppers")
        product4 = Meal(203, "Hotdog", 55, "Beef, mustard, ketchup, onion, cucumber")
        product_menu = [product1, product2, product3, product4]
        return product_menu
    
    def _create_lunch_menu_items(self):
        product1 =  Meal(300, "Salmon",40, "Salmon filet with potatoes")
        product2 =  Meal(301, "Steak ",45, "Steak with butter and fries")
        product3 =  Meal(302, "Roastbeef",30, "Roastbeef with vegetables")
        product4 =  Meal(303, "Spageti Bolognese", 55, "Spageti with homemade bolognese sauce")
        product_menu = [product1, product2, product3, product4]
        return product_menu

    def _create_restaurant_2(self):
        menus = self._create_menu_group_2()
        tables = self._create_table_group_3()
        restaurant_2 = Restaurant("Test Restuarant 2", " test Address 2", menus, tables)
        return restaurant_2
    
    def _create_table_group_2(self):
        table1 = Table(21,2)
        table2 = Table(22,4)
        table3 = Table(23,6)
        table_list = [table1, table2, table3]
        return table_list

    def _create_menu_group_2(self):
        vodka_martini = Drink(100, "Vodka Martini",80)
        cosmopolitan = Drink(200,"Cosmopolitan",50)

        product_list = [vodka_martini, cosmopolitan]

        ice_cream_menu = Menu("Ice cream Menu", product_list)
        menu_list = [ice_cream_menu]
        return menu_list
    
    def _create_restaurant_3(self):
        menus = self._create_menu_group_3()
        tables = self._create_table_group_3()
        restaurant_3 = Restaurant("Test Restuarant 3", " test Address 3", menus, tables)
        return restaurant_3
    
    def _create_table_group_3(self):
        table1 = Table(31,2)
        table2 = Table(32,4)
        table_list = [table1, table2]
        return table_list

    def _create_menu_group_3(self):
        vanila_ice_cream = Meal(100, "Ice Cream Vanila",10,"")
        pinneaple_ice_cream = Meal(200, "Ice Cream Pinneaple",15)

        product_list = [vanila_ice_cream, pinneaple_ice_cream]

        ice_cream_menu = Menu("Ice cream Menu", product_list)
        menu_list = [ice_cream_menu]
        return menu_list

    
    def _create_restaurant_4(self):
        menus = self._create_menu_group_4()
        tables = self._create_table_group_4()
        restaurant_4 = Restaurant("Test Restuarant 4", " test Address 4", menus, tables)
        return restaurant_4

    def _create_table_group_4(self):
        table = Table(41,2)
        table_list = [table]
        return table_list

    def _create_menu_group_4(self):
        pizza_margarita = Meal(100, "Pizza Margarita", 6, "lots of cheese")
        pizza_vegetarian = Meal(101, "Pizza Vegetarian", 6.5, "cheese, green pepper, tomator, onion")
        pizza_mushroom =  Meal(102, "Pizza Mushroom", 6.5, "cheese, mushroom, garlic, chilli")
        pizza_mexican =  Meal(103, "Pizza Mexican", 7, "cheese, chilli, sweet corn, tomato, olives")

        product_list = [pizza_margarita, pizza_vegetarian, pizza_mushroom, pizza_mexican]

        pizza_menu = Menu("Pizza Menu", product_list)
        menu_list = [pizza_menu]
        return menu_list

    def get_restaurants(self):
        return self.restaurants

    def set_restaurants(self, restaurant_list):
        self.restaurants = restaurant_list

