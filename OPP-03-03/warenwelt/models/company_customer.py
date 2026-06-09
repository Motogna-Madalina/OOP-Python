from warenwelt.models.customer import Customer
from warenwelt.utils.validator import Validator
 
 
class CompanyCustomer(Customer):
 
    def __init__(
            self,
            name,
            address,
            email,
            phone,
            password,
            company_id):
 
        super().__init__(
            name,
            address,
            email,
            phone,
            password
        )
 
        if not Validator.validate_company_id(company_id):
            raise ValueError("Invalid company ID")
 
        self.company_id = company_id
 
    def validate_company(self):
        return Validator.validate_company_id(self.company_id)
 
    def get_company_id(self):
        return self.company_id
 
    def set_company_id(self, company_id):
        if Validator.validate_company_id(company_id):
            self.company_id = company_id
 
    def __str__(self):
        return (
            f"Company Customer: {self.name} | "
            f"Email: {self.email} | "
            f"Company ID: {self.company_id}"
        )
 
    # =====================================
    # DATABASE METHODS (CRUD)
    # =====================================
 
    @staticmethod
    def save(storage, company):
 
        new_id = Customer.save(storage, company, "company")
 
        storage.query(
            """
            INSERT INTO CompanyCustomers (id_customer, company_id)
            VALUES (%s, %s)
            """,
            (new_id, company.company_id)
        )
 
        print("COMPANY CUSTOMER SAVED")
 
        return new_id
 
    @staticmethod
    def load(storage, id_customer):
 
        cursor = storage.query(
            """
            SELECT c.*, co.company_id
            FROM Customers c
            JOIN CompanyCustomers co ON c.id_customer = co.id_customer
            WHERE c.id_customer = %s
            """,
            (id_customer,)
        )
 
        return cursor.fetchone()
 
    @staticmethod
    def load_all(storage):
 
        cursor = storage.query(
            """
            SELECT c.*, co.company_id
            FROM Customers c
            JOIN CompanyCustomers co ON c.id_customer = co.id_customer
            """
        )
 
        return cursor.fetchall()
 