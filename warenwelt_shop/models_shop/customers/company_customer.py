from models_shop.customers.customer import Customer
from utils.validator import Validator
from exceptions.shop_error import ShopError


class CompanyCustomer(Customer):


    def __init__(self, name, address, email, phone, password, company_id):
        super().__init__(name, address, email, phone, password)

        self._company_id = None
        self.set_company_id(company_id)

    def get_company_id(self):
        return self._company_id

    def set_company_id(self, company_id):
        if not Validator.validate_company_id(company_id):
            raise ShopError(f"Ungültige Firmennummer (5-15 Ziffern): {company_id}")
        self._company_id = company_id