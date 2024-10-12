from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import BaseModel

class BrandModel(BaseModel):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)  # Brand name
    description = Column(String(500), nullable=True)  # Brand description
    logo_url = Column(String(255), nullable=True)  # Optional logo for the brand
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Brand {self.name}>'
