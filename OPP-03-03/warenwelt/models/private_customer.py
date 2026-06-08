from warenwelt.models.customer import Customer
from warenwelt.utils.validator import Validator


class PrivateCustomer(Customer):

    def __init__(
            self,
            name,
            address,
            email,
            phone,
            password,
            birthdate):

        super().__init__(
            name,
            address,
            email,
            phone,
            password
        )

        if not Validator.validate_birthdate(
                birthdate):
            raise ValueError(
                "Invalid birthdate"
            )

        self.birthdate = birthdate

    def calculate_age(self):

        birth_year = int(
            self.birthdate[-4:]
        )

        return 2025 - birth_year

    def get_birthdate(self):

        return self.birthdate

    def set_birthdate(self, birthdate):

        if Validator.validate_birthdate(
                birthdate):
            self.birthdate = birthdate

    def __str__(self):

        return (
            f"Private Customer: {self.name} | "
            f"Email: {self.email} | "
            f"Birthdate: {self.birthdate}"
        )
    
# =====================================
# DATABASE METHODS
# =====================================

@staticmethod
def save(storage, customer):

    sql = """
    INSERT INTO PrivateCustomers
    (name, address, email, phone, password, birthdate)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        customer.name,
        customer.address,
        customer.email,
        customer.phone,
        customer.password,
        customer.birthdate
    )

    storage.query(sql, values)

@staticmethod
def load(storage, customer_id):

    cursor = storage.query(
        """
        SELECT *
        FROM PrivateCustomers
        WHERE id_customer = %s
        """,
        (customer_id,)
    )

    return cursor.fetchone()

@staticmethod
def load_all(storage):

    cursor = storage.query(
        "SELECT * FROM PrivateCustomers"
    )

    return cursor.fetchall()
    