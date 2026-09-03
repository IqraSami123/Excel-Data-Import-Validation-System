from sqlalchemy.orm import Session
from sqlalchemy import func, select
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


def get_customers(
    db: Session,
    page: int,
    page_size: int,
):
    offset = (page - 1) * page_size

    total = db.scalar(
        select(func.count()).select_from(Customer)
    )

    customers = db.scalars(
        select(Customer)
        .order_by(Customer.id)
        .offset(offset)
        .limit(page_size)
    ).all()

    pages = (total + page_size - 1) // page_size

    return {
        "customers": customers,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
    }