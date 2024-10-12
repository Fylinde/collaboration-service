import math
from app.models.seller import SellerModel


def calculate_proximity(location1: str, location2: str) -> float:
    """
    Calculate the distance between two locations using the Haversine formula.
    
    :param location1: Coordinates of the first location as 'latitude,longitude'.
    :param location2: Coordinates of the second location as 'latitude,longitude'.
    :return: Distance in kilometers.
    """
    try:
        lat1, lon1 = map(float, location1.split(','))
        lat2, lon2 = map(float, location2.split(','))
    except ValueError:
        raise ValueError("Invalid format for location. Please provide coordinates as 'latitude,longitude'.")

    R = 6371.0  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def suggest_seller_collaborations(seller_location: str, db):
    """
    Suggest seller collaborations based on proximity, demand trends, and categories.
    
    :param seller_location: Coordinates of the seller.
    :param db: The database session.
    :return: A list of potential seller partners.
    """
    sellers = db.query(SellerModel).all()
    
    nearby_sellers = [
        seller for seller in sellers
        if calculate_proximity(seller_location, seller.location) <= 50  # Example proximity filter: 50 km
    ]

    return nearby_sellers
