"""
This file tests the database functionality.
"""

from data_base.storage import Storage

from shop_models.customers.private_customer import PrivateCustomer
from shop_models.customers.company_customer import CompanyCustomer

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

print("\n--- SAVE CUSTOMERS ---")

private_customer = PrivateCustomer(
    "John Smith",
    "Main Street 10",
    "john@test.com",
    "123456789",
    "password123",
    "15.03.2000"
)

company_customer = CompanyCustomer(
    "ABC GmbH",
    "Business Street 5",
    "office@abc.com",
    "987654321",
    "company123",
    "123456789"
)

private_customer.save(storage)
company_customer.save(storage)

print("Customers saved")


print("\n--- SAVE PRODUCTS ---")

book = Book(
    "Python Basics",
    29.99,
    "John Author",
    350
)

electronics = Electronics(
    "Dell Laptop",
    1200.99,
    "Dell",
    2
)

clothing = Clothing(
    "T-Shirt",
    19.99,
    "L",
    "Black"
)


book.save(storage)
electronics.save(storage)
clothing.save(storage)

print("Products saved")


print("\n--- PRIVATE CUSTOMER AGE ---")

print(
    private_customer.calculate_age()
)


print("\n--- LOAD ALL PRIVATE CUSTOMERS ---")

print(
    PrivateCustomer.load_all(storage)
)


print("\n--- LOAD ALL COMPANY CUSTOMERS ---")

print(
    CompanyCustomer.load_all(storage)
)


print("\n--- LOAD ALL BOOKS ---")

print(
    Book.load_all(storage)
)


print("\n--- LOAD ALL ELECTRONICS ---")

print(
    Electronics.load_all(storage)
)


print("\n--- LOAD ALL CLOTHING ---")

print(
    Clothing.load_all(storage)
)

storage.disconnect()