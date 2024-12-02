from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class StatusBonusStatusSchema(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
class StatusBonusSchema(BaseModel):
    id: int
    bonus: int
    left_volume_snapshot: int
    right_volume_snapshot: int
    created_at: datetime
    status: Optional[StatusBonusStatusSchema] = None
    model_config = ConfigDict(from_attributes=True)


class Participant(BaseModel):
    id: int
    personal_number: str
    model_config = ConfigDict(from_attributes=True)

class ChequeBonusSchema(BaseModel):
    id: int
    bonus_amount:int
    depth: int
    created_at: datetime
    from_: Optional[Participant] = Field(default=None, alias="from")

class BinarSchema(BaseModel):
    id: int
    amount: int
    created_at: datetime
    from_participant: Optional[Participant] = None
    model_config = ConfigDict(from_attributes=True)