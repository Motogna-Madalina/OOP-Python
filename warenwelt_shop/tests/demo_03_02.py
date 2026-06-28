from models_shop.products.book import *
from models_shop.products.electronic import *
from models_shop.products.clothing import *

# Two products----------------------------------------------------------------------------------
laptop = Electronic("Laptop X1", 999.99, 1.5, "Lenovo", 2)
print("Produkt:", laptop.get_category(), "-", laptop.get_name(), "-", laptop.get_price(), "€")

book = Book("Python lernen", 29.50, 0.6, "Anna Schmidt", 350)
print("Produkt:", book.get_category(), "-", book.get_name(), "-", book.get_pages(), "Seiten")

# An invalid value - error-------------------------------------------------------------
try:
    Electronic("Handy", -100, 0.3, "Samsung", 1)
except ShopError as error:
    print("Fehler:", error)

clothing = Clothing("T-shit", "23", 2, 45, "blue")
print("Produkt:", clothing.get_category(), "-", clothing.get_name(), "-", clothing.get_price(), "-",
clothing.get_size(), "-", clothing.get_color())