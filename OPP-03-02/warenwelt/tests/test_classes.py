from warenwelt.models.private_customer import PrivateCustomer
from warenwelt.models.company_customer import CompanyCustomer


print("=== Private Customer ===")

p1 = PrivateCustomer(
    "Madalina Motogna",
    "Hauptstraße 1",
    "madalina@test.com",
    "+436641234567",
    "pass123",
    "01.05.1997"
)

print("ID:", p1.id)
print("Name:", p1.get_name())
print("Address:", p1.get_address())
print("Email:", p1.get_email())
print("Phone:", p1.get_phone())
print("Age:", p1.calculate_age())


print("\n=== Company Customer ===")

c1 = CompanyCustomer(
    "Test Company",
    "Industriestraße 10",
    "company@test.com",
    "+43123456789",
    "company123",
    "123456789"
)

print("ID:", c1.id)
print("Name:", c1.get_name())
print("Company ID:", c1.get_company_id())
print("Company Valid:", c1.validate_company())