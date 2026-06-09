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
    # GENERIC QUERY METHOD
    # =====================================

    def query(self, sql, values=None):

        try:

            cursor = self.connection.cursor()

            if values is not None:

                cursor.execute(sql, values)

            else:

                cursor.execute(sql)

            self.connection.commit()

            return cursor

        except Error as e:

            self.connection.rollback()

            print(f"DATABASE ERROR: {e}")

