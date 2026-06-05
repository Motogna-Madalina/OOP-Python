#here we have a class that validates the input 
#data for our customers.

#It has static methods that check if
#the email, phone number, name, address,
#birthdate and company ID are valid 
#according to certain criteria.

#This class is used in the constructors of 
#the Customer classes to ensure that
#the data is correct before creating 
#an instance of a customer.

class Validator:

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email

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
        return len(name.strip()) > 1

    @staticmethod
    def validate_address(address):
        return len(address.strip()) > 3

    @staticmethod
    def validate_birthdate(birthdate):

        if len(birthdate) != 10:
            return False

        return (
            birthdate[2] == "."
            and
            birthdate[5] == "."
        )

    @staticmethod
    def validate_company_id(company_id):

        return (
            company_id.isdigit()
            and
            5 <= len(company_id) <= 15
        )