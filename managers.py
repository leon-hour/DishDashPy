from enum import Enum

class UserRole(Enum):
    ADMIN = 1
    WAITER = 2
    COOK = 3

class UserFeatures(Enum):
    RESTAURANT_MANAGER = 1
    MENU_MANAGER = 2 
    MENU_ITEM_MANAGER =3
    TABLE_MANAGER = 4
    SIGN_OUT = 5  
    TABLE_ORDERS = 6
    ORDER_STATUS = 7

class OrderStatus(Enum):
    QUEUE = "QUEUE"
    IN_PROGRESS = "IN PROGRESS"
    READY = "READY"
    PAID = "PAID"
    DELIVERED = "DELIVERED"

class AuthorizationService:

    def get_user_feature_by_user_role(self, user_role):
        if user_role == UserRole.ADMIN:
            return [UserFeatures.RESTAURANT_MANAGER, UserFeatures.MENU_MANAGER, UserFeatures.MENU_ITEM_MANAGER, UserFeatures.TABLE_MANAGER, UserFeatures.SIGN_OUT]
        elif user_role == UserRole.WAITER:
            return [UserFeatures.TABLE_ORDERS, UserFeatures.ORDER_STATUS, UserFeatures.SIGN_OUT]
        elif user_role == UserRole.COOK:
            return [UserFeatures.ORDER_STATUS, UserFeatures.SIGN_OUT]
        elif user_role == None:
            raise RuntimeError("Something went wrong")
        

class UserFeatureLabelResolver:
    user_feature_label_map = None
    
    @staticmethod
    def get_user_feature_label(user_feature):
        return UserFeatureLabelResolver.get_user_feature_label_map().get(user_feature)
    
    @staticmethod
    def get_user_feature_label_map():
        if UserFeatureLabelResolver.user_feature_label_map is None:
            UserFeatureLabelResolver.user_feature_label_map = {
                UserFeatures.RESTAURANT_MANAGER: "Restaurant manager",
                UserFeatures.MENU_MANAGER: "Menu manager",
                UserFeatures.MENU_ITEM_MANAGER: "Menu item manager",
                UserFeatures.TABLE_MANAGER: "Table manager",
                UserFeatures.SIGN_OUT: "Sign out",
                UserFeatures.TABLE_ORDERS: "Table orders",
                UserFeatures.ORDER_STATUS: "Order status",
            }
        
        return UserFeatureLabelResolver.user_feature_label_map