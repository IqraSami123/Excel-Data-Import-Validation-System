import re

from email_validator import EmailNotValidError, validate_email


REQUIRED_FIELDS = {
    "name",
    "email",
    "phone",
    "age",
    "city",
    "status",
}

ALLOWED_STATUS = {"active", "inactive"}


def validate_row(row: dict) -> list[str]:
    ### this function will check the each row of the excel file and validate data of each field and return errors collectively in a single list ###
    errors = []

    # Required fields
    for field in REQUIRED_FIELDS:
        value = row.get(field)  #this will get the value of the field from the row dictionary, if the field is not present it will return None

        if value is None or str(value).strip() == "":
            errors.append(f"{field} is required")

    # If required fields are missing, continue with the fields that exist
    name = row.get("name")
    email = row.get("email")
    phone = row.get("phone")
    age = row.get("age")
    status = row.get("status")

    # Name validation
    if name is not None and str(name).strip():
        if len(str(name).strip()) > 100:
            errors.append("name must not exceed 100 characters")

    # Email validation
    if email is not None and str(email).strip():
        try:
            validate_email(str(email).strip(), check_deliverability=False)
        except EmailNotValidError:
            errors.append("invalid email format")

    # Phone validation
    if phone is not None and str(phone).strip():
        phone_pattern = r"^\+?[0-9]{7,15}$"   #applied rejex 

        if not re.fullmatch(phone_pattern, str(phone).strip()):
            errors.append("invalid phone format")

    # Age validation
    if age is not None and str(age).strip():
        try:
            age_value = int(age)

            if age_value <= 0 or age_value > 120:
                errors.append("age must be between 1 and 120")

        except (ValueError, TypeError):
            errors.append("age must be an integer")

    # Status validation
    if status is not None and str(status).strip():
        if str(status).strip().lower() not in ALLOWED_STATUS:
            errors.append("status must be active or inactive")

    return errors