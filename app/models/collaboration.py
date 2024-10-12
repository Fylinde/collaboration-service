from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship
from app.database import BaseModel
from datetime import datetime

class CollaborationModel(BaseModel):
    __tablename__ = "collaborations"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    partner_seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    collaboration_type = Column(String(10), nullable=False)  # B2B or B2C
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)  # Collaborating on specific product (Optional)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)  # Collaborating on category level (Optional)
    geographical_exclusivity = Column(Boolean, default=False)
    bulk_order_threshold = Column(Integer, nullable=True)
    revenue_sharing_percentage = Column(Float, nullable=True)
    contract_terms = Column(Text, nullable=True)
    agreement_details = Column(Text, nullable=False)
    collaboration_start_date = Column(DateTime, default=datetime.utcnow)
    collaboration_end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    brand_id = Column(Integer, nullable=True)  # Stores the brand ID fetched from collaboration-service
    # Relationships
    seller = relationship("SellerModel", foreign_keys=[seller_id], back_populates="collaborations")
    partner_seller = relationship("SellerModel", foreign_keys=[partner_seller_id], back_populates="partnership_collaborations")
    product = relationship("ProductModel", back_populates="collaborations")  # Link to ProductModel
    category = relationship("CategoryModel", back_populates="collaborations")  # Link to CategoryModel
    # brand = relationship("BrandModel", back_populates="collaborations")
    
    def __repr__(self):
        return f"<Collaboration {self.id} - {self.collaboration_type}>"
