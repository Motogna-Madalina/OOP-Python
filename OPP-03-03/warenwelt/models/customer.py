from abc import ABC, abstractmethod

from warenwelt.utils.validator import Validator


class Customer(ABC):

    next_id = 1

    def __init__(
            self,
            name,
            address,
            email,
            phone,
            password):

        if not Validator.validate_name(name):
            raise ValueError("Invalid name")

        if not Validator.validate_address(address):
            raise ValueError("Invalid address")

        if not Validator.validate_email(email):
            raise ValueError("Invalid email")

        if not Validator.validate_phone(phone):
            raise ValueError("Invalid phone number")

        self.id = Customer.next_id
        Customer.next_id += 1

        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.password = password

    # =====================================
    # GETTERS
    # =====================================

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.phone

    def get_password(self):
        return self.password

    # =====================================
    # SETTERS
    # =====================================

    def set_name(self, name):
        if Validator.validate_name(name):
            self.name = name

    def set_address(self, address):
        if Validator.validate_address(address):
            self.address = address

    def set_email(self, email):
        if Validator.validate_email(email):
            self.email = email

    def set_phone(self, phone):
        if Validator.validate_phone(phone):
            self.phone = phone

    def set_password(self, password):
        self.password = password

    # Metodo abstracto: cada subclase DEBE definir su propio __str__.
    # Esto es lo que impide instanciar Customer directamente.
    @abstractmethod
    def __str__(self):
        pass

    # =====================================
    # DATABASE METHODS (CRUD)
    # =====================================

    @staticmethod
    def save(storage, customer, customer_type):

        cursor = storage.query(
            """
            INSERT INTO Customers
            (type, name, address, email, phone, password)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                customer_type,
                customer.name,
                customer.address,
                customer.email,
                customer.phone,
                customer.password
            )
        )

        return cursor.lastrowid

    @staticmethod
    def load(storage, customer_id):

        cursor = storage.query(
            "SELECT * FROM Customers WHERE id_customer = %s",
            (customer_id,)
        )

        return cursor.fetchone()

    @staticmethod
    def load_all(storage):

        cursor = storage.query("SELECT * FROM Customers")

        return cursor.fetchall()

    @staticmethod
    def update(storage, customer_id, customer):

        storage.query(
            """
            UPDATE Customers
            SET
                name=%s,
                address=%s,
                email=%s,
                phone=%s,
                password=%s
            WHERE id_customer=%s
            """,
            (
                customer.name,
                customer.address,
                customer.email,
                customer.phone,
                customer.password,
                customer_id
            )
        )

        print("CUSTOMER UPDATED")

    @staticmethod
    def delete(storage, customer_id):

        storage.query(
            "DELETE FROM Customers WHERE id_customer = %s",
            (customer_id,)
        )

        print("CUSTOMER DELETED")