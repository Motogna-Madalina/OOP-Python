from warenwelt.database.storage import Storage
from warenwelt.models.customer import Customer

print("TEST STARTED")

storage = Storage()

storage.connect()

customer = Customer(
    "Alex",
    "Main Street 1",
    "alex@test.com",
    "+436641234567",
    "secret123"
)

print("CUSTOMER CREATED")

storage.save_customer(customer)

print("\nONE CUSTOMER:")

customer_data = storage.load_customer(1)

print(customer_data)

print("\nALL CUSTOMERS:")

all_customers = storage.load_all_customers()

for customer in all_customers:
    print(customer)

storage.disconnect()

print("TEST FINISHED")