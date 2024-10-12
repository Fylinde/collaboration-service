from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from typing_extensions import Annotated
from typing import Optional
from datetime import datetime

PhoneNumber = Annotated[
    str,
    BeforeValidator(lambda x: str(x).strip()),  # Strip whitespace before validation
    Field(min_length=10, max_length=20)  # Apply length constraints
]

class SellerBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[PhoneNumber] = None
    business_license: Optional[str] = None
    address: Optional[str] = None
    warehouse_location: Optional[str] = None
    preferred_collaboration_types: Optional[str] = None
    seller_rating: Optional[float] = None
    is_active: Optional[bool] = True

class SellerCreate(SellerBase):
    pass

class SellerBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[PhoneNumber] = None
    business_license: Optional[str] = None
    address: Optional[str] = None
    warehouse_location: Optional[str] = None
    preferred_collaboration_types: Optional[str] = None
    seller_rating: Optional[float] = None
    is_active: Optional[bool] = True

class Seller(SellerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
