from warenwelt.models.company_customer import CompanyCustomer
from warenwelt.models.electronics import Electronics
from warenwelt.models.book import Book
from warenwelt.models.shopping_cart import ShoppingCart
from warenwelt.models.order import Order

print("TEST STARTED")

customer = CompanyCustomer(
    "Firma Test",
    "Main Street 1",
    "office@test.com",
    "+436641234567",
    "secret123",
    "12345678"
)

print("CUSTOMER CREATED")

phone = Electronics(
    "iPhone",
    999.99,
    0.2,
    "Apple",
    2
)

book = Book(
    "Python Programming",
    39.99,
    0.5,
    "Max Mustermann",
    400
)

print("PRODUCTS CREATED")

cart = ShoppingCart(customer)

cart.add_product(phone)
cart.add_product(book)

print("PRODUCTS ADDED")

print("\nCART TOTAL:")
print(cart.calculate_total())

order = Order(
    customer,
    cart.products
)

print("\nORDER TOTAL:")
print(order.calculate_total())

order.create_invoice()

print("\nINVOICE CREATED")

print("TEST FINISHED")