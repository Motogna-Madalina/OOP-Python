from warenwelt.database.storage import Storage
from warenwelt.models.customer import Customer

print("TEST STARTED")

storage = Storage()
storage.connect()

# CREATE
customer = Customer(
    "Lina",
    "Main Street 1",
    "lina@test.com",
    "+436641234567",
    "secret123"
)

storage.save_customer(customer)

print("\nCUSTOMER CREATED")

# READ ONE
customer_data = storage.load_customer(1)
print(customer_data)

# READ ALL
print("\nALL CUSTOMERS:")
for customer in storage.load_all_customers():
    print(customer)

# UPDATE
customer.id_customer = 1
customer.name = "Alexander"
customer.address = "New Street 10"

storage.update_customer(customer)

print("\nUPDATED CUSTOMER:")
print(storage.load_customer(1))

# DELETE
storage.delete_customer(1)

print("\nAFTER DELETE:")
for customer in storage.load_all_customers():
    print(customer)

storage.disconnect()

print("\nTEST FINISHED")