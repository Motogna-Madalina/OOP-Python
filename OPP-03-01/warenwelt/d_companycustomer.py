from b_customer import Customer
from a_validator import Validator



class CompanyCustomer(Customer):

    def __init__(
            self,
            name,
            adresse,
            email,
            telefon,
            password,
            firmennummer):

        super().__init__(
            name,
            adresse,
            email,
            telefon,
            password
        )

        if not Validator.validate_company_id(
                firmennummer):
            raise ValueError(
                "Ungültige Firmennummer"
            )

        self.firmennummer = firmennummer

    def validate_firma(self):

        return Validator.validate_company_id(
            self.firmennummer
        )