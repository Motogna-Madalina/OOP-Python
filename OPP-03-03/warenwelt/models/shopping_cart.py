class ShoppingCart:

    def __init__(self, customer):

        self.customer = customer
        self.products = []

    def add_product(self, product):

        self.products.append(product)

    def remove_product(self, product):

        if product in self.products:
            self.products.remove(product)

    def clear_cart(self):

        self.products.clear()

    def calculate_total(self):

        total = 0

        for product in self.products:
            total += product.price

        return total