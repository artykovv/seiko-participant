from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, insert, select

from models import Paket, User, Branch, Participant
from functions.func import generate_code
from database import get_async_session
from core.fastapi_users_instance import fastapi_users

router = APIRouter(tags=["site"])

@router.get("/participant/personal_number")
async def get_personal_number():
    """
    Для страницы Регистрации
    Генерация уникального кода для участникаов
    """
    code = await generate_code()
    return {"personal_number": code}


@router.get("/pakets")
async def get_all_status(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Для Страницы изменение участника, регистрации, добавление в структуру
    получить пакеты с id
    """
    query = select(
        Paket.id,
        Paket.name
    )
    result = await session.execute(query)
    pakets = result.all()

    pakets_list = [
        {
            "id": s.id,
            "name": s.name
        } for s in pakets
    ]
    return pakets_list

# Получить все филиалы
@router.get("/branches")
async def get_all_branches(
    session: AsyncSession = Depends(get_async_session),
    ):
    """
    Для страницы Филиалы
    Запрос на получение всех филиалов
    """
     
    query = select(
        Branch.id,
        Branch.code,
        Branch.name,
        Branch.address
    )
    result = await session.execute(query)
    branches = result.all()

    branches_list = [
        {
            "id": b.id,
            "code": b.code,
            "name": b.name,
            "address": b.address,

        } for b in branches
    ]
    return branches_list

@router.get("/participants")
async def get_participants_in_structure_for_site(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Для страницы регистрации
    Получить списиок пользователей для сайта а именно для регистриации где можно выбрать спонсора
    """
    query = select(
        Participant.id,
        Participant.name,
        Participant.lastname,
        Participant.patronymic,
        Participant.personal_number
    ).where(Participant.registered == True).order_by(desc(Participant.register_at))

    result = await session.execute(query)
    participants = result.all()

    # Преобразование в список словарей
    participants_data = [
        {
            "id": row.id,
            "name": row.name,
            "lastname": row.lastname,
            "patronymic": row.patronymic,
            "personal_number": row.personal_number
        }
        for row in participants
    ]

    return participants_data