from sqlalchemy.orm import Session
from app.models.collaboration import CollaborationModel
from app.schemas.collaboration_schemas import CollaborationCreate, CollaborationUpdate, SharedInventoryAgreement
from typing import List

# CRUD Operations for Collaboration

def create_collaboration(db: Session, collaboration: CollaborationCreate):
    """
    Create a new collaboration and persist it to the database.
    
    :param db: The database session.
    :param collaboration: CollaborationCreate schema containing collaboration details.
    :return: The newly created collaboration.
    """
    new_collaboration = CollaborationModel(**collaboration.dict())
    db.add(new_collaboration)
    db.commit()
    db.refresh(new_collaboration)
    return new_collaboration


def get_collaboration_by_id(db: Session, collaboration_id: int):
    """
    Retrieve a collaboration by its ID.
    
    :param db: The database session.
    :param collaboration_id: ID of the collaboration to retrieve.
    :return: The collaboration object if found, else None.
    """
    return db.query(CollaborationModel).filter(CollaborationModel.id == collaboration_id).one_or_none()


def get_collaborations_by_seller(db: Session, seller_id: int):
    """
    Retrieve all collaborations for a specific seller.
    
    :param db: The database session.
    :param seller_id: ID of the seller whose collaborations are to be retrieved.
    :return: A list of collaboration objects.
    """
    return db.query(CollaborationModel).filter(
        (CollaborationModel.seller_id == seller_id) | 
        (CollaborationModel.partner_seller_id == seller_id)
    ).all()


def get_collaborations_by_type(db: Session, seller_id: int, collaboration_type: str) -> List[CollaborationModel]:
    """
    Retrieve collaborations for a specific seller based on collaboration type (B2B/B2C).
    
    :param db: The database session.
    :param seller_id: ID of the seller.
    :param collaboration_type: Type of collaboration to filter (B2B or B2C).
    :return: List of collaborations matching the criteria.
    """
    return db.query(CollaborationModel).filter(
        ((CollaborationModel.seller_id == seller_id) | 
         (CollaborationModel.partner_seller_id == seller_id)) & 
         (CollaborationModel.collaboration_type == collaboration_type)
    ).all()


def update_collaboration(db: Session, collaboration_id: int, collaboration: CollaborationUpdate):
    """
    Update an existing collaboration.
    
    :param db: The database session.
    :param collaboration_id: ID of the collaboration to update.
    :param collaboration: CollaborationUpdate schema containing updated details.
    :return: The updated collaboration object if successful, else None.
    """
    db_collaboration = get_collaboration_by_id(db, collaboration_id)
    if not db_collaboration:
        return None

    for key, value in collaboration.dict(exclude_unset=True).items():
        setattr(db_collaboration, key, value)

    db.commit()
    db.refresh(db_collaboration)
    return db_collaboration


def delete_collaboration(db: Session, collaboration_id: int):
    """
    Delete a collaboration by its ID.
    
    :param db: The database session.
    :param collaboration_id: ID of the collaboration to delete.
    :return: The deleted collaboration object if found and deleted, else None.
    """
    db_collaboration = get_collaboration_by_id(db, collaboration_id)
    if not db_collaboration:
        return None

    db.delete(db_collaboration)
    db.commit()
    return db_collaboration


# New functions for handling B2B-specific and logistics-sharing logic

def create_shared_inventory_agreement(db: Session, collaboration_id: int, agreement: SharedInventoryAgreement):
    """
    Create a shared inventory agreement between collaborating sellers.
    
    :param db: The database session.
    :param collaboration_id: ID of the collaboration.
    :param agreement: SharedInventoryAgreement schema containing the agreement details.
    :return: Success message or error message.
    """
    collaboration = get_collaboration_by_id(db, collaboration_id)
    if not collaboration:
        return None
    
    collaboration.agreement_details = f"Shared Inventory: {agreement.products}, Logistics: {agreement.logistics}, Terms: {agreement.terms}"
    db.commit()
    return collaboration


def update_b2b_contract(db: Session, collaboration_id: int, contract_update: CollaborationUpdate):
    """
    Update an existing B2B contract.
    
    :param db: The database session.
    :param collaboration_id: ID of the contract to update.
    :param contract_update: CollaborationUpdate schema with updated contract details.
    :return: The updated contract object if found, else None.
    """
    collaboration = get_collaboration_by_id(db, collaboration_id)
    if not collaboration:
        return None

    for key, value in contract_update.dict(exclude_unset=True).items():
        setattr(collaboration, key, value)

    db.commit()
    db.refresh(collaboration)
    return collaboration


def delete_b2b_contract(db: Session, collaboration_id: int):
    """
    Delete a B2B contract by its ID.
    
    :param db: The database session.
    :param collaboration_id: ID of the contract to delete.
    :return: The deleted contract if found and deleted, else None.
    """
    collaboration = get_collaboration_by_id(db, collaboration_id)
    if not collaboration:
        return None

    db.delete(collaboration)
    db.commit()
    return collaboration


def get_contracts_by_seller(db: Session, seller_id: int):
    """
    Retrieve all contracts for a specific seller.
    
    :param db: The database session.
    :param seller_id: ID of the seller whose contracts are to be retrieved.
    :return: A list of contracts.
    """
    return db.query(CollaborationModel).filter(
        (CollaborationModel.seller_id == seller_id) |
        (CollaborationModel.partner_seller_id == seller_id)
    ).all()
