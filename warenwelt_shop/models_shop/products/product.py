from abc import ABC, abstractmethod

from utils.validator import Validator
from exceptions.shop_error import ShopError


class Product(ABC):


    def __init__(self, name, price, weight):
        # The id is None - we will make it in MySql (AUTO_INCREMENT).
        self._id = None
        self._name = None
        self._price = None
        self._weight = None

        self.set_name(name)
        self.set_price(price)
        self.set_weight(weight)


    @abstractmethod
    def get_category(self):
        pass

    #id-----------------------------------------------------------------

    def get_id(self):
        return self._id

    #name----------------------------------------------------------------

    def get_name(self):
        return self._name

    def set_name(self, name):
        if not Validator.validate_text(name):
            raise ShopError(f"Ungültiger Produktname: {name}")
        self._name = name

    #--------------------------------------------------------------------

    def get_price(self):
        return self._price

    def set_price(self, price):
        if not Validator.validate_price(price):
            raise ShopError(f"Ungültiger Preis (muss >= 0 sein): {price}")
        self._price = price

    #weight-----------------------------------------------------------------
    
    def get_weight(self):
        return self._weight

    def set_weight(self, weight):
        if not Validator.validate_weight(weight):
            raise ShopError(f"Ungültiges Gewicht (muss > 0 sein): {weight}")
        self._weight = weight