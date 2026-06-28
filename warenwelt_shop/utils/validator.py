
import re
from datetime import datetime

class Validator:

    @staticmethod
    def validate_email(email):
        pattern = r'^[\w.-]+@[\w.-]+\.\w+$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone):
        pattern = r'^\+?\d{8,20}$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def validate_name(name):
        pattern = r"^[A-Za-zÄÖÜäöüß\s\-']+$"
        return bool(re.match(pattern, name))

    @staticmethod
    def validate_address(address):
        pattern = r'^[A-Za-zÄÖÜäöüß0-9\s,.\-/]+$'
        return bool(re.match(pattern, address))

    @staticmethod
    def validate_birthdate(birthdate):
        try:
            date_obj = datetime.strptime(birthdate, "%d.%m.%Y").date()
        except ValueError:
            return False
        return date_obj <= datetime.now().date()

    @staticmethod
    def validate_company_id(company_id):
        pattern = r'^\d{5,15}$'
        return bool(re.match(pattern, str(company_id)))

    @staticmethod
    def validate_password(password):
        return len(password) >= 8