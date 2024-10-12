from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.database import BaseModel

class ProductModel(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Product name
    description = Column(Text, nullable=True)  # Optional field for product description
    price = Column(Float, nullable=False)  # Price of the product
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)  # Link to category
    stock_quantity = Column(Integer, nullable=False)  # Number of items in stock
    brand_id = Column(Integer, nullable=True)  # Stores the brand ID fetched from collaboration-service
    #brand = relationship("BrandModel", back_populates="products")
    # Relationships
    collaborations = relationship("CollaborationModel", back_populates="product")  # Link to collaborations
    category = relationship("CategoryModel", back_populates="products")  # Link to category
    b2b_contracts = relationship("B2BContractModel", back_populates="product")

    def __repr__(self):
        return f"<Product {self.name} - {self.price}>"
