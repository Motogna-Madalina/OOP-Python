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