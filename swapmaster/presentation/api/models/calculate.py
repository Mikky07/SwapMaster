from pydantic import BaseModel, ValidationInfo, field_validator

from swapmaster.application.calculate_send_total import CalculateTotalDTO
from swapmaster.core.models import PairId


class CalculateData(BaseModel):
    pair_id: PairId
    to_receive_quantity: float

    @field_validator('to_receive_quantity')
    @classmethod
    def check_commission_range(cls, v, info: ValidationInfo):
        if not (0 <= v <= 100):
            raise ValueError(f"{info.field_name} must be from 0 to 100!")
        return v
