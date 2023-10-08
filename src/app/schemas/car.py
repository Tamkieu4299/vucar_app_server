from pydantic import  BaseModel


class CreateCarSchema(BaseModel):
    name: str
    model: str

    class Config:
        orm_mode = True


class CarResponseSchema(BaseModel):
    car_id: int
    name: str
    model: str

    class Config:
        orm_mode = True

