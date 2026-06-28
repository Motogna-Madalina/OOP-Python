from datetime import datetime, date

from models_shop.customers.customer import Customer
from utils.validator import Validator
from exceptions.shop_error import ShopError


class PrivateCustomer(Customer):


    def __init__(self, name, address, email, phone, password, birthdate):
        super().__init__(name, address, email, phone, password)

        self._birthdate = None
        self.set_birthdate(birthdate)

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