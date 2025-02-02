from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from app.database import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship

class SellerModel(BaseModel):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Seller's name (Company or Individual)
    email = Column(String(255), unique=True, nullable=False)  # Contact email
    phoneNumber = Column(String(20), nullable=True)  # Contact number
    business_license = Column(String(100), nullable=True)  # Business license (for B2B)
    address = Column(String(255), nullable=True)  # Seller's main business address
    warehouse_location = Column(String(255), nullable=True)  # Primary warehouse location
    preferred_collaboration_types = Column(String(50), nullable=True)  # Preferences: B2B, B2C, Both
    seller_rating = Column(Float, default=0.0)  # Average rating of the seller
    is_active = Column(Boolean, default=True)  # Status of seller's account
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    collaborations = relationship("CollaborationModel", foreign_keys="CollaborationModel.seller_id", back_populates="seller")
    partnership_collaborations = relationship("CollaborationModel", foreign_keys="CollaborationModel.partner_seller_id", back_populates="partner_seller")
    b2b_contracts = relationship("B2BContractModel", back_populates="seller")
    partner_b2b_contracts = relationship("B2BContractModel", back_populates="partner_seller")

    def __repr__(self):
        return f'<Seller {self.name} (ID: {self.id})>'
