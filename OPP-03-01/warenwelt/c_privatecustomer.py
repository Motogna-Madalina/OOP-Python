from b_customer import Customer
from a_validator import Validator


class PrivatCustomer(Customer):

    def __init__(
            self,
            name,
            adresse,
            email,
            phone,
            password,
            birthdate):

        super().__init__(
            name,
            adresse,
            email,
            phone,
            password
        )

        if not Validator.validate_birthdate(
                birthdate):
            raise ValueError(
                "Ungültiges Geburtsdatum"
            )

        self.birthdate = birthdate

    def alter_berechnen(self):

        jahr = int(
            self.birthdate[-4:]
        )

        return 2025 - jahr