from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.collaboration_schemas import (
    CollaborationCreate, 
    CollaborationUpdate, 
    Collaboration, 
    SharedInventoryAgreement
)
from app.crud import collaboration_crud
from app.database import get_db
from app.utils.collaboration_utils import calculate_proximity

router = APIRouter()

# -------------------- BASIC COLLABORATION ENDPOINTS -------------------- #

@router.post("/", response_model=Collaboration)
def create_collaboration(collaboration: CollaborationCreate, db: Session = Depends(get_db)):
    """
    Create a new collaboration between two sellers. 
    This can be B2B or B2C collaboration.
    
    - **collaboration_type**: B2B or B2C
    - **geographical_exclusivity**: Ensures sellers can't collaborate with others in the same region
    
    :param collaboration: The collaboration details (seller IDs, agreement details).
    :param db: The database session.
    :return: The newly created collaboration.
    """
    try:
        return collaboration_crud.create_collaboration(db, collaboration)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating collaboration")


@router.get("/{collaboration_id}", response_model=Collaboration)
def get_collaboration(collaboration_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a collaboration by its ID.
    
    :param collaboration_id: The ID of the collaboration to retrieve.
    :param db: The database session.
    :return: The collaboration details if found.
    """
    collaboration = collaboration_crud.get_collaboration_by_id(db, collaboration_id)
    if not collaboration:
        raise HTTPException(status_code=404, detail="Collaboration not found")
    return collaboration


@router.get("/seller/{seller_id}", response_model=List[Collaboration])
def get_collaborations_by_seller(
    seller_id: int, 
    collaboration_type: str = Query(None, description="Filter by B2B or B2C collaboration"), 
    db: Session = Depends(get_db)
):
    """
    Retrieve all collaborations for a specific seller. 
    Can filter by collaboration type (B2B/B2C).
    
    :param seller_id: The seller's ID whose collaborations are to be retrieved.
    :param collaboration_type: Filter by 'B2B' or 'B2C'.
    :param db: The database session.
    :return: A list of collaborations related to the seller.
    """
    collaborations = collaboration_crud.get_collaborations_by_seller(db, seller_id)
    if not collaborations:
        raise HTTPException(status_code=404, detail=f"No collaborations found for seller ID {seller_id}")
    
    # If a collaboration_type is provided, filter the collaborations
    if collaboration_type:
        collaborations = collaboration_crud.get_collaborations_by_type(db, seller_id, collaboration_type)
    
    return collaborations


@router.put("/{collaboration_id}", response_model=Collaboration)
def update_collaboration(collaboration_id: int, collaboration: CollaborationUpdate, db: Session = Depends(get_db)):
    """
    Update an existing collaboration by its ID.
    
    :param collaboration_id: The ID of the collaboration to update.
    :param collaboration: The updated collaboration details.
    :param db: The database session.
    :return: The updated collaboration.
    """
    updated_collaboration = collaboration_crud.update_collaboration(db, collaboration_id, collaboration)
    if not updated_collaboration:
        raise HTTPException(status_code=404, detail="Collaboration not found")
    return updated_collaboration


@router.delete("/{collaboration_id}", response_model=Collaboration)
def delete_collaboration(collaboration_id: int, db: Session = Depends(get_db)):
    """
    Delete a collaboration by its ID.
    
    :param collaboration_id: The ID of the collaboration to delete.
    :param db: The database session.
    :return: The deleted collaboration object.
    """
    deleted_collaboration = collaboration_crud.delete_collaboration(db, collaboration_id)
    if not deleted_collaboration:
        raise HTTPException(status_code=404, detail="Collaboration not found")
    return deleted_collaboration


# -------------------- NEW ADVANCED ENDPOINTS -------------------- #

@router.post("/shared-inventory/{collaboration_id}", response_model=Collaboration)
def create_shared_inventory_agreement(
    collaboration_id: int, 
    agreement: SharedInventoryAgreement, 
    db: Session = Depends(get_db)
):
    """
    Create a shared inventory agreement between two sellers who have a collaboration.
    
    :param collaboration_id: The ID of the collaboration.
    :param agreement: SharedInventoryAgreement schema containing the agreement details.
    :param db: The database session.
    :return: The collaboration with updated agreement details.
    """
    updated_collaboration = collaboration_crud.create_shared_inventory_agreement(db, collaboration_id, agreement)
    if not updated_collaboration:
        raise HTTPException(status_code=404, detail="Collaboration not found or unable to create agreement.")
    return updated_collaboration


@router.get("/find-nearby-sellers/{seller_id}", response_model=List[Collaboration])
def find_nearby_sellers(
    seller_id: int, 
    location: str, 
    db: Session = Depends(get_db)
):
    """
    Find nearby sellers based on location proximity. Returns a list of nearby sellers
    who are available for collaboration.
    
    :param seller_id: The ID of the seller requesting nearby sellers.
    :param location: The location in 'latitude,longitude' format to match sellers to.
    :param db: The database session.
    :return: A list of nearby sellers within a certain radius.
    """
    nearby_sellers = collaboration_crud.find_nearby_sellers(db, seller_id, location)
    if not nearby_sellers:
        raise HTTPException(status_code=404, detail="No nearby sellers found.")
    return nearby_sellers


@router.get("/contracts/{seller_id}", response_model=List[Collaboration])
def get_contracts_by_seller(seller_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all B2B contracts for a specific seller.
    
    :param seller_id: The seller's ID whose contracts are to be retrieved.
    :param db: The database session.
    :return: A list of contracts related to the seller.
    """
    contracts = collaboration_crud.get_contracts_by_seller(db, seller_id)
    if not contracts:
        raise HTTPException(status_code=404, detail=f"No contracts found for seller ID {seller_id}")
    return contracts


@router.put("/contracts/{contract_id}", response_model=Collaboration)
def update_b2b_contract(contract_id: int, contract_update: CollaborationUpdate, db: Session = Depends(get_db)):
    """
    Update an existing B2B contract by its ID.
    
    :param contract_id: The ID of the contract to update.
    :param contract_update: The updated contract details.
    :param db: The database session.
    :return: The updated contract.
    """
    updated_contract = collaboration_crud.update_b2b_contract(db, contract_id, contract_update)
    if not updated_contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return updated_contract


@router.delete("/contracts/{contract_id}", response_model=Collaboration)
def delete_b2b_contract(contract_id: int, db: Session = Depends(get_db)):
    """
    Delete a B2B contract by its ID.
    
    :param contract_id: The ID of the contract to delete.
    :param db: The database session.
    :return: The deleted contract object.
    """
    deleted_contract = collaboration_crud.delete_b2b_contract(db, contract_id)
    if not deleted_contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return deleted_contract
