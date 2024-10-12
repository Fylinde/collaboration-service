# utils/brand_utils.py

def validate_brand_name(name: str):
    if len(name) < 3:
        raise ValueError("Brand name is too short")
    return True
