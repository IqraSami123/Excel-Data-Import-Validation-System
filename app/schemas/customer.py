from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


#________________________________________
class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=1, max_length=30)
    age: int = Field(gt=0, le=120)
    city: str = Field(min_length=1, max_length=100)
    status: str = Field(default="active")


#________________________________________
class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    age: int
    city: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # this allows Pydantic to read data from ORM models directly, enabling seamless conversion between SQLAlchemy models and Pydantic schemas.


#________________________________________
class CustomerListResponse(BaseModel):
    customers: list[CustomerResponse]
    total: int
    page: int
    page_size: int
    pages: int


#________________________________________
class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=1, max_length=30)
    age: int | None = Field(default=None, gt=0, le=120)
    city: str | None = Field(default=None, min_length=1, max_length=100)
    status: str | None = None