"""
This script checks if everything we wrote works together.
It does NOT use the database, so you can run it anywhere.


Run it from the project root with:
    python -m tests_package.test_shop

It prints every step:
- Validator: good and bad values.
- Customers: a private and a company customer.
- Products: a book, an electronic item and a piece of clothing.
- Shopping flow: load products, see the total, remove one, checkout
  into an order (company gets -5%) and create the invoice file.

Resumen (en español):
Va imprimiendo cada paso para ver a simple vista que todo funciona:
validador, clientes, productos y el flujo de carrito -> orden -> factura.
"""

import os
import sys



# Print special characters (ä, ö, ü, ...) correctly, even on a Windows
# terminal that uses a non-UTF-8 code page by default.
sys.stdout.reconfigure(encoding="utf-8")

from utils.validator import Validator

from shop_models.customers.private_customer import PrivateCustomer
from shop_models.customers.company_customer import CompanyCustomer

from shop_models.products.book import Book
from shop_models.products.electronics import Electronics
from shop_models.products.clothing import Clothing

from orders.shopping_cart import ShoppingCart


# ==================================================================
# 1) VALIDATOR
# ==================================================================

print("\n========== VALIDATOR ==========")

print("Email 'office@abc.com' ->", Validator.validate_email("office@abc.com"))
print("Email 'not-an-email'   ->", Validator.validate_email("not-an-email"))
print("Phone '987654321'      ->", Validator.validate_phone("987654321"))
print("Phone '12'             ->", Validator.validate_phone("12"))
print("Name  'Anna Müller'    ->", Validator.validate_name("Anna Müller"))
print("Name  'Anna123'        ->", Validator.validate_name("Anna123"))
print("Date  '01.01.1990'     ->", Validator.validate_birthdate("01.01.1990"))
print("Date  '1990-01-01'     ->", Validator.validate_birthdate("1990-01-01"))


# ==================================================================
# 2) CUSTOMERS
# ==================================================================

print("\n========== CUSTOMERS ==========")

private = PrivateCustomer(
    "Anna Müller", "Main Street 1", "anna@web.de",
    "123456789", "pw1234", "15.05.1990"
)
print(f"Private customer: {private.get_name()}, born {private.get_birthdate()}")

company = CompanyCustomer(
    "ABC GmbH", "Business Street 5", "office@abc.com",
    "987654321", "company123", "123456789"
)
print(f"Company customer: {company.get_name()}, "
      f"company number {company.get_company_number()}")


# ==================================================================
# 3) PRODUCTS
# ==================================================================

print("\n========== PRODUCTS ==========")

book = Book("Clean Code", 39.99, "Robert Martin", 464)
laptop = Electronics("Dell Laptop", 1200.99, "Dell", 2)
jacket = Clothing("Jacket", 89.99, "XL", "Green")

print(f"Book:        {book.get_name()} - {book.get_price()} EUR "
      f"(author: {book.get_author()})")
print(f"Electronics: {laptop.get_name()} - {laptop.get_price()} EUR "
      f"(brand: {laptop.get_brand()})")
print(f"Clothing:    {jacket.get_name()} - {jacket.get_price()} EUR "
      f"(color: {jacket.get_color()})")


# ==================================================================
# 4) SHOPPING FLOW: cart -> remove -> checkout -> invoice
# ==================================================================

print("\n========== SHOPPING FLOW ==========")

# The company customer gets a 5% discount in the final order.
cart = ShoppingCart(company)

print("\n--- LOAD PRODUCTS INTO CART ---")
for product in [book, laptop, jacket]:
    cart.add_product(product)
    print(f"Added: {product.name} - {product.price} EUR")

print(f"\nCart total (no discount): {cart.total_amount:.2f} EUR")

print("\n--- REMOVE A PRODUCT ---")
cart.remove_product(jacket)
print(f"Removed: {jacket.name}")
print(f"New cart total: {cart.total_amount:.2f} EUR")

print("\n--- CHECKOUT ---")
order = cart.checkout()
print(f"Order for: {order.customer.name}")
print(f"Order total (company -5%): {order.total_amount:.2f} EUR")

print("\n--- INVOICE ---")
order.create_invoice()
invoice_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "orders",
    "invoice.txt"
)
print(f"Invoice saved: {os.path.exists(invoice_path)} -> {invoice_path}")

print("\n========== DONE: everything ran without errors ==========")