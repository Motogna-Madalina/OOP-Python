import re
from datetime import datetime


class Validator:

    @staticmethod
    def validate_email(email):

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone):

        phone = phone.replace("+", "")

        return (
            phone.isdigit()
            and
            8 <= len(phone) <= 20
        )

    @staticmethod
    def validate_name(name):

        pattern = r"^[A-Za-zÄÖÜäöüß\s'-]+$"

        return bool(re.match(pattern, name))

    @staticmethod
    def validate_address(address):

        pattern = r"^[A-Za-zÄÖÜäöüß0-9\s,.\-]+$"

        return bool(re.match(pattern, address))

    @staticmethod
    def validate_birthdate(birthdate):

        try:

            datetime.strptime(
                birthdate,
                "%d.%m.%Y"
            )

            return True

        except ValueError:

            return False

    @staticmethod
    def validate_company_id(company_id):

        return (
            company_id.isdigit()
            and
            5 <= len(company_id) <= 15
        )