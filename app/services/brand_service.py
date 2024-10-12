import requests
from fastapi import HTTPException
from app.schemas.brand_schemas import BrandCreate, BrandUpdate

BRAND_SERVICE_URL = "http://brand-service:8010/brands"

def create_new_brand(brand: BrandCreate):
    """
    Sends a POST request to the brand-service to create a new brand.
    """
    try:
        response = requests.post(f"{BRAND_SERVICE_URL}/", json=brand.dict())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error creating brand from brand-service") from e

def get_brand(brand_id: int):
    """
    Sends a GET request to retrieve a brand by its ID from the brand-service.
    """
    try:
        response = requests.get(f"{BRAND_SERVICE_URL}/{brand_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=404, detail="Brand not found") from e

def update_existing_brand(brand_id: int, brand_update: BrandUpdate):
    """
    Sends a PUT request to the brand-service to update an existing brand.
    """
    try:
        response = requests.put(f"{BRAND_SERVICE_URL}/{brand_id}", json=brand_update.dict())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error updating brand from brand-service") from e

def delete_brand(brand_id: int):
    """
    Sends a DELETE request to the brand-service to delete a brand by its ID.
    """
    try:
        response = requests.delete(f"{BRAND_SERVICE_URL}/{brand_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error deleting brand from brand-service") from e
