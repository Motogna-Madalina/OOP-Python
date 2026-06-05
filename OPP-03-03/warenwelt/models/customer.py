from warenwelt.utils.validator import Validator


class Customer:

    next_id = 1

    def __init__(
            self,
            name,
            address,
            email,
            phone,
            password):

        if not Validator.validate_name(name):
            raise ValueError("Invalid name")

        if not Validator.validate_address(address):
            raise ValueError("Invalid address")

        if not Validator.validate_email(email):
            raise ValueError("Invalid email")

        if not Validator.validate_phone(phone):
            raise ValueError("Invalid phone number")

        self.id = Customer.next_id
        Customer.next_id += 1

        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.password = password

    # Getters

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.phone

    def get_password(self):
        return self.password

    # Setters

    def set_name(self, name):

        if Validator.validate_name(name):
            self.name = name

    def set_address(self, address):

        if Validator.validate_address(address):
            self.address = address

    def set_email(self, email):

        if Validator.validate_email(email):
            self.email = email

    def set_phone(self, phone):

        if Validator.validate_phone(phone):
            self.phone = phone

    def set_password(self, password):

        self.password = password

    def __str__(self):

        return (
            f"Customer: {self.name} | "
            f"Email: {self.email} | "
            f"Phone: {self.phone}"
        )