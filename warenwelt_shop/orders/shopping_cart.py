"""
This class represents a shopping cart.
"""

from orders.order import Order


class ShoppingCart:

    def __init__(
            self,
            customer
    ):

        self.customer = customer
        self.products = []
        self.total_amount = 0

    def add_product(
            self,
            product
    ):

        self.products.append(
            product
        )

        self.calculate_total()

    def remove_product(
            self,
            product
    ):

        # Only remove if it is actually in the cart,
        # otherwise list.remove() would raise ValueError.
        if product in self.products:

            self.products.remove(
                product
            )

            self.calculate_total()

    def clear_cart(self):

        self.products.clear()

        self.total_amount = 0

    def calculate_total(self):

        self.total_amount = sum(
            product.price
            for product in self.products
        )

        return self.total_amount


    def checkout(self):

        # Turn the current cart into a real order.
        return Order(
            self.customer,
            self.products
        )