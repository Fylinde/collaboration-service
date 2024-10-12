import requests
from fastapi import HTTPException

CATEGORY_SERVICE_URL = "http://category-service:8005/categories"

def create_category(category_data: dict):
    """
    Create a new category using the category-service API.
    
    :param category_data: Dictionary containing category details.
    :return: The newly created category data from the category-service.
    """
    try:
        response = requests.post(f"{CATEGORY_SERVICE_URL}/", json=category_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error creating category from category-service") from e


def get_category_by_id(category_id: int):
    """
    Retrieve a category by its ID using the category-service API.
    
    :param category_id: ID of the category to retrieve.
    :return: The category object from the category-service.
    """
    try:
        response = requests.get(f"{CATEGORY_SERVICE_URL}/{category_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=404, detail="Category not found") from e


def get_all_categories():
    """
    Retrieve all categories using the category-service API.
    
    :return: A list of categories from the category-service.
    """
    try:
        response = requests.get(f"{CATEGORY_SERVICE_URL}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error retrieving categories from category-service") from e


def update_category(category_id: int, category_data: dict):
    """
    Update a category using the category-service API.
    
    :param category_id: ID of the category to update.
    :param category_data: Updated category data.
    :return: The updated category data from the category-service.
    """
    try:
        response = requests.put(f"{CATEGORY_SERVICE_URL}/{category_id}", json=category_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error updating category from category-service") from e


def delete_category(category_id: int):
    """
    Delete a category by its ID using the category-service API.
    
    :param category_id: ID of the category to delete.
    :return: The deleted category data from the category-service.
    """
    try:
        response = requests.delete(f"{CATEGORY_SERVICE_URL}/{category_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error deleting category from category-service") from e
