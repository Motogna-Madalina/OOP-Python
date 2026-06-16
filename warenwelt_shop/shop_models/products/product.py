"""
This abstract class represents a product.

It is a real abstract base class now: every concrete product
(Book, Electronics, Clothing) MUST provide its own `category`
and `short_detail()`. Because of the abstract methods, Product
itself can no longer be instantiated by mistake.
"""

from abc import ABC, abstractmethod


class Product(ABC):

    _id_counter = 1

    def __init__(self, name, price):

        self.id = Product._id_counter
        Product._id_counter += 1

        self.name = name
        self.price = price

    # ------------------------------------------------------------------
    # Abstract contract: every concrete product must implement these.
    # This is what makes the class truly abstract and lets the rest of
    # the app use polymorphism instead of isinstance() chains.
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def category(self):
        raise NotImplementedError

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
