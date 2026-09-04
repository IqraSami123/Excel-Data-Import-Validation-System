from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerListResponse, CustomerUpdate
from app.services.customer_service import create_customer, delete_customer, get_customers, get_customer, update_customer, partial_update_customer


router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"],    
)


#________________________________________
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


#________________________________________
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


#________________________________________
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = get_customer(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


#________________________________________
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer_endpoint(
    customer_id: int,
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
):
    customer = update_customer(
        db=db,
        customer_id=customer_id,
        customer_data=customer_data,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


#________________________________________
@router.patch("/{customer_id}", response_model=CustomerResponse)
def partial_update_customer_endpoint(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
):
    customer = partial_update_customer(
        db=db,
        customer_id=customer_id,
        customer_data=customer_data,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


#________________________________________
@router.delete("/{customer_id}", status_code=status.HTTP_200_OK)
def delete_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = delete_customer(
        db=db,
        customer_id=customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return {"detail": "Customer deleted successfully"}