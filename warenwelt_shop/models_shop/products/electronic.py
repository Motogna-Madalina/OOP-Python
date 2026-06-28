from models_shop.products.product import Product
from utils.validator import Validator
from exceptions.shop_error import ShopError


class Electronic(Product):


    def __init__(self, name, price, weight, brand, warranty_years):
        super().__init__(name, price, weight)

        self._brand = None
        self._warranty_years = None

        self.set_brand(brand)
        self.set_warranty_years(warranty_years)

    def get_category(self):
        return "Electronic"

    #brand---------------------------------------------------------------------
    def get_brand(self):
        return self._brand

    def set_brand(self, brand):
        if not Validator.validate_text(brand):
            raise ShopError(f"Ungültige Marke: {brand}")
        self._brand = brand

    #warranty years-------------------------------------------------------------
    def get_warranty_years(self):
        return self._warranty_years

    def set_warranty_years(self, years):
        if not Validator.validate_warranty_years(years):
            raise ShopError(f"Ungültige Garantie (Jahre, muss >= 0 sein): {years}")
        self._warranty_years = years