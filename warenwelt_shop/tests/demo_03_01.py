

from exceptions.shop_error import ShopError
from models_shop.customers.private_customer import PrivateCustomer
from models_shop.customers.company_customer import CompanyCustomer


#a private customer with correct data
private = PrivateCustomer(
    "Anna Müller", "Hauptstraße 1, Wien", "anna@example.com",
    "+436641234567", "geheim123", "23.04.1995"
)
print("Privatkunde:", private.get_name(), "- Alter:", private.calculate_age())

#  company with right attributes
company = CompanyCustomer(
    "Mustermann GmbH", "Industrieweg 5, Linz", "info@mustermann.at",
    "073212345678", "firmenpw99", "123456"
)
print("Firmenkunde:", company.get_name(), "- Nr:", company.get_company_id())

# e-mail ist nicht richtig -es muss ein fehler bringen
try:
    PrivateCustomer("Hans", "Weg 1", "I just write an invalid-email",
                    "12345678", "passwort1", "01.01.1990")
except ShopError as error:
    print("Fehler abgefangen:", error)

#repository test
print("Hola")

