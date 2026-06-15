"""
This class represents a private customer.
"""

from datetime import datetime
from shop_models.customers.customer import Customer
from utils.validator import Validator


class PrivateCustomer(Customer):

    def __init__(
            self,
            name,
            address,
            email,
            phone,
            password,
            birthdate
    ):

        super().__init__(
            name,
            address,
            email,
            phone,
            password
        )

        self.set_birthdate(
            birthdate
        )

    # GETTERS

    def get_birthdate(self):
        return self.birthdate

    # SETTERS

    def set_birthdate(
            self,
            birthdate
    ):

        if not Validator.validate_birthdate(
                birthdate
        ):
            raise ValueError(
                "Invalid birthdate"
            )

        self.birthdate = birthdate

    # PRIVATE CUSTOMER METHODS

    def calculate_age(self):

        birthdate = datetime.strptime(
            self.birthdate,
            "%d.%m.%Y"
        )

        return (
            datetime.now().year
            - birthdate.year
        )

    # DATABASE METHODS

    # ==================================================================
    # >>> SAVE THIS CUSTOMER INTO MYSQL <<<
    # This WRITES the customer as a new row (INSERT).
    # This is the part that really saves the data in the database.
    # ==================================================================

    def save(
            self,
            storage
    ):

        storage.execute_query(
            """
            INSERT INTO private_customers     -- add a new row
            (
                name,                         -- columns to fill
                address,
                email,
                phone,
                password,
                birthdate
            )
            VALUES (%s,%s,%s,%s,%s,%s)        -- one value per column
            """,
            (                                 # the real values, same order
                self.name,
                self.address,
                self.email,
                self.phone,
                self.password,
                self.birthdate
            )
        )

    # ==================================================================
    # >>> READ CUSTOMERS FROM MYSQL <<<
    # load()      -> get ONE customer by email  (one row)
    # load_all()  -> get ALL private customers  (a list of rows)
    # ==================================================================

    @staticmethod
    def load(
            storage,
            email
    ):

        return storage.execute_query(
            """
            SELECT *
            FROM private_customers
            WHERE email=%s             -- only the customer with this email
            """,
            (email,)                   # value for %s (safe)
        ).fetchone()                   # one row only

    @staticmethod
    def load_all(storage):

        return storage.execute_query(
            """
            SELECT *
            FROM private_customers     -- every private customer
            """
        ).fetchall()                   # a list of rows