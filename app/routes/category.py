from fastapi import APIRouter, HTTPException
from app.schemas.category_schemas import CategoryCreate, Category
from app.crud import category_crud

router = APIRouter()

import logging
logger = logging.getLogger(__name__)

@router.post("/", response_model=Category)
def create_category_endpoint(category: CategoryCreate):
    """
    Create a new category by calling the category-service API.
    """
    logger.info(f"Received request to create category: {category}")
    try:
        return category_crud.create_category(category.dict())
    except Exception as e:
        logger.error(f"Error creating category: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating category")


@router.get("/", response_model=list[Category])
def get_all_categories_endpoint():
    """
    Get all categories by calling the category-service API.
    """
    try:
        return category_crud.get_all_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving categories")


@router.get("/{category_id}", response_model=Category)
def get_category_by_id_endpoint(category_id: int):
    """
    Retrieve a category by its ID by calling the category-service API.
    """
    try:
        return category_crud.get_category_by_id(category_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/{category_id}", response_model=Category)
def delete_category_endpoint(category_id: int):
    """
    Delete a category by its ID by calling the category-service API.
    """
    try:
        return category_crud.delete_category(category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting category")
