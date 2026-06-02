from a_validator import Validator


class Customer:

    next_id = 1

    def __init__(
            self,
            name,
            adresse,
            email,
            phone,
            password):

        if not Validator.validate_name(name):
            raise ValueError("Ungültiger Name")

        if not Validator.validate_address(adresse):
            raise ValueError("Ungültige Adresse")

        if not Validator.validate_email(email):
            raise ValueError("Ungültige Email")

        if not Validator.validate_phone(phone):
            raise ValueError("Ungültige Telefonnummer")

        self.id = Customer.next_id
        Customer.next_id += 1

        self.name = name
        self.adresse = adresse
        self.email = email
        self.phone = phone
        self.password = password

    # Getter

    def get_name(self):
        return self.name

    def get_adresse(self):
        return self.adresse

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.phone

    def get_password(self):
        return self.password

    # Setter

    def set_name(self, name):

        if Validator.validate_name(name):
            self.name = name

    def set_adresse(self, adresse):

        if Validator.validate_address(adresse):
            self.adresse = adresse

    def set_email(self, email):

        if Validator.validate_email(email):
            self.email = email

    def set_phone(self, phone):

        if Validator.validate_phone(phone):
            self.phone = phone

    def set_password(self, password):

        self.password = password