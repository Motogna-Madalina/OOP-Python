"""
This file tests the shopping cart flow:
add products, calculate the total, checkout into an
order and create the invoice file.
"""

from orders.shopping_cart import ShoppingCart

from shop_models.customers.company_customer import CompanyCustomer

from shop_models.products.book import Book
from shop_models.products.electronics import Electronics
from shop_models.products.clothing import Clothing


# ==================================
# CUSTOMER
# ==================================

customer = CompanyCustomer(
    "ABC GmbH",
    "Business Street 5",
    "office@abc.com",
    "987654321",
    "company123",
    "123456789"
)


# ==================================
# SHOPPING CART
# ==================================

cart = ShoppingCart(customer)

print("\n--- ADD PRODUCTS TO CART ---")

book = Book("Clean Code", 39.99, "Robert Martin", 464)
laptop = Electronics("Dell Laptop", 1200.99, "Dell", 2)
jacket = Clothing("Jacket", 89.99, "XL", "Green")

cart.add_product(book)
print(f"Added: {book.name} - {book.price} EUR")

cart.add_product(laptop)
print(f"Added: {laptop.name} - {laptop.price} EUR")

cart.add_product(jacket)
print(f"Added: {jacket.name} - {jacket.price} EUR")


print("\n--- CART TOTAL ---")
print(f"Total (no discount): {cart.total_amount:.2f} EUR")


# ==================================
# REMOVE A PRODUCT
# ==================================

print("\n--- REMOVE PRODUCT ---")

cart.remove_product(jacket)
print(f"Removed: {jacket.name}")
print(f"New total: {cart.total_amount:.2f} EUR")


# ==================================
# CHECKOUT + INVOICE
# ==================================

print("\n--- CHECKOUT ---")

order = cart.checkout()
print(f"Order created for: {order.customer.name}")
print(f"Order total (company -5%): {order.total_amount:.2f} EUR")

order.create_invoice()
print("Invoice saved to invoice.txt")