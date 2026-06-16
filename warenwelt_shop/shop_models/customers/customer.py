"""
This abstract class represents a customer.
It stores basic customer information and uses getters/setters.

It is abstract now: PrivateCustomer and CompanyCustomer must each
define their own discount_rate(). That single method replaces the
isinstance() checks that used to decide the company discount.
"""

from abc import ABC, abstractmethod

from utils.validator import Validator


class Customer(ABC):

    # Class variable shared by all customers.
    # It remembers the last id that was given out.
    _id_counter = 0

    def __init__(self, name, address, email, phone, password):
        # Increase the shared counter and use it as this customer's id.
        Customer._id_counter += 1
        self.id = Customer._id_counter

        self.set_name(name)
        self.set_address(address)
        self.set_email(email)
        self.set_phone(phone)
        self.set_password(password)

    # ------------------------------------------------------------------
    # Abstract contract: each customer type decides its own discount.
    # The shop, the cart and the order all call this single method
    # instead of checking the customer's type by hand.
    # ------------------------------------------------------------------

    @abstractmethod
    def discount_rate(self):
        """Fraction (0.0 - 1.0) taken off the order total."""
        raise NotImplementedError

    # Getters

    def get_id(self):
        return self.id

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
