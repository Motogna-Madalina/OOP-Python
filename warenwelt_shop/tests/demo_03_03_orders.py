from models_shop.customers.private_customer import PrivateCustomer
from models_shop.customers.company_customer import CompanyCustomer
from models_shop.products.electronic import Electronic
from models_shop.products.clothing import Clothing
from models_shop.products.book import Book
from models_shop.orders.cart import Cart
from models_shop.orders.order import Order


# Kunde + Produkte erstellen---------------------------------------------------
firma = CompanyCustomer("Alpha GmbH", "Industrieweg 5, Linz", "office@alpha.at", "+437320010001", "firmenpw99", "100001")

laptop = Electronic("Laptop X1", 999.99, 1.5, "Lenovo", 2)
shirt = Clothing("T-Shirt Basic", 19.99, 0.2, "M", "blau")
buch = Book("Python lernen", 29.50, 0.6, "Anna Schmidt", 350)

# Warenkorb füllen-------------------------------------------------------------
warenkorb = Cart(firma)
warenkorb.add_product(laptop)
warenkorb.add_product(shirt)
warenkorb.add_product(buch)

print("Produkte im Warenkorb:", len(warenkorb.get_products()))
print("Zwischensumme:", warenkorb.get_total(), "EUR")

# Ein Produkt entfernen--------------------------------------------------------
warenkorb.remove_product(shirt)
print("Nach Entfernen:", len(warenkorb.get_products()), "Produkte")

# Bestellung abschließen (Firmenkunde -> 5% Rabatt)----------------------------
bestellung = Order(warenkorb)
print("Gesamtbetrag (mit 5% Firmenrabatt):", round(bestellung.get_total(), 2), "EUR")
bestellung.create_invoice()

# Vergleich: Privatkunde ohne Rabatt-------------------------------------------
print("\n--- Privatkunde (kein Rabatt) ---")
privat = PrivateCustomer("Anna Müller", "Hauptstraße 1, Wien", "anna@example.com", "+436641234567", "geheim123", "23.04.1995")
korb2 = Cart(privat)
korb2.add_product(laptop)
bestellung2 = Order(korb2)
print("Gesamtbetrag:", round(bestellung2.get_total(), 2), "EUR")
bestellung2.create_invoice()