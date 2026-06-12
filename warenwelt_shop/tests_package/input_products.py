"""
This file inserts 3 products of each type into the database:
3 books, 3 electronics and 3 clothing items.
"""

from data_base.storage import Storage

from shop_models.products.book import Book
from shop_models.products.clothing import Clothing
from shop_models.products.electronics import Electronics


storage = Storage(
    host="127.0.0.1",
    user="root",
    password="Motogna6624.",
    database="warenwelt",
    port=3306
)

storage.connect()


# ==================================
# BOOKS
# ==================================

books = [
    Book("Python Basics", 29.99, "John Author", 350),
    Book("Clean Code", 39.99, "Robert Martin", 464),
    Book("The Hobbit", 14.99, "J.R.R. Tolkien", 310),
]


# ==================================
# ELECTRONICS
# ==================================

electronics = [
    Electronics("Dell Laptop", 1200.99, "Dell", 2),
    Electronics("iPhone 15", 999.00, "Apple", 1),
    Electronics("Samsung TV", 749.50, "Samsung", 3),
]


# ==================================
# CLOTHING
# ==================================

clothing = [
    Clothing("T-Shirt", 19.99, "L", "Black"),
    Clothing("Jeans", 49.99, "M", "Blue"),
    Clothing("Jacket", 89.99, "XL", "Green"),
]


# ==================================
# SAVE EVERYTHING
# ==================================

print("\n--- SAVE BOOKS ---")

for book in books:
    book.save(storage)

print("3 books saved")


print("\n--- SAVE ELECTRONICS ---")

for electronic in electronics:
    electronic.save(storage)

print("3 electronics saved")


print("\n--- SAVE CLOTHING ---")

for item in clothing:
    item.save(storage)

print("3 clothing items saved")


# ==================================
# CHECK WHAT IS IN THE DATABASE
# ==================================

print("\n--- ALL BOOKS IN DATABASE ---")
print(Book.load_all(storage))

print("\n--- ALL ELECTRONICS IN DATABASE ---")
print(Electronics.load_all(storage))

print("\n--- ALL CLOTHING IN DATABASE ---")
print(Clothing.load_all(storage))


storage.disconnect()