import mysql.connector
from mysql.connector import Error


class Storage:

    def __init__(self):

        self.database_name = "onlineshop"
        self.connection = None

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

    def save_customer(self, customer):

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

    def load_customer(self, customer_id):

        cursor = self.connection.cursor()

        sql = """
        SELECT *
        FROM Customers
        WHERE id_customer = %s
        """

        cursor.execute(sql, (customer_id,))

        return cursor.fetchone()

    def load_all_customers(self):

        cursor = self.connection.cursor()

        sql = """
        SELECT *
        FROM Customers
        """

        cursor.execute(sql)

        return cursor.fetchall()