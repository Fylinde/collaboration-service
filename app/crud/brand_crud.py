import requests
from fastapi import HTTPException

BRAND_SERVICE_URL = "http://brand-service:8010/brands"

def create_brand(brand_data: dict):
    """
    Create a new brand using the brand-service API.
    
    :param brand_data: Dictionary containing brand details.
    :return: The newly created brand data from the brand-service.
    """
    try:
        response = requests.post(f"{BRAND_SERVICE_URL}/", json=brand_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error creating brand from brand-service") from e


def get_brand_by_id(brand_id: int):
    """
    Retrieve a brand by its ID using the brand-service API.
    
    :param brand_id: ID of the brand to retrieve.
    :return: The brand object from the brand-service.
    """
    try:
        response = requests.get(f"{BRAND_SERVICE_URL}/{brand_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=404, detail="Brand not found") from e


def get_all_brands():
    """
    Retrieve all brands using the brand-service API.
    
    :return: A list of brand objects from the brand-service.
    """
    try:
        response = requests.get(BRAND_SERVICE_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error fetching brands from brand-service") from e


def update_brand(brand_id: int, brand_update: dict):
    """
    Update an existing brand using the brand-service API.
    
    :param brand_id: ID of the brand to update.
    :param brand_update: Updated brand data.
    :return: The updated brand data from the brand-service.
    """
    try:
        response = requests.put(f"{BRAND_SERVICE_URL}/{brand_id}", json=brand_update)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error updating brand from brand-service") from e


def delete_brand(brand_id: int):
    """
    Delete a brand by its ID using the brand-service API.
    
    :param brand_id: ID of the brand to delete.
    :return: The deleted brand object if found and deleted, else an error.
    """
    try:
        response = requests.delete(f"{BRAND_SERVICE_URL}/{brand_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error deleting brand from brand-service") from e
