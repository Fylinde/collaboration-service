from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union
from datetime import datetime


# Base Collaboration schema shared across multiple collaboration types
class CollaborationBase(BaseModel):
    seller_id: int  # Main seller initiating the collaboration
    partner_seller_id: int  # Partner seller joining the collaboration
    agreement_details: str  # High-level overview of the agreement

    class Config:
        orm_mode = True


# Schema for creating a new collaboration (B2B/B2C)
class CollaborationCreate(CollaborationBase):
    collaboration_type: str  # Either 'B2B' or 'B2C'
    category_id: Optional[int] = None  # Optional category-level collaboration
    product_id: Optional[int] = None  # Optional product-level collaboration
    geographical_exclusivity: Optional[bool] = False  # Geographical exclusivity flag
    bulk_order_threshold: Optional[int] = None  # Threshold for B2B bulk orders
    revenue_sharing_percentage: Optional[float] = None  # Revenue-sharing percentage for partnership
    logistics_sharing: Optional[bool] = False  # Whether to share logistics resources
    collaboration_start_date: Optional[datetime] = None  # Optional collaboration start date
    collaboration_end_date: Optional[datetime] = None  # Optional collaboration end date

    class Config:
        orm_mode = True


# Schema for updating existing collaboration details
class CollaborationUpdate(BaseModel):
    agreement_details: Optional[str] = None
    bulk_order_threshold: Optional[int] = None  # Update bulk order threshold
    revenue_sharing_percentage: Optional[float] = None  # Update revenue-sharing percentage
    collaboration_end_date: Optional[datetime] = None  # Update end date of collaboration

    class Config:
        orm_mode = True


# Full Collaboration details including read-only fields
class Collaboration(CollaborationBase):
    id: int
    collaboration_type: str  # Type of collaboration ('B2B' or 'B2C')
    geographical_exclusivity: bool  # Whether the collaboration is geographically exclusive
    bulk_order_threshold: Optional[int] = None  # Minimum bulk order threshold for B2B
    revenue_sharing_percentage: Optional[float] = None  # Revenue-sharing percentage
    logistics_sharing: bool  # Whether the sellers share logistics resources
    collaboration_start_date: Optional[datetime] = None  # Collaboration start date
    collaboration_end_date: Optional[datetime] = None  # Collaboration end date
    created_at: datetime  # When the collaboration was created

    class Config:
        orm_mode = True


# Schema for shared inventory agreement between sellers (optional)
class SharedInventoryAgreement(BaseModel):
    products: List[int]  # List of product IDs being shared
    logistics: str  # Details about logistics/shipping handling
    terms: str  # Contract or agreement details between sellers

    class Config:
        orm_mode = True


# Schema for representing a B2B contract
class B2BContract(BaseModel):
    contract_id: int
    seller_id: int
    partner_seller_id: int
    terms: str  # Contract terms such as pricing, exclusivity, etc.
    start_date: datetime
    end_date: Optional[datetime] = None  # Optional for indefinite contracts

    class Config:
        orm_mode = True


# Schema for B2C agreements (optional)
class B2CAgreement(BaseModel):
    seller_id: int
    partner_seller_id: int
    promotion_details: str  # Details of cross-promotions or collaborative marketing efforts

    class Config:
        orm_mode = True


# Request model to calculate proximity between two geographical locations
class LocationRequest(BaseModel):
    location1: str  # Example: '52.2296756,21.0122287'
    location2: str  # Example: '41.8919300,12.5113300'

    class Config:
        orm_mode = True


# Seller Schema for additional enhancements (can be integrated with SellerService or Collaboration)
class SellerBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    business_license: Optional[str] = None  # Useful for B2B
    address: Optional[str] = None
    warehouse_location: Optional[str] = None  # Location of seller's main warehouse
    preferred_collaboration_types: Optional[str] = "B2C"  # Default to B2C, but can handle both
    seller_rating: Optional[float] = 0.0  # Average rating for the seller
    is_active: bool

    class Config:
        orm_mode = True


# Enhanced seller creation schema
class SellerCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    business_license: Optional[str] = None  # Relevant for B2B
    address: Optional[str] = None
    warehouse_location: Optional[str] = None
    preferred_collaboration_types: Optional[str] = "B2C"  # Default collaboration type for new sellers

    class Config:
        orm_mode = True


# Seller schema for read-only responses
class SellerResponse(SellerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
