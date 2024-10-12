from fastapi import APIRouter, HTTPException
from app.schemas.brand_schemas import BrandCreate, BrandUpdate, Brand
from app.crud.brand_crud import create_brand, get_brand_by_id, update_brand, delete_brand

router = APIRouter()

@router.post("/", response_model=Brand)
def create_brand_route(brand: BrandCreate):
    try:
        return create_brand(brand.dict())
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{brand_id}", response_model=Brand)
def get_brand_by_id_route(brand_id: int):
    try:
        return get_brand_by_id(brand_id)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{brand_id}", response_model=Brand)
def update_brand_route(brand_id: int, brand_update: BrandUpdate):
    try:
        return update_brand(brand_id, brand_update.dict())
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{brand_id}", response_model=Brand)
def delete_brand_route(brand_id: int):
    try:
        return delete_brand(brand_id)
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
