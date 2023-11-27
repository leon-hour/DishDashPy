from enum import Enum


class User:
    def __init__(self, username, password, user_role):
        self.__username = username
        self.__password = password
        self.__user_role = user_role
        self.__restaurant_list = []

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    @property
    def user_role(self):
        return self.__user_role

    @user_role.setter
    def user_role(self, value):
        self.__user_role = value

    @property
    def restaurant_list(self):
        return self.__restaurant_list

    @restaurant_list.setter
    def restaurant_list(self, value):
        self.__restaurant_list = value



class Menu:
    def __init__(self, menu_name, menu_items):
        self.__menu_name = menu_name
        self.__menu_items = menu_items

    @property
    def menu_name(self):
        return self.__menu_name

    @menu_name.setter
    def menu_name(self, value):
        self.__menu_name = value

    @property
    def menu_items(self):
        return self.__menu_items

    @menu_items.setter
    def menu_items(self, value):
        self.__menu_items = value

    def __str__(self):
        return self.__menu_name


class Restaurant:
    def __init__(self, name, address, menu_list, table_list):
        self.__name = name
        self.__address = address
        self.__menu_list = menu_list
        self.__table_list = table_list

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @property
    def menu_list(self) -> list:
        return self.__menu_list

    @menu_list.setter
    def menu_list(self, value):
        self.__menu_list = value

    @property
    def table_list(self) -> list:
        return self.__table_list

    @table_list.setter
    def table_list(self, value):
        self.__table_list = value

    def __str__(self):
        return self.name



class Table:
    def __init__(self, table_number, seats):
        self.__table_number = table_number
        self.__seats = seats

    @property
    def table_number(self):
        return self.__table_number

    @table_number.setter
    def table_number(self, value):
        self.__table_number = value

    @property
    def seats(self):
        return self.__seats

    @seats.setter
    def seats(self, value):
        self.__seats = value


class Product:
    def __init__(self, id, name, price):
        self.__name = name
        self.__price = price
        self.__id = id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

class Meal(Product):
    def __init__(self, product_id, name, price, description=None):
        super().__init__(product_id, name, price)
        self.description = description

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description


class Drink(Product):
    def __init__(self, product_id, name, price, sugar_free=None):
        super().__init__(product_id, name, price)
        self.sugar_free = sugar_free

    @property
    def sugar_free(self):
        return self._sugar_free

    @sugar_free.setter
    def sugar_free(self, sugar_free):
        self._sugar_free = sugar_free


