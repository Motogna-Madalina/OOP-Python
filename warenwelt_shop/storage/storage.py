import pymysql

from exceptions.storage_error import StorageError


class Storage:


    def __init__(self):
        self.database_name = "shop_warenwelt"
        self.connection = None



    def connect(self):
        # Open the connection to the database.
        try:
            self.connection = pymysql.connect(
                host="localhost",
                user="root",
                password="Motogna6624.",
                database=self.database_name
            )
            print("Verbindung erfolgreich!")
        except pymysql.Error as error:
            raise StorageError(f"Fehler bei der Verbindung zur Datenbank: {error}")

    def disconnect(self):
        # Close the connection (only if it is open).
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
                print("Verbindung geschlossen.")
        except pymysql.Error as error:
            raise StorageError(f"Fehler beim Schließen der Verbindung: {error}")



    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # For INSERT: run the query and return the new id.
    # commit=True means confirm immediately .
    # commit=False means that the caller is then responsible for commit()/rollback().
    #

    def execute_query(self, query, values=None, commit=True):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            if commit:
                self.connection.commit()
            return cursor.lastrowid
        except pymysql.Error as error:
            self.connection.rollback()
            raise StorageError(f"Datenbankabfrage fehlgeschlagen: {error}")

        # Confirm the current transaction (all open operations at once).

    def commit(self):
        try:
            self.connection.commit()
        except pymysql.Error as error:
            raise StorageError(f"Commit fehlgeschlagen: {error}")

        # Undo every operation of the current transaction.

    def rollback(self):
        try:
            self.connection.rollback()
        except pymysql.Error as error:
            raise StorageError(f"Rollback fehlgeschlagen: {error}")



    # For SELECT: run the query and - return all rows
    #here is a query to use for see things, just select and they show us the result the name


    def fetch_query(self, query, values=None):
        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, values)
            return cursor.fetchall()
        except pymysql.Error as error:
            raise StorageError(f"Datenbankabfrage fehlgeschlagen: {error}")