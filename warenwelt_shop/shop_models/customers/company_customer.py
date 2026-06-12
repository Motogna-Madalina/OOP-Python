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
            customer_id
    ):

        query = """
        SELECT *
        FROM company_customers
        WHERE id_company_customer = %s
        """

        return storage.execute_query(
            query,
            (customer_id,)
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

    def update(
            self,
            storage,
            customer_id
    ):

        query = """
        UPDATE company_customers
        SET
            name=%s,
            address=%s,
            email=%s,
            phone=%s,
            password=%s,
            company_number=%s
        WHERE id_company_customer=%s
        """

        values = (
            self.name,
            self.address,
            self.email,
            self.phone,
            self.password,
            self.company_number,
            customer_id
        )

        storage.execute_query(
            query,
            values
        )

    def delete(
            self,
            storage,
            customer_id
    ):

        query = """
        DELETE FROM company_customers
        WHERE id_company_customer=%s
        """

        storage.execute_query(
            query,
            (customer_id,)
        )