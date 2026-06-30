from datetime import datetime, date

from models_shop.customers.customer import Customer
from utils.validator import Validator
from exceptions.shop_error import ShopError


class PrivateCustomer(Customer):


    def __init__(self, name, address, email, phone, password, birthdate):
        super().__init__(name, address, email, phone, password)

        self._birthdate = None
        self.set_birthdate(birthdate)

    def get_type(self):
        return "private"

    def get_birthdate(self):
        return self._birthdate

    def set_birthdate(self, birthdate):
        if not Validator.validate_birthdate(birthdate):
            raise ShopError(f"Ungültiges Geburtsdatum (Format TT.MM.JJJJ): {birthdate}")
        self._birthdate = birthdate

    def calculate_age(self):
        birth = datetime.strptime(self._birthdate, "%d.%m.%Y").date()
        today = date.today()
        age = today.year - birth.year

        # If the birthday did not happen yet this year, subtract 1.
        if today.month < birth.month:
            age = age - 1
        elif today.month == birth.month and today.day < birth.day:
            age = age - 1
        return age

#=====================================================================================================
    #SAVE
    def save(self, storage):


        try:

            customer_id = self.save_base(storage)

            query = """
                    INSERT INTO private_customer (customer_id, birthdate)
                    VALUES (%s, %s) \
                    """

            storage.execute_query(
                query,
                (
                    customer_id,
                    datetime.strptime(
                        self.get_birthdate(),
                        "%d.%m.%Y"
                    ).date()
                ),
                commit=False
            )

            storage.commit()
        except Exception:

            #if anything went wrong - wer make undo for BOTH inserts and there is no orphan customer
            storage.rollback()
            raise

        self._id = customer_id
        print(f"Kunde {self.get_name()} wurde gespeichert (ID {customer_id}).")
