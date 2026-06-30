from models_shop.products.product import Product
from utils.validator import Validator
from exceptions.shop_error import ShopError


class Clothing(Product):


    def __init__(self, name, price, weight, size, color):
        super().__init__(name, price, weight)
        self._size = None
        self._color = None
        self.set_size(size)
        self.set_color(color)

    def get_category(self):
        return "Clothing"

    #size-----------------------------------------------------------
    def get_size(self):
        return self._size

    def set_size(self, size):
        if not Validator.validate_text(size):
            raise ShopError(f"Ungültige Größe: {size}")
        self._size = size

    #color-----------------------------------------------------------
    def get_color(self):
        return self._color

    def set_color(self, color):
        if not Validator.validate_color(color):
            raise ShopError(f"Ungültige Farbe: {color}")
        self._color = color

