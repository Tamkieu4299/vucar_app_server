from fastapi import APIRouter, Depends, status
from ..schemas.inspectation import CreateInspecSchema, InspecResponseSchema, InspecUpdateSchema
from ..utils.logger import setup_logger
from ..db.database import get_db
from sqlalchemy.orm import Session
from ..models.inspectation import Inspectation
from ..crud.inspectation import add_inspectation, read_inspectation, all_inspectations, update_inspectation
from ..utils.crawl_data import get_criterias
from ..utils.exception import (
    NotFoundException,
)
from typing import List

router = APIRouter()
logger = setup_logger(__name__)

@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=InspecResponseSchema,
)
async def create_inspec(
    inspec_data: CreateInspecSchema,
    db: Session = Depends(get_db),
):
    hash_inspec_data = inspec_data.dict() 
    hash_inspec_data["stats"] = get_criterias()
    inspec: Inspectation = Inspectation(**hash_inspec_data)
    new_inspec = await add_inspectation(inspec, db)

    return new_inspec.__dict__

@router.get(
    "/get-inspec/{inspec_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=InspecResponseSchema,
)
async def get_inspect(inspec_id: int, db: Session = Depends(get_db)):
    inspec = read_inspectation(inspec_id, db)

    if inspec is None:
        logger.info(f"Invalid inspec id {inspec_id}")
        raise NotFoundException(detail=f"Invalid inspec id")

    return inspec.__dict__

@router.get(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=List[InspecResponseSchema],
)
async def get_inspecs(db: Session = Depends(get_db)):
    inspec = await all_inspectations(db)
    rs = [i.__dict__ for i in inspec]
    return rs

@router.get(
    "/get-criterias",
    status_code=status.HTTP_201_CREATED,
)
async def get_criterias_api():
    return get_criterias()


@router.put("/update/{id}")
async def update_by_id(
    id: int, inspec: InspecUpdateSchema, db: Session = Depends(get_db)
):
    updated_inspec = await update_inspectation(id, db, inspec.fieldName, inspec.status, inspec.note)
    if updated_inspec is None:
        logger.info(f"Invalid inspec with ID: {id}")
        raise NotFoundException(detail=f"Invalid inspec with ID: {id}")

    logger.info(f"Updated inspec with ID: {id}")
    return updated_inspec.__dict__


