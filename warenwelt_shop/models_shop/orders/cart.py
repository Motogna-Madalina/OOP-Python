from exceptions.shop_error import ShopError


class Cart:


    def __init__(self, customer):
        self._customer = customer
        self._products = []

    # customer ----------------------------------------------------------
    def get_customer(self):
        return self._customer

    # products ----------------------------------------------------------
    def get_products(self):
        return self._products

    # Produkt hinzufügen -------------------------------------------------
    def add_product(self, product):
        self._products.append(product)
        print(f"Produkt hinzugefügt: {product.get_name()}")

    # Produkt entfernen --------------------------------------------------
    def remove_product(self, product):
        if product not in self._products:
            raise ShopError(f"Produkt nicht im Warenkorb: {product.get_name()}")
        self._products.remove(product)
        print(f"Produkt entfernt: {product.get_name()}")

    # Warenkorb leeren ---------------------------------------------------
    def clear(self):
        self._products = []
        print("Warenkorb geleert.")

    # Gesamtsumme (ohne Rabatt) ------------------------------------------
    def get_total(self):
        total = 0
        for product in self._products:
            total = total + float(product.get_price())
        return total