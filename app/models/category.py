from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import BaseModel
from sqlalchemy import Table, Column, Integer, ForeignKey



category_brand_association = Table('category_brand', BaseModel.metadata,
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('brand_id', Integer, nullable=True)
)

class CategoryModel(BaseModel):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(String(500), nullable=True)
    brand_id = Column(Integer, nullable=True)  # Stores the brand ID fetched from collaboration-service
    # Relationships
    products = relationship("ProductModel", back_populates="category")  # Link to products
    collaborations = relationship("CollaborationModel", back_populates="category")  # Link to collaborations

    def __repr__(self):
        return f"<Category {self.name}>"
