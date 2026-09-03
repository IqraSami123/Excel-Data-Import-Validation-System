from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import create_customer


router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"],    
)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer_endpoint(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),   # dependancy injection

):
    return create_customer(db, customer_data)