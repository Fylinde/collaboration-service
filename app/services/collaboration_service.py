from sqlalchemy.orm import Session
from app.models.seller import SellerModel
from app.models.collaboration import CollaborationModel
from app.schemas.collaboration_schemas import SharedInventoryAgreement, CreateCollaborationRequest
from app.utils.collaboration_utils import calculate_proximity, suggest_seller_collaborations
from fastapi import HTTPException


def create_collaboration(request: CreateCollaborationRequest, db: Session, collaboration_type: str):
    """
    Create a new seller collaboration based on the provided request with B2B/B2C support.
    
    :param request: Request schema containing seller IDs and details of the collaboration.
    :param db: Database session.
    :param collaboration_type: The type of collaboration ('B2B', 'B2C', 'Hybrid').
    :return: Collaboration object if successfully created.
    """
    seller = get_seller_by_id(db, request.seller_1_id)
    partner_seller = get_seller_by_id(db, request.seller_2_id)

    if not seller or not partner_seller:
        raise HTTPException(status_code=404, detail="One or both sellers not found.")
    
    if collaboration_type not in ['B2B', 'B2C', 'Hybrid']:
        raise HTTPException(status_code=400, detail="Invalid collaboration type.")

    new_collaboration = CollaborationModel(
        seller_id=request.seller_1_id,
        partner_seller_id=request.seller_2_id,
        agreement_details=request.details,
        collaboration_type=collaboration_type,  # B2B, B2C, Hybrid
        product_id=request.product_id,
        category_id=request.category_id,
        bulk_order_threshold=request.bulk_order_threshold,
        revenue_sharing_percentage=request.revenue_sharing_percentage,
        geographical_exclusivity=request.geographical_exclusivity
    )
    
    db.add(new_collaboration)
    db.commit()
    db.refresh(new_collaboration)
    
    return new_collaboration


def find_nearby_sellers(seller_id: int, location: str, db: Session):
    """
    Find nearby sellers based on location proximity and availability of stock.
    
    :param seller_id: The ID of the seller requesting nearby sellers.
    :param location: The location to match sellers to.
    :param db: Database session.
    :return: List of nearby sellers.
    """
    seller = get_seller_by_id(db, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail=f"Seller with ID {seller_id} does not exist.")
    
    return suggest_seller_collaborations(location, db)


def create_shared_inventory_agreement(seller_id: int, partner_seller_id: int, agreement_details: SharedInventoryAgreement, db: Session):
    """
    Create a shared inventory agreement between two sellers.
    
    :param seller_id: ID of the seller initiating the agreement.
    :param partner_seller_id: ID of the partner seller.
    :param agreement_details: Details of the agreement (products, logistics, etc.).
    :param db: Database session.
    :return: Collaboration object if successful.
    """
    seller = get_seller_by_id(db, seller_id)
    partner_seller = get_seller_by_id(db, partner_seller_id)
    
    if not seller or not partner_seller:
        raise HTTPException(status_code=404, detail="One or both sellers not found.")
    
    new_collaboration = CollaborationModel(
        seller_id=seller_id,
        partner_seller_id=partner_seller_id,
        agreement_details=agreement_details.details
    )
    
    db.add(new_collaboration)
    db.commit()
    db.refresh(new_collaboration)
    
    return new_collaboration


# Helper function to retrieve seller by ID
def get_seller_by_id(db: Session, seller_id: int):
    return db.query(SellerModel).filter(SellerModel.id == seller_id).one_or_none()


# Refactored CRUD function for creating a new collaboration
def create_new_collaboration(request: CreateCollaborationRequest, db: Session):
    new_collaboration = CollaborationModel(
        seller_id=request.seller_1_id,
        partner_seller_id=request.seller_2_id,
        agreement_details=request.details
    )

    db.add(new_collaboration)
    db.commit()
    db.refresh(new_collaboration)
    return new_collaboration
