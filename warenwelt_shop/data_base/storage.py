"""
This class manages the database connection.

It is responsible for:
- Connecting to the database
- Disconnecting from the database
- Executing SQL queries
"""

import mysql.connector


class Storage:

    # ==================================
    # CONSTRUCTOR
    # ==================================

    def __init__(
            self,
            host,
            user,
            password,
            database,
            port=3306
    ):

        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

        self.connection = None

    # ==================================
    # DATABASE CONNECTION
    # ==================================

    def connect(self):

        try:

            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                use_pure=True   # evita el crash de la extensión C con Python 3.14
            )

            print("Database connected")

        except mysql.connector.Error as error:

            print(
                f"Connection error: {error}"
            )

            # Re-raise so the program stops here instead of failing
            # later with a confusing "NoneType has no attribute cursor".
            raise

    def disconnect(self):

        if self.connection:

            self.connection.close()

            print("Database disconnected")

    # ==================================
    # QUERY METHODS
    # ==================================

    def execute_query(
            self,
            query,
            values=None
    ):

        try:

            # buffered=True reads the whole result set immediately, so a
            # SELECT cursor that isn't fully consumed/closed doesn't block
            # the next query with "Unread result found".
            cursor = self.connection.cursor(buffered=True)

            if values:

                cursor.execute(
                    query,
                    values
                )

            else:

                cursor.execute(query)

            self.connection.commit()

            return cursor

        except mysql.connector.Error as error:

            print(
                f"Database error: {error}"
            )

            return None
