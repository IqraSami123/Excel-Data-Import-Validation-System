from app.services.validation_service import validate_row


def test_valid_customer():
    ### this function will test the valid data of the customer and it should return empty list as there is no error in the data ##
    row = {
        "name": "Iqra SAmi",
        "email": "iqra998@test.com",
        "phone": "0300654567",
        "age": 25,
        "city": "Lahore",
        "status": "active",
    }

    errors = validate_row(row)

    assert errors == []


def test_invalid_customer():
    ### this function will test the invalid data of the customer and it should return list of errors as there is error in the data ##
    row = {
        "name": "",
        "email": "invalid-email",
        "phone": "invalid-phone",
        "age": 150,
        "city": "Lahore",
        "status": "wrong",
    }

    errors = validate_row(row)

    assert "name is required" in errors   #assert means if the condition is true then it will pass the test otherwise it will fail the test
    assert "invalid email format" in errors
    assert "invalid phone format" in errors
    assert "age must be between 1 and 120" in errors
    assert "status must be active or inactive" in errors