"""
This class represents a company customer.
"""

from shop_models.customers.customer import Customer
from utils.validator import Validator


class CompanyCustomer(Customer):

    def __init__(
            self,
            name,
            address,
            email,
            phone,
            password,
            company_number
    ):

        super().__init__(
            name,
            address,
            email,
            phone,
            password
        )

        self.set_company_number(
            company_number
        )

    # Company customers get a 5% discount on the order total.
    def discount_rate(self):
        return 0.05

    # GETTERS

    def get_company_number(self):
        return self.company_number

    # SETTERS

    def set_company_number(
            self,
            company_number
    ):

        if not Validator.validate_company_number(
                company_number
        ):
            raise ValueError(
                "Invalid company number"
            )

        self.company_number = company_number

    # DATABASE METHODS

    def save(
            self,
            storage
    ):

        query = """
        INSERT INTO company_customers
        (
            name,
            address,
            email,
            phone,
            password,
            company_number
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            self.name,
            self.address,
            self.email,
            self.phone,
            self.password,
            self.company_number
        )

        storage.execute_query(
            query,
            values
        )

    @staticmethod
    def load(
            storage,
            email
    ):

        query = """
        SELECT *
        FROM company_customers
        WHERE email = %s
        """

        return storage.execute_query(
            query,
            (email,)
        ).fetchone()

    @staticmethod
    def load_all(storage):

        query = """
        SELECT *
        FROM company_customers
        """

        return storage.execute_query(
            query
        ).fetchall()
