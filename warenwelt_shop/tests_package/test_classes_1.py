"""
This file tests all classes.
It creates one private customer
and one company customer.
"""

from shop_models.customers.private_customer import PrivateCustomer
from shop_models.customers.company_customer import CompanyCustomer


def test_classes():
    private_customer = PrivateCustomer(
        "John Smith",
        "Main Street 10",
        "john@test.com",
        "123456789",
        "password123",
        "15.03.1995"
    )

    company_customer = CompanyCustomer(
        "ABC Company",
        "Business Street 5",
        "office@abc.com",
        "987654321",
        "company123",
        "123456789"
    )

    print(private_customer.get_name())
    print(private_customer.get_birthdate())

    print(company_customer.get_name())
    print(company_customer.get_company_number())
    print(company_customer.get_email())


