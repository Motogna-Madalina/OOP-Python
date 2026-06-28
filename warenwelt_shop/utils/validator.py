
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

 #product validation------------------------------------------------------------

    @staticmethod
    def validate_text(text):

        if not text:
            return False
        pattern = r"^[A-Za-zÄÖÜäöüß0-9\s\-'&.,/]+$"
        return bool(re.match(pattern, str(text)))

    @staticmethod
    def validate_color(color):

        if not color:
            return False
        pattern = r"^[A-Za-zÄÖÜäöüß\s\-]+$"
        return bool(re.match(pattern, str(color)))

    @staticmethod
    def validate_price(price):
        pattern = r'^\d+(\.\d+)?$'
        return bool(re.match(pattern, str(price)))

    @staticmethod
    def validate_weight(weight):
        pattern = r'^\d+(\.\d+)?$'
        if re.match(pattern, str(weight)):
            return float(weight) > 0
        return False

    @staticmethod
    def validate_pages(pages):
        pattern = r'^\d+$'
        if re.match(pattern, str(pages)):
            return int(pages) > 0
        return False

    @staticmethod
    def validate_warranty_years(years):
        pattern = r'^\d+$'
        return bool(re.match(pattern, str(years)))