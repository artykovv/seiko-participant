from fastapi import APIRouter, Depends
from sqlalchemy import insert
from core.fastapi_users_instance import fastapi_users
from core.auth import auth_backend
from functions.generate_personal_number import generate_personal_number
from schemas.participants import ParticipantUpdate, ParticipantReadResponse, ParticipantCreate, ParticipantResponse
from models import Participant
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session

from fastapi_users.password import PasswordHelper


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


@router.post("/auth/register",  tags=["auth"])
async def register(
    participants_create: ParticipantCreate,
    session: AsyncSession = Depends(get_async_session),
):
    number = participants_create.code
    personal_number = await generate_personal_number(session, participants_create.branch_id, participants_create.code)
    print(participants_create)

    # Добавляем сгенерированные данные в схему для создания
    participant_data = participants_create.dict()
    participant_data['number'] = number
    participant_data['personal_number'] = personal_number


    password_helper = PasswordHelper()
    participant_data['hashed_password'] = password_helper.hash(participants_create.password)
    participant_data.pop('password', None)  # Убираем пароль


    # Убираем code нету в модели
    participant_data.pop('code', None)

    # Создание нового участника
    stmt = insert(Participant).values(participant_data)
    result = await session.execute(stmt)
    await session.commit()

    return ParticipantResponse(success=True, detail="Participant created successfully")

router.include_router(
    fastapi_users.get_users_router(ParticipantReadResponse, ParticipantUpdate),
    prefix="/users",
    tags=["users"],
)

@router.get("/auth/validate-token", tags=["auth"])
async def validate_token(current_user: Participant = Depends(fastapi_users.current_user())):
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid token or user not found")
    
    return {"message": "Token is valid", "user": current_user}

@router.get("/auth/validate-page", tags=["auth"])
async def validate_token(current_user: Participant = Depends(fastapi_users.current_user())):
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid token or user not found")
    
    return {"message": "Token is valid", "Page": current_user.registered}

