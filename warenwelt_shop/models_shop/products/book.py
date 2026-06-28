from models_shop.products.product import Product
from utils.validator import Validator
from exceptions.shop_error import ShopError


class Book(Product):


    def __init__(self, name, price, weight, author, pages):
        super().__init__(name, price, weight)
        self._author = None
        self._pages = None
        self.set_author(author)
        self.set_pages(pages)

    def get_category(self):
        return "Book"

    #author--------------------------------------------------------------
    def get_author(self):
        return self._author

    def set_author(self, author):
        if not Validator.validate_text(author):
            raise ShopError(f"Ungültiger Autor: {author}")
        self._author = author

    #pages--------------------------------------------------------------
    def get_pages(self):
        return self._pages

    def set_pages(self, pages):
        if not Validator.validate_pages(pages):
            raise ShopError(f"Ungültige Seitenanzahl (muss > 0 sein): {pages}")
        self._pages = pages