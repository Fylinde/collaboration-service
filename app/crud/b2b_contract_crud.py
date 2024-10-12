from sqlalchemy.orm import Session
from app.models.b2b_contract import B2BContractModel
from app.schemas.b2b_contract_schemas import B2BContractCreate, B2BContractUpdate
from typing import Optional
import logging
from typing import Optional, List, Union

logger = logging.getLogger(__name__)

def create_b2b_contract(db: Session, contract: B2BContractCreate):
    """
    Create a new B2B contract.
    
    :param db: The database session.
    :param contract: B2BContractCreate schema containing contract details.
    :return: The newly created B2B contract.
    """
    new_contract = B2BContractModel(**contract.dict())
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    return new_contract


def get_contract_by_id(db: Session, contract_id: int) -> Optional[B2BContractModel]:
    """
    Retrieve a B2B contract by its ID.
    
    :param db: The database session.
    :param contract_id: ID of the contract to retrieve.
    :return: The contract object if found, else None.
    """
    return db.query(B2BContractModel).filter(B2BContractModel.id == contract_id).one_or_none()


def update_b2b_contract(db: Session, contract_id: int, contract_update: B2BContractUpdate) -> Optional[B2BContractModel]:
    """
    Update an existing B2B contract.
    
    :param db: The database session.
    :param contract_id: ID of the contract to update.
    :param contract_update: B2BContractUpdate schema with updated contract details.
    :return: The updated contract object if found, else None.
    """
    contract = get_contract_by_id(db, contract_id)
    if not contract:
        return None

    # Update the contract fields with the provided values
    for key, value in contract_update.dict(exclude_unset=True).items():
        setattr(contract, key, value)

    db.commit()
    db.refresh(contract)
    return contract


def delete_b2b_contract(db: Session, contract_id: int) -> Optional[B2BContractModel]:
    """
    Delete a B2B contract by its ID.
    
    :param db: The database session.
    :param contract_id: ID of the contract to delete.
    :return: The deleted contract object if found and deleted, else None.
    """
    contract = get_contract_by_id(db, contract_id)
    if not contract:
        return None

    db.delete(contract)
    db.commit()
    return contract


def get_contracts_by_seller(db: Session, seller_id: int) -> Optional[List[B2BContractModel]]:
    """
    Retrieve all B2B contracts for a specific seller.
    
    :param db: The database session.
    :param seller_id: The seller's ID whose contracts are to be retrieved.
    :return: A list of B2B contracts related to the seller.
    """
    return db.query(B2BContractModel).filter(
        (B2BContractModel.seller_id == seller_id) |
        (B2BContractModel.partner_seller_id == seller_id)
    ).all()

