from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.seller import SellerModel
from app.schemas.seller_schemas import SellerCreate, SellerUpdate
import logging

logger = logging.getLogger(__name__)

def create_seller(db: Session, seller: SellerCreate):
    """
    Create a new seller and persist it to the database.
    
    :param db: The database session.
    :param seller: SellerCreate schema containing seller details.
    :return: The newly created seller or error message.
    """
    new_seller = SellerModel(**seller.dict())
    try:
        db.add(new_seller)
        db.commit()
        db.refresh(new_seller)
        logger.info(f"Seller created: {new_seller}")
        return new_seller
    except IntegrityError as e:
        logger.error(f"Error creating seller: {e}")
        db.rollback()
        raise


def get_seller_by_id(db: Session, seller_id: int):
    """
    Retrieve a seller by its ID.
    
    :param db: The database session.
    :param seller_id: ID of the seller to retrieve.
    :return: The seller object if found, else None.
    """
    return db.query(SellerModel).filter(SellerModel.id == seller_id).one_or_none()


def update_seller(db: Session, seller_id: int, seller: SellerUpdate):
    """
    Update an existing seller.
    
    :param db: The database session.
    :param seller_id: ID of the seller to update.
    :param seller: SellerUpdate schema containing updated seller details.
    :return: The updated seller object if successful, else None.
    """
    db_seller = get_seller_by_id(db, seller_id)
    if not db_seller:
        return None

    for key, value in seller.dict(exclude_unset=True).items():
        setattr(db_seller, key, value)

    db.commit()
    db.refresh(db_seller)
    return db_seller
