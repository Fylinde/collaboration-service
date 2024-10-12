from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import BaseModel
from datetime import datetime

class B2BContractModel(BaseModel):
    __tablename__ = "b2b_contracts"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)  # Reference to the seller initiating the contract
    partner_seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)  # Reference to the partner seller
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)  # Specific product in the B2B contract
    contract_terms = Column(Text, nullable=False)  # The terms and conditions of the B2B contract
    revenue_sharing_percentage = Column(Float, nullable=True)  # Revenue sharing agreement in the contract
    bulk_order_threshold = Column(Integer, nullable=True)  # Minimum order size in bulk for this contract
    contract_start_date = Column(DateTime, default=datetime.utcnow)  # Start date of the contract
    contract_end_date = Column(DateTime, nullable=True)  # Optional end date of the contract
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    seller = relationship("SellerModel", foreign_keys=[seller_id], back_populates="b2b_contracts")
    partner_seller = relationship("SellerModel", foreign_keys=[partner_seller_id], back_populates="partner_b2b_contracts")
    product = relationship("ProductModel", back_populates="b2b_contracts")

    def __repr__(self):
        return f'<B2BContract {self.id} - Seller {self.seller_id} with Partner {self.partner_seller_id}>'
