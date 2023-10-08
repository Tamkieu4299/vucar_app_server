from fastapi import APIRouter, Depends, status
from ..schemas.inspectation import CreateInspecSchema, InspecResponseSchema
from ..utils.logger import setup_logger
from ..db.database import get_db
from sqlalchemy.orm import Session
from ..models.inspectation import Inspectation
from ..crud.inspectation import add_inspectation
from ..utils.crawl_data import get_criterias

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
    "/get-criterias",
    status_code=status.HTTP_201_CREATED,
)
async def get_criterias_api():
    return get_criterias()