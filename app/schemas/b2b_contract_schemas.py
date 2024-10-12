from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class B2BContractBase(BaseModel):
    seller_id: int = Field(..., description="ID of the seller initiating the contract")
    partner_seller_id: int = Field(..., description="ID of the partner seller")
    product_id: Optional[int] = Field(None, description="ID of the product involved in the B2B contract (Optional)")
    contract_terms: str = Field(..., description="The terms and conditions of the contract")
    revenue_sharing_percentage: Optional[float] = Field(None, description="Revenue sharing percentage")
    bulk_order_threshold: Optional[int] = Field(None, description="Bulk order threshold")
    contract_start_date: Optional[datetime] = Field(None, description="Start date of the contract")
    contract_end_date: Optional[datetime] = Field(None, description="End date of the contract (Optional)")

class B2BContractCreate(B2BContractBase):
    """
    Schema for creating a new B2B contract.
    """
    pass

class B2BContractUpdate(BaseModel):
    """
    Schema for updating an existing B2B contract.
    Fields are optional to allow partial updates.
    """
    product_id: Optional[int] = Field(None, description="ID of the product involved in the B2B contract")
    contract_terms: Optional[str] = Field(None, description="Updated terms and conditions of the contract")
    revenue_sharing_percentage: Optional[float] = Field(None, description="Updated revenue sharing percentage")
    bulk_order_threshold: Optional[int] = Field(None, description="Updated bulk order threshold")
    contract_start_date: Optional[datetime] = Field(None, description="Updated start date of the contract")
    contract_end_date: Optional[datetime] = Field(None, description="Updated end date of the contract")

class B2BContract(B2BContractBase):
    """
    Schema for retrieving a B2B contract with additional fields like ID and timestamps.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
