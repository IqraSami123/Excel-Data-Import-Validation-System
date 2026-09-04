from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


################################################################
#_______________________create customer_________________________
################################################################

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


################################################################
#_______________________get customers list______________________
################################################################

def get_customers(
    db: Session,
    page: int,
    page_size: int,
):
    offset = (page - 1) * page_size     

    total = db.scalar(       # counts the totla number of customers from table usinf sqlalchemy's functions
        select(func.count()).select_from(Customer)
    )

    customers = db.scalars(
        select(Customer)
        .order_by(Customer.id)
        .offset(offset)
        .limit(page_size)
    ).all()

    pages = (total + page_size - 1) // page_size    # this calculates the total number of pages    

    return {
        "customers": customers,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
    }


################################################################
#_______________________get customer by id______________________
################################################################

def get_customer(db: Session, customer_id: int) -> Customer | None:
    return db.get(Customer, customer_id)


################################################################
#_______________________completly update customer_______________
################################################################

def update_customer(
    db: Session,
    customer_id: int,
    customer_data: CustomerCreate,
) -> Customer | None:

    customer = db.get(Customer, customer_id)

    if customer is None:
        return None

    customer.name = customer_data.name
    customer.email = customer_data.email
    customer.phone = customer_data.phone
    customer.age = customer_data.age
    customer.city = customer_data.city
    customer.status = customer_data.status

    db.commit()
    db.refresh(customer)

    return customer



################################################################
#_______________________partialy update customer________________
################################################################

def partial_update_customer(
    db: Session,
    customer_id: int,
    customer_data: CustomerUpdate,
) -> Customer | None:

    customer = db.get(Customer, customer_id)

    if customer is None:
        return None

    update_data = customer_data.model_dump(exclude_unset=True)   # this line extracts the fields that have been provided in the update request, ignoring any fields that were not included. This allows for partial updates.

    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    return customer


################################################################
#_______________________delete customer________________________
################################################################

def delete_customer(db: Session, customer_id: int) -> Customer | None:
    customer = db.get(Customer, customer_id)

    if customer is None:
        return None

    db.delete(customer)
    db.commit()

    return customer