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
            raise ValueError(
                "Invalid company ID"
            )

        self.company_id = company_id

    def validate_company(self):

        return Validator.validate_company_id(
            self.company_id
        )

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