"""
This class validates customer information.
It checks email, phone number, name, address,
birth date and company number.
"""

import re
from datetime import datetime


class Validator:

    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone):
        pattern = r'^\+?\d{8,20}$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def validate_name(name):
        pattern = r'^[A-Za-zÄÖÜäöüß\s\-]+$'
        return bool(re.match(pattern, name))

    @staticmethod
    def validate_address(address):
        pattern = r'^[A-Za-zÄÖÜäöüß0-9\s,.\-/]+$'
        return bool(re.match(pattern, address))

    @staticmethod
    def validate_birthdate(birthdate):
        try:
            datetime.strptime(birthdate, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_company_number(company_number):
        pattern = r'^\d{5,15}$'
        return bool(re.match(pattern, company_number))