from pydantic import BaseModel, ValidationInfo, field_validator

from swapmaster.application.create_commission import NewCommissionDTO


class Commission(BaseModel):
    value: float

    @field_validator('value')
    @classmethod
    def check_commission_range(cls, v, info: ValidationInfo):
        if not (0 <= v <= 100):
            raise ValueError(f"{info.field_name} must be from 0 to 100!")
        return v

    def to_dto(self) -> NewCommissionDTO:
        return NewCommissionDTO(
            value=self.value
        )
