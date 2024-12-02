
from pydantic import BaseModel, ConfigDict

class PaketBase(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class PaketRead(PaketBase):
    id: int
    model_config = ConfigDict(from_attributes=True)