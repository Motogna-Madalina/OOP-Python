from utils.validator import Validator
from exceptions.shop_error import ShopError


class Customer:

    #_id_counter = 0 #how it would bee to make the auto-generiert number
    def __init__(self, name, address, email, phone, password):

        self._id = None
        #Customer._id_counter = Customer._id_counter + 1
        #self._id = Customer._id_counter
        #I will not make this because I will use AUTO_INCREMENT in MySql
        self._name = None
        self._address = None
        self._email = None
        self._phone = None
        self._password = None

        self.set_name(name)
        self.set_address(address)
        self.set_email(email)
        self.set_phone(phone)
        self.set_password(password)


    def get_id(self):
        return self._id

    #name---------------------------------------------------
    def get_name(self):
        return self._name

    def set_name(self, name):
        if not Validator.validate_name(name):
            raise ShopError(f"Ungültiger Name: {name}")
        self._name = name

    #adress----------------------------------------------------
    def get_address(self):
        return self._address

    def set_address(self, address):
        if not Validator.validate_address(address):
            raise ShopError(f"Ungültige Adresse: {address}")
        self._address = address

    #email------------------------------------------------------
    def get_email(self):
        return self._email

    def set_email(self, email):
        if not Validator.validate_email(email):
            raise ShopError(f"Ungültige E-Mail-Adresse: {email}")
        self._email = email

    #phone-------------------------------------------------------
    def get_phone(self):
        return self._phone

    def set_phone(self, phone):
        if not Validator.validate_phone(phone):
            raise ShopError(f"Ungültige Telefonnummer: {phone}")
        self._phone = phone

    #password------------------------------------------------------
    def get_password(self):
        return self._password

    def set_password(self, password):
        if not Validator.validate_password(password):
            raise ShopError("Passwort muss mindestens 8 Zeichen haben.")
        self._password = password



    #====================================================================================================



    # SAVE BASE CUSTOMER (a half of it)
    #______________________________________________________________________________
    def save_base(self, storage):

        query = """
        INSERT INTO customer (name, address, email, phone, password)
        VALUES (%s, %s, %s, %s, %s)
        """


        #commit=Fals this INSERT ist only the first half of the customer
        #we let the transaction open and we will make commit at the end

        return storage.execute_query(
            query,
            (
                self.get_name(),
                self.get_address(),
                self.get_email(),
                self.get_phone(),
                self.get_password()
            ),
            commit=False
        )




    @staticmethod
    def load(storage, customer_id):
        from models_shop.customers.private_customer import PrivateCustomer
        from models_shop.customers.company_customer import CompanyCustomer

        #----------------------------------------------------------------
        # CUSTOMER


        query = """
                SELECT *
                FROM customer
                WHERE id = %s \
                """

        result = storage.fetch_query(query, (customer_id,))

        if not result:
            return None

        customer = result[0]

        #----------------------------------------------------------------
        # PRIVATE CUSTOMER


        query = """
                SELECT *
                FROM private_customer
                WHERE customer_id = %s \
                """

        result = storage.fetch_query(query, (customer_id,))

        if result:
            private_customer = result[0]

            customer_object = PrivateCustomer(
                customer["name"],
                customer["address"],
                customer["email"],
                customer["phone"],
                customer["password"],
                private_customer["birthdate"].strftime("%d.%m.%Y")
            )

            customer_object._id = customer["id"]

            return customer_object

        #----------------------------------------------------------------
        # COMPANY CUSTOMER


        query = """
                SELECT *
                FROM company_customer
                WHERE customer_id = %s \
                """

        result = storage.fetch_query(query, (customer_id,))

        if result:
            company_customer = result[0]

            customer_object = CompanyCustomer(
                customer["name"],
                customer["address"],
                customer["email"],
                customer["phone"],
                customer["password"],
                company_customer["company_id"]
            )

            customer_object._id = customer["id"]

            return customer_object

        return None

    @staticmethod
    def load_all(storage):

        query = """
        SELECT id
        FROM customer
        ORDER BY id
        """

        results = storage.fetch_query(query)

        customers = []

        for row in results:

            customer = Customer.load(storage, row["id"])

            if customer:
                customers.append(customer)

        return customers