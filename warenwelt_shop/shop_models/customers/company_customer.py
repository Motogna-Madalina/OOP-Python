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

    # ==================================================================
    # >>> SAVE THIS COMPANY INTO MYSQL <<<
    # This WRITES the company customer as a new row (INSERT).
    # This is the part that really saves the data in the database.
    # ==================================================================

    def save(
            self,
            storage
    ):

        query = """
        INSERT INTO company_customers      -- add a new row
        (
            name,                          -- columns to fill
            address,
            email,
            phone,
            password,
            company_number
        )
        VALUES (%s,%s,%s,%s,%s,%s)         -- one value per column
        """

        values = (                         # the real values, same order
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

    # ==================================================================
    # >>> READ COMPANY CUSTOMERS FROM MYSQL <<<
    # load()      -> get ONE company by email   (one row)
    # load_all()  -> get ALL company customers  (a list of rows)
    # ==================================================================

    @staticmethod
    def load(
            storage,
            email
    ):

        query = """
        SELECT *
        FROM company_customers
        WHERE email = %s                   -- only the company with this email
        """

        return storage.execute_query(
            query,
            (email,)                       # value for %s (safe)
        ).fetchone()                       # one row only

    @staticmethod
    def load_all(storage):

        query = """
        SELECT *
        FROM company_customers             -- every company customer
        """

        return storage.execute_query(
            query
        ).fetchall()                       # a list of rows