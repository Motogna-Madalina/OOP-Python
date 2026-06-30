from datetime import datetime

from exceptions.shop_error import ShopError


class Order:


    # 5% Rabatt für Firmenkunden
    DISCOUNT_RATE = 0.05

    def __init__(self, cart):
        if not cart.get_products():
            raise ShopError("Der Warenkorb ist leer – keine Bestellung möglich.")

        # User Daten + bestellte Produkte aus dem Warenkorb übernehmen
        self._customer = cart.get_customer()
        self._products = list(cart.get_products())   # Kopie -> Warenkorb bleibt unberührt
        self._order_time = datetime.now()
        self._total = self.calculate_total()

    # getters ------------------------------------------------------------
    def get_customer(self):
        return self._customer

    def get_products(self):
        return self._products

    def get_order_time(self):
        return self._order_time

    def get_total(self):
        return self._total

    # Gesamtkosten berechnen---5% Rabatt für Firmenkunden---------------
    def calculate_total(self):
        subtotal = 0
        for product in self._products:
            subtotal = subtotal + float(product.get_price())

        # Automatischer 5%-Rabatt nur für Firmenkunden
        if self._customer.get_type() == "company":
            subtotal = subtotal * (1 - Order.DISCOUNT_RATE)

        return subtotal

    # Rechnung als- txt-Datei erstellen ----------------------------------
    def create_invoice(self):
        with open("rechnung.txt", "w", encoding="utf-8") as datei:
            datei.write("WARENWELT - RECHNUNG\n")
            datei.write(f"Datum: {self._order_time.strftime('%d.%m.%Y %H:%M')}\n")
            datei.write(f"Kunde: {self._customer.get_name()} ({self._customer.get_type()})\n\n")

            for product in self._products:
                datei.write(f"{product.get_name()}: {float(product.get_price())} EUR\n")

            datei.write(f"\nGesamtbetrag: {round(self._total, 2)} EUR\n")

        print("Rechnung erstellt: rechnung.txt")