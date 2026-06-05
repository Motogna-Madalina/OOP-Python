from datetime import datetime

class Order:

    def __init__(self, customer, products):

        self.customer = customer
        self.products = products
        self.order_date = datetime.now()

    def calculate_total(self):

        total = 0

        for product in self.products:
            total += product.price

        # 5% descuento para empresa
        if self.customer.__class__.__name__ == "CompanyCustomer":
            total *= 0.95

        return round(total, 2)

    def create_invoice(self):

        with open("invoice.txt", "w") as file:

            file.write("WARENWELT INVOICE\n")
            file.write("====================\n\n")

            file.write(f"Date: {self.order_date}\n\n")

            for product in self.products:

                file.write(
                    f"{product.name} - {product.price} EUR\n"
                )

            file.write("\n")

            file.write(
                f"TOTAL: {self.calculate_total():.2f} EUR"
            )