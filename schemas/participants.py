from datetime import date, datetime
from typing import List, Optional
from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict
from schemas import PaketBase, StatusBase
from schemas.branches import Branch


class ParticipantResponse(BaseModel):
    success: bool
    detail: str

class ParticipantCreate(schemas.BaseUserCreate):
    is_superuser: bool = False
    is_active: bool = True
    is_verified: bool = False

    sponsor_id: Optional[int]

    name: str
    lastname: str
    patronymic: str

    phone_number: Optional[str]
    personal_info: Optional[str]
    address: Optional[str]
    birth_date: Optional[date]
    pin: Optional[str]
    passport_id: Optional[str]
    passport_issuer: Optional[str]
    passport_issue_date: Optional[date]
    bank: Optional[str]
    ip_inn: Optional[bool]
    pensioner: Optional[bool]
    paket_id: Optional[int]
    branch_id: Optional[int]

    code: Optional[str]


class ParticipantBase(BaseModel):
    id: int
    name: str
    lastname: str
    patronymic: str
    personal_number: str
    model_config = ConfigDict(from_attributes=True)

class Sponsor(BaseModel):
    id: int
    name: str
    lastname: str
    patronymic: str
    personal_number: str

class Mentor(BaseModel):
    id: int
    name: str
    lastname: str
    patronymic: str
    personal_number: str

class ParticipantInfo(schemas.BaseUser):
    phone_number: Optional[str]
    email: Optional[str]
    register_at: Optional[datetime]  
    bank: Optional[str]
    personal_info: Optional[str]
    ip_inn: Optional[bool]
    pensioner: Optional[bool]
    mentor: Optional[Mentor] = None
    sponsor: Optional[Sponsor] = None


class ParticipantUpdate(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[str] = None
    bank: Optional[str] = None
    password: Optional[str] = None
    personal_info: Optional[str] = None
    ip_inn: Optional[bool] = None
    pensioner: Optional[bool] = None


class PersonalNumberInfo(BaseModel):
    id: int
    personal_number: Optional[str]
    name: Optional[str]
    lastname: Optional[str]
    patronymic: Optional[str]
    email: Optional[str]
    personal_info: Optional[str]
    birth_date: Optional[datetime]
    phone_number: Optional[str]
    bank: Optional[str]
    paket: Optional[PaketBase] = None
    mentor: Optional[Mentor] = None
    sponsor: Optional[Sponsor] = None
    branch: Optional[Branch] = None
    model_config = ConfigDict(from_attributes=True)

class ParticipantRead(schemas.BaseUser):
    name: str
    lastname: str
    patronymic: str
    personal_number: str
    left_volume: int
    right_volume: int

class ParticipantReadResponse(ParticipantRead):
    paket: Optional[PaketBase] = None
    status: Optional[StatusBase] = None
    model_config = ConfigDict(from_attributes=True)