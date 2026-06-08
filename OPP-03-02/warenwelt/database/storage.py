import mysql.connector
from mysql.connector import Error

from warenwelt.models.electronics import Electronics
from warenwelt.models.clothing import Clothing
from warenwelt.models.book import Book


class Storage:

    def __init__(self):

        self.database_name = "onlineshop"
        self.connection = None

    # =====================================
    # DATABASE CONNECTION
    # =====================================

    def connect(self):

        try:

            self.connection = mysql.connector.connect(
                host="localhost",
                user="shopuser",
                password="Shop123!",
                database=self.database_name,
                use_pure=True
            )

            if self.connection.is_connected():

                print("DATABASE CONNECTED")

        except Error as e:

            print(f"DATABASE ERROR: {e}")

    def disconnect(self):

        try:

            if self.connection and self.connection.is_connected():

                self.connection.close()

                print("DATABASE DISCONNECTED")

        except Error as e:

            print(f"DATABASE ERROR: {e}")

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

    # =====================================
    # ELECTRONICS
    # =====================================

    def save_electronics(self, electronics):

        try:

            cursor = self.connection.cursor()

            sql = """
            INSERT INTO Electronics
            (name, price, weight, brand, warranty_years)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                electronics.name,
                electronics.price,
                electronics.weight,
                electronics.brand,
                electronics.warranty_years
            )

            cursor.execute(sql, values)

            self.connection.commit()

            print("ELECTRONICS SAVED")

        except Error as e:

            self.connection.rollback()

            print(f"DATABASE ERROR: {e}")

    def load_all_electronics(self):

        try:

            cursor = self.connection.cursor()

            cursor.execute("SELECT * FROM Electronics")

            return cursor.fetchall()

        except Error as e:

            print(f"DATABASE ERROR: {e}")

    # =====================================
    # CLOTHING
    # =====================================

    def save_clothing(self, clothing):

        try:

            cursor = self.connection.cursor()

            sql = """
            INSERT INTO Clothing
            (name, price, weight, size, color)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                clothing.name,
                clothing.price,
                clothing.weight,
                clothing.size,
                clothing.color
            )

            cursor.execute(sql, values)

            self.connection.commit()

            print("CLOTHING SAVED")

        except Error as e:

            self.connection.rollback()

            print(f"DATABASE ERROR: {e}")

    def load_all_clothing(self):

        try:

            cursor = self.connection.cursor()

            cursor.execute("SELECT * FROM Clothing")

            return cursor.fetchall()

        except Error as e:

            print(f"DATABASE ERROR: {e}")

    # =====================================
    # BOOKS
    # =====================================

    def save_book(self, book):

        try:

            cursor = self.connection.cursor()

            sql = """
            INSERT INTO Book
            (name, price, weight, author, page_count)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                book.name,
                book.price,
                book.weight,
                book.author,
                book.page_count
            )

            cursor.execute(sql, values)

            self.connection.commit()

            print("BOOK SAVED")

        except Error as e:

            self.connection.rollback()

            print(f"DATABASE ERROR: {e}")

    def load_all_books(self):

        try:

            cursor = self.connection.cursor()

            cursor.execute("SELECT * FROM Book")

            return cursor.fetchall()

        except Error as e:

            print(f"DATABASE ERROR: {e}")

    # =====================================
    # GENERIC PRODUCT METHODS
    # =====================================

    def save_product(self, product):

        if isinstance(product, Electronics):

            self.save_electronics(product)

        elif isinstance(product, Clothing):

            self.save_clothing(product)

        elif isinstance(product, Book):

            self.save_book(product)

        else:

            raise ValueError("Unknown product type")

    def load_all_products(self):

        return {
            "electronics": self.load_all_electronics(),
            "clothing": self.load_all_clothing(),
            "books": self.load_all_books()
        }
