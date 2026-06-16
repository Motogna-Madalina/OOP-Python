"""
This class represents an order.

"""

import os
from datetime import datetime


class Order:

    def __init__(self, customer, products):
        # Make a new order. We save the customer who buys and the list of
        # products. We also save the date and time of now, and we calculate
        # the total price at once, so the order knows its total from the start.
        self.customer = customer
        self.products = products
        self.order_date = datetime.now()
        self.total_amount = self.calculate_total()

    def calculate_total(self):
        # Add the price of all products to get the total, then apply the
        # customer's own discount. Each customer type decides its rate via
        # discount_rate() (0% for private, 5% for company), so this method
        # never needs to know which concrete customer class it is dealing
        # with. We return the total so we can save it in self.total_amount.
        total = sum(product.price for product in self.products)
        total = total * (1 - self.customer.discount_rate())
        return total

    def create_invoice(self):
        # Write an invoice for this order in a text file. First we write the
        # title, the customer name and the date. Then we write one line for
        # each product with its price. At the end we write the total price
        # with two decimals. We always save the file next to this file
        # (orders/invoice.txt), so it does not matter from where we start
        # the program.
        path = os.path.join(os.path.dirname(__file__), "invoice.txt")

        with open(path, "w") as file:
            file.write("WARENWELT INVOICE\n\n")
            file.write(f"Customer: {self.customer.name}\n")
            file.write(f"Date: {self.order_date}\n\n")

            for product in self.products:
                file.write(f"{product.name} - {product.price} EUR\n")

            file.write(f"\nTotal: {self.total_amount:.2f} EUR")