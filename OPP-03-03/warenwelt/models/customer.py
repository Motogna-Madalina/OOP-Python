from binascii import Error

from warenwelt.utils.validator import Validator


class Customer:

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

    # Getters

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

    # Setters

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

    def __str__(self):

        return (
            f"Customer: {self.name} | "
            f"Email: {self.email} | "
            f"Phone: {self.phone}"
        )

    # =====================================
    # CUSTOMER METHODS
    # =====================================

    def save_customer(self, customer):

        try:

            cursor = self.connection.cursor()

            sql = """
            INSERT INTO Customers
            (name, address, email, phone, password)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                customer.name,
                customer.address,
                customer.email,
                customer.phone,
                customer.password
            )

            cursor.execute(sql, values)

            self.connection.commit()

            print("CUSTOMER SAVED")

        except Error as e:

            self.connection.rollback()

            print(f"DATABASE ERROR: {e}")

    def load_customer(self, customer_id):

        try:

            cursor = self.connection.cursor()

            sql = """
            SELECT *
            FROM Customers
            WHERE id_customer = %s
            """

            cursor.execute(sql, (customer_id,))

            return cursor.fetchone()

        except Error as e:

            print(f"DATABASE ERROR: {e}")

    def load_all_customers(self):

        try:

            cursor = self.connection.cursor()

            sql = """
            SELECT *
            FROM Customers
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Error as e:

            print(f"DATABASE ERROR: {e}")

    def update_customer(self, customer):

        try:

            cursor = self.connection.cursor()

            sql = """
            UPDATE Customers
            SET
                name=%s,
                address=%s,
                email=%s,
                phone=%s,
                password=%s
            WHERE id_customer=%s
            """

            values = (
                customer.name,
                customer.address,
                customer.email,
                customer.phone,
                customer.password,
                customer.id_customer
            )

            cursor.execute(sql, values)

            self.connection.commit()

            print("CUSTOMER UPDATED")

        except Error as e:

            self.connection.rollback()

            print(f"DATABASE ERROR: {e}")

    def delete_customer(self, customer_id):

        try:

            cursor = self.connection.cursor()

            sql = """
            DELETE FROM Customers
            WHERE id_customer = %s
            """

            cursor.execute(sql, (customer_id,))

            self.connection.commit()

            print("CUSTOMER DELETED")

        except Error as e:

            self.connection.rollback()

            print(f"DATABASE ERROR: {e}")    