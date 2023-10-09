from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import update
from ..models.inspectation import Inspectation

async def add_inspectation(inspectation: Inspectation, db: Session) -> Inspectation:
    db.add(inspectation)
    db.commit()
    db.refresh(inspectation)
    return inspectation


def read_inspectation(inspectation_id: int, db: Session) -> Inspectation:
    inspectation = (
        db.query(Inspectation)
        .filter(Inspectation.inspectation_id == inspectation_id and Inspectation.is_deleted == False)
        .first()
    )
    return inspectation

async def update_inspectation(inspectation_id: int, db: Session, inspec_data: dict):
    inspec = db.query(Inspectation).filter(Inspectation.inspectation_id == inspectation_id and Inspectation.is_deleted == False).first()
    print(inspec_data)
    if inspec:
        # json_data = inspec.stats
        # if fieldName in json_data:
        #     if status:
        #         json_data[fieldName]["status"] = status
        #         json_data[fieldName]["note"] =  ""

        #     else:
        #         if not note:
        #             return None
        #         json_data[fieldName]["status"] = status
        #         json_data[fieldName]["note"] =  note
            
            inspec.stats = inspec_data
            print(inspec.stats)
            db.commit()
            db.refresh(inspec)
            return inspec
    return None
def soft_delete(inspectation_id: str, db: Session) -> Inspectation:
    inspectation = (
        db.query(Inspectation)
        .where(Inspectation.inspectation_id == inspectation_id and Inspectation.is_deleted == False)
        .first()
    )
    if inspectation:
        inspectation.is_deleted = True
        db.commit()
        db.refresh(inspectation)
        return inspectation
    return None


async def all_inspectations(db: Session) -> List[Inspectation]:
    db_inspectations = db.query(Inspectation).filter(Inspectation.is_deleted == False).all()
    return db_inspectations
