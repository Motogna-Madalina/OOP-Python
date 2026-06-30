from storage.storage import Storage
from models_shop.customers.customer import Customer
from models_shop.products.product import Product

storage = Storage()
storage.connect()

# Alle Produkte laden----------------------------------------------------------
products = Product.load_all(storage)
print("Produkte:", len(products))
for product in products:
    print("-", product.get_category(), "-", product.get_name(), "-", product.get_price(), "€")

# Ein Produkt laden------------------------------------------------------------
produkt = Product.load(storage, 1)
print("Produkt 1:", produkt.get_category(), "-", produkt.get_name())

# Alle Kunden laden------------------------------------------------------------
customers = Customer.load_all(storage)
print("Kunden:", len(customers))
for customer in customers:
    print("-", customer.get_type(), "-", customer.get_name(), "-", customer.get_email())

# Ein Kunde laden--------------------------------------------------------------
kunde = Customer.load(storage, 1)
print("Kunde 1:", kunde.get_type(), "-", kunde.get_name())

storage.disconnect()