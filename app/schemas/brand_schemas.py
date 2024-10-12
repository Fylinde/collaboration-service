from pydantic import BaseModel

class BrandBase(BaseModel):
    name: str
    description: str | None = None
    logo_url: str | None = None

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BrandBase):
    pass

class Brand(BrandBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
