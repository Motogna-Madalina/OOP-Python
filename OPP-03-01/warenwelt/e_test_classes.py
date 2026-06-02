from c_privatecustomer import PrivatCustomer
from d_companycustomer import CompanyCustomer


print("=== PrivatCustomer ===")

p1 = PrivatCustomer(
    "Madalina Motogna",
    "Hauptstraße 1",
    "madalina@test.com",
    "+436641234567",
    "pass123",
    "01.05.1997"
)

print("ID:", p1.id)
print("Name:", p1.get_name())
print("Adresse:", p1.get_adresse())
print("Email:", p1.get_email())
print("Telefon:", p1.get_phone())
print("Alter:", p1.alter_berechnen())


print("\n=== CompanyCustomer ===")

f1 = CompanyCustomer(
    "Test Firma",
    "Industriestraße 10",
    "firma@test.com",
    "+43123456789",
    "firma123",
    "123456789"
)

print("ID:", f1.id)
print("Name:", f1.get_name())
print("Firmennummer:", f1.firmennummer)
print("Firmennummer gültig:",
      f1.validate_firma())