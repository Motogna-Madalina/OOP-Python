from warenwelt.models.customer import Customer
from warenwelt.utils.validator import Validator


class CompanyCustomer(Customer):

    def __init__(
            self,
            name,
            address,
            email,
            phone,
            password,
            company_id):

        super().__init__(
            name,
            address,
            email,
            phone,
            password
        )

        if not Validator.validate_company_id(company_id):
            raise ValueError(
                "Invalid company ID"
            )

        self.company_id = company_id

    def validate_company(self):

        return Validator.validate_company_id(
            self.company_id
        )

    def get_company_id(self):

        return self.company_id

    def set_company_id(self, company_id):

        if Validator.validate_company_id(company_id):
            self.company_id = company_id

    def __str__(self):

        return (
            f"Company Customer: {self.name} | "
            f"Email: {self.email} | "
            f"Company ID: {self.company_id}"
        )
# =====================================
# DATABASE METHODS
# =====================================

@staticmethod
def save(storage, customer):

    sql = """
    INSERT INTO CompanyCustomers
    (name, address, email, phone, password, company_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        customer.name,
        customer.address,
        customer.email,
        customer.phone,
        customer.password,
        customer.company_id
    )

    storage.query(sql, values)

@staticmethod
def load(storage, customer_id):

    cursor = storage.query(
        """
        SELECT *
        FROM CompanyCustomers
        WHERE id_customer = %s
        """,
        (customer_id,)
    )

    return cursor.fetchone()

@staticmethod
def load_all(storage):

    cursor = storage.query(
        "SELECT * FROM CompanyCustomers"
    )

    return cursor.fetchall()