from datetime import datetime
 
from warenwelt.models.customer import Customer
from warenwelt.utils.validator import Validator
 
 
class PrivateCustomer(Customer):
 
    def __init__(
            self,
            name,
            address,
            email,
            phone,
            password,
            birthdate):
 
        super().__init__(
            name,
            address,
            email,
            phone,
            password
        )
 
        if not Validator.validate_birthdate(birthdate):
            raise ValueError("Invalid birthdate")
 
        self.birthdate = birthdate
 
    def calculate_age(self):
 
        birth_year = int(self.birthdate[-4:])
 
        return datetime.now().year - birth_year
 
    def get_birthdate(self):
        return self.birthdate
 
    def set_birthdate(self, birthdate):
        if Validator.validate_birthdate(birthdate):
            self.birthdate = birthdate
 
    def __str__(self):
        return (
            f"Private Customer: {self.name} | "
            f"Email: {self.email} | "
            f"Birthdate: {self.birthdate}"
        )
 
    # =====================================
    # DATABASE METHODS (CRUD)
    # =====================================
 
    @staticmethod
    def save(storage, private):
 
        new_id = Customer.save(storage, private, "private")
 
        storage.query(
            """
            INSERT INTO PrivateCustomers (id_customer, birthdate)
            VALUES (%s, %s)
            """,
            (new_id, private.birthdate)
        )
 
        print("PRIVATE CUSTOMER SAVED")
 
        return new_id
 
    @staticmethod
    def load(storage, id_customer):
 
        cursor = storage.query(
            """
            SELECT c.*, p.birthdate
            FROM Customers c
            JOIN PrivateCustomers p ON c.id_customer = p.id_customer
            WHERE c.id_customer = %s
            """,
            (id_customer,)
        )
 
        return cursor.fetchone()
 
    @staticmethod
    def load_all(storage):
 
        cursor = storage.query(
            """
            SELECT c.*, p.birthdate
            FROM Customers c
            JOIN PrivateCustomers p ON c.id_customer = p.id_customer
            """
        )
 
        return cursor.fetchall()
 