from warenwelt.models.private_customer import PrivateCustomer
from warenwelt.models.company_customer import CompanyCustomer
from warenwelt.models.book import Book
from warenwelt.models.clothing import Clothing
from warenwelt.models.electronics import Electronics


def test_customers():

    p1 = PrivateCustomer(
        "John Doe",
        "Street 1",
        "john@test.com",
        "123456789",
        "password",
        "01.01.1990"
    )

    c1 = CompanyCustomer(
        "ACME GmbH",
        "Business Street 10",
        "office@acme.com",
        "987654321",
        "password",
        "12345678"
    )

    print("\n===== PRIVATE CUSTOMER =====")
    print(p1)

    print("\n===== COMPANY CUSTOMER =====")
    print(c1)


def test_products():

    print("\n===== BOOK =====")

    try:
        b1 = Book(
            "Python Basics",
            19.99,
            0.5,
            "Max Mustermann",
            350
        )
        print(b1)
    except Exception as e:
        print("BOOK ERROR:", e)

    print("\n===== CLOTHING =====")

    try:
        c1 = Clothing(
            "T-Shirt",
            24.99,
            0.3,
            "L",
            "Black"
        )
        print(c1)
    except Exception as e:
        print("CLOTHING ERROR:", e)

    print("\n===== ELECTRONICS =====")

    try:
        e1 = Electronics(
            "Laptop",
            999.99,
            2.5,
            "Lenovo",
            2
        )
        print(e1)
    except Exception as e:
        print("ELECTRONICS ERROR:", e)


if __name__ == "__main__":
    test_customers()
    test_products()