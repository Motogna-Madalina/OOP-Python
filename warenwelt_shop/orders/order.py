"""
This class represents an order.
"""

from datetime import datetime

from shop_models.customers.company_customer import CompanyCustomer


class Order:

    def __init__(
            self,
            customer,
            products
    ):

        self.customer = customer
        self.products = products

        self.order_date = datetime.now()

        self.total_amount = self.calculate_total()

    def calculate_total(self):

        total = sum(
            product.price
            for product in self.products
        )

        if isinstance(
                self.customer,
                CompanyCustomer
        ):
            total *= 0.95

        return total

    def create_invoice(self):

        with open(
                "invoice.txt",
                "w"
        ) as file:

            file.write(
                "WARENWELT INVOICE\n\n"
            )

            file.write(
                f"Customer: {self.customer.name}\n"
            )

            file.write(
                f"Date: {self.order_date}\n\n"
            )

            for product in self.products:

                file.write(
                    f"{product.name} - {product.price} EUR\n"
                )

            file.write(
                f"\nTotal: {self.total_amount:.2f} EUR"
            )