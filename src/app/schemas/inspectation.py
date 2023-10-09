from pydantic import  BaseModel


class CreateInspecSchema(BaseModel):
    user_id: int
    car_id: int
    stats: dict = {}

    class Config:
        orm_mode = True


class InspecResponseSchema(BaseModel):
    inspectation_id: int
    user_id: int
    car_id: int
    stats: dict

    class Config:
        orm_mode = True

class InspecUpdateSchema(BaseModel):
    fieldName: str
    status: bool
    note: str = None

    class Config:
        orm_mode = True

