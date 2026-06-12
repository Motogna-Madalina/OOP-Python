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

    def save(
            self,
            storage
    ):

        storage.execute_query(
            """
            INSERT INTO private_customers
            (
                name,
                address,
                email,
                phone,
                password,
                birthdate
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                self.name,
                self.address,
                self.email,
                self.phone,
                self.password,
                self.birthdate
            )
        )

    @staticmethod
    def load(
            storage,
            customer_id
    ):

        return storage.execute_query(
            """
            SELECT *
            FROM private_customers
            WHERE id_private_customer=%s
            """,
            (customer_id,)
        ).fetchone()

    @staticmethod
    def load_all(storage):

        return storage.execute_query(
            """
            SELECT *
            FROM private_customers
            """
        ).fetchall()

    def update(
            self,
            storage,
            customer_id
    ):

        storage.execute_query(
            """
            UPDATE private_customers
            SET
                name=%s,
                address=%s,
                email=%s,
                phone=%s,
                password=%s,
                birthdate=%s
            WHERE id_private_customer=%s
            """,
            (
                self.name,
                self.address,
                self.email,
                self.phone,
                self.password,
                self.birthdate,
                customer_id
            )
        )

    def delete(
            self,
            storage,
            customer_id
    ):

        storage.execute_query(
            """
            DELETE FROM private_customers
            WHERE id_private_customer=%s
            """,
            (customer_id,)
        )