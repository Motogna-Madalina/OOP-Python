"""
This abstract class represents a product.
"""

from abc import ABC


class Product(ABC):

    _id_counter = 1

    def __init__(self, name, price):

        self.id = Product._id_counter
        Product._id_counter += 1

        self.name = name
        self.price = price

    # Getters

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    # Setters

    def set_name(self, name):
        self.name = name

    def set_price(self, price):
        self.price = price