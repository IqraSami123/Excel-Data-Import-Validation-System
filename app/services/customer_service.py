from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


def create_customer(
    db: Session,
    customer_data: CustomerCreate,
) -> Customer:   # this function takes a SQLAlchemy session and a Pydantic schema as input, creates a new Customer instance, adds it to the database, commits the transaction, and returns the newly created Customer object.

    customer = Customer(  
        name=customer_data.name,
        email=customer_data.email,
        phone=customer_data.phone,
        age=customer_data.age,
        city=customer_data.city,
        status=customer_data.status,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer