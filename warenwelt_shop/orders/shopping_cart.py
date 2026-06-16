"""
This class represents a shopping cart.

"""

from orders.order import Order


class ShoppingCart:

    def __init__(self, customer):
        # Make an empty shopping cart for one customer. At the start there
        # are no products and the total is 0. Later the customer can add
        # products and the total will go up.
        self.customer = customer
        self.products = []
        self.total_amount = 0

    def add_product(self, product):
        # Add one product to the cart. After that we calculate the total
        # again, so the cart always shows the right amount.
        self.products.append(product)
        self.calculate_total()

    def remove_product(self, product):
        # Take one product out of the cart. First we check if the product is
        # really in the cart, because remove() gives an error if it is not
        # there. If we remove it, we calculate the total again.
        if product in self.products:
            self.products.remove(product)
            self.calculate_total()

    def clear_cart(self):
        # Empty the cart. We delete all products and set the total back to 0,
        # so the cart is like a new one again.
        self.products = []
        self.total_amount = 0

    def calculate_total(self):
        # Add the price of all products in the cart, save it in
        # self.total_amount, and return it so other code can use it.
        self.total_amount = sum(product.price for product in self.products)
        return self.total_amount

    def checkout(self):
        # Finish shopping: make a real Order from the products in the cart
        # for this customer. The cart does not change here; it only gives its
        # products and customer to a new Order.
        return Order(self.customer, self.products)