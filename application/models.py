from pydantic import BaseModel
from uuid import UUID
from typing import Union


class DroneModel(BaseModel):
    drone_id: Union[UUID, None]
    serial_number: str
    model_id: int
    weight_limit: float
    battery_capacity: float
    state_id: int


class MedicationModel(BaseModel):
    medication_id: Union[UUID, None]
    drone_id: UUID
    name: str
    weight: float 
    code: str
    image: Union[bytes, None]