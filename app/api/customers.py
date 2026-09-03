from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerListResponse
from app.services.customer_service import create_customer, get_customers


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


@router.get(
    "/",
    response_model=CustomerListResponse,
)
def list_customers(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_customers(
        db=db,
        page=page,
        page_size=page_size,
    )