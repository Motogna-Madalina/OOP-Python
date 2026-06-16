"""
This class manages the database connection.

It is responsible for:
- Connecting to the database
- Disconnecting from the database
- Executing SQL queries
"""

import mysql.connector


class Storage:

    # ==================================================================
    # >>> STEP 1: SAVE THE LOGIN DATA <<<
    # When we create a Storage, we only SAVE the login data here.
    # We do NOT open the database yet. There is still no connection.
    # ==================================================================

    def __init__(
            self,
            host,
            user,
            password,
            database,
            port=3306
    ):

        self.host = host            # where MySQL is
        self.user = user            # the user name
        self.password = password    # the password
        self.database = database    # the database name
        self.port = port            # the port (door) of MySQL

        self.connection = None      # no connection yet (it opens in connect())

    # ==================================================================
    # >>> STEP 2: OPEN THE CONNECTION TO MYSQL <<<
    # This is the real connection. It uses the saved login data to
    # open the database "warenwelt". If it works, it prints
    # "Database connected". If it fails, it shows the error and stops.
    # ==================================================================

    def connect(self):

        try:

            self.connection = mysql.connector.connect(   # <-- OPEN MYSQL HERE
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                use_pure=True   # evita el crash de la extensión C con Python 3.14
            )

            print("Database connected")     # success message

        except mysql.connector.Error as error:

            print(
                f"Connection error: {error}"   # something went wrong
            )

            # Re-raise so the program stops here instead of failing
            # later with a confusing "NoneType has no attribute cursor".
            raise

    # ==================================================================
    # >>> CLOSE THE CONNECTION <<<
    # When we finish, we close the database to free the resources.
    # ==================================================================

    def disconnect(self):

        if self.connection:                  # only if a connection is open

            self.connection.close()          # close it

            print("Database disconnected")

    # ==================================================================
    # >>> STEP 3: RUN SQL COMMANDS IN MYSQL <<<
    # This sends an SQL command to the database (SELECT, INSERT, etc.).
    # - "query" is the SQL text.
    # - "values" are the safe values for the %s placeholders.
    # commit() saves the change. It returns a cursor to read the result.
    # ==================================================================


    def execute_query(
            self,
            query,
            values=None
    ):

        try:

            # buffered=True reads the whole result set immediately, so a
            # SELECT cursor that isn't fully consumed/closed doesn't block
            # the next query with "Unread result found".
            cursor = self.connection.cursor(buffered=True)   # tool to run SQL

            if values:                       # if there are values for %s

                cursor.execute(
                    query,
                    values                   # safe way (stops SQL injection)
                )

            else:                            # query without values

                cursor.execute(query)

            self.connection.commit()         # SAVE the change in the database

            return cursor                    # give back the result to read

        except mysql.connector.Error as error:

            print(
                f"Database error: {error}"   # something failed in the SQL
            )

            # Re-raise so a failed INSERT/UPDATE is NEVER silent. Read
            # paths (ShopRepository._query / load_catalog) catch this and
            # fall back; register() turns it into a clear user message.
            raise


DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "Motogna6624."
DB_NAME = "warenwelt"
DB_PORT = 3306


def connect_warenwelt():
    storage = Storage(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT)
    storage.connect()
    return storage