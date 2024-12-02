from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import extract, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from sqlalchemy.orm import selectinload, joinedload
from fastapi_users.password import PasswordHelper

from database import get_async_session
from models import Participant, Paket, User
from core.fastapi_users_instance import fastapi_users
from schemas.paket import PaketBase
from .handler import bonuses, get_descendants, get_participant, get_participant_bonuses_history, get_participant_with_sponsored, status, gifts, get_bonuses_summary
from schemas.participants import ParticipantBase, ParticipantInfo, ParticipantUpdate, PersonalNumberInfo

router = APIRouter()

@router.get("/info", response_model=ParticipantInfo)
async def get_participant_data(
    session: AsyncSession = Depends(get_async_session),
    current_user: Participant = Depends(fastapi_users.current_user())
):

    query = select(Participant).where(Participant.id == current_user.id).options(
        selectinload(Participant.mentor),
        selectinload(Participant.sponsor),
    )
    result = await session.execute(query)
    participant = result.scalar()
    return participant

@router.get("/bonuses_summary/")
async def get_p_hm(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user())

):
    id = current_user.id
    """
    For homepage
    """
    b = await bonuses(participant_id=id, session=session)
    s = await status(participant_id=id, session=session)
    g = await gifts(participant_id=id, session=session)

    data = {
        "bonuses": b,
        "status": s,
        "gifts": g
    }

    return data


@router.get("/children")
async def get_children(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user())
    ):

    """
    Для страницы Структура
    """

    # Получаем потомков для левого и правого дочерних участников
    left_child = await get_descendants(current_user.left_child_id, session) if current_user.left_child_id else None
    right_child = await get_descendants(current_user.right_child_id, session) if current_user.right_child_id else None

    # Формируем ответ
    response = {
        "participant_id": current_user.id,
        "participant_name": current_user.name,
        "participant_lastname": current_user.lastname,
        "participant_patronymic": current_user.patronymic,
        "participant_personal_number": current_user.personal_number,
        "color": current_user.paket.color,
        "left_child": left_child,
        "right_child": right_child
    }

    return response

@router.get("/info/{participant_id}", response_model=PersonalNumberInfo)
async def get_participant_data(
    participant_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Participant = Depends(fastapi_users.current_user())
):

    query = select(Participant).where(Participant.id == participant_id).options(
        selectinload(Participant.mentor),
        selectinload(Participant.sponsor),
        selectinload(Participant.paket),
        selectinload(Participant.branch),
    )
    result = await session.execute(query)
    participant = result.scalar()
    return participant


@router.get("/children/{participant_id}/")
async def get_children(
    participant_id: int, 
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user())
    ):

    """
    Для страницы Структура
    """
    participant = await session.execute(
        select(Participant)
        .options(
            selectinload(Participant.paket)
        )
        .filter(Participant.id == participant_id)
    )
    participant = participant.scalars().first()

    if not participant:
        return {"detail": "Participant not found"}

    # Получаем потомков для левого и правого дочерних участников
    left_child = await get_descendants(participant.left_child_id, session) if participant.left_child_id else None
    right_child = await get_descendants(participant.right_child_id, session) if participant.right_child_id else None

    # Формируем ответ
    response = {
        "participant_id": participant.id,
        "participant_name": participant.name,
        "participant_lastname": participant.lastname,
        "participant_patronymic": participant.patronymic,
        "participant_personal_number": participant.personal_number,
        "color": participant.paket.color,
        "left_child": left_child,
        "right_child": right_child
    }

    return response

@router.get("/turnover/details/{participant_id}")
async def participant_turnover_details(
    participant_id: int,
    session: AsyncSession = Depends(get_async_session),
    # current_user: User = Depends(fastapi_users.current_user())
):
    """
    Для модального окна а именно Структура кнопка Подробнее
    """
    participant = await get_participant(participant_id, session)
    
    stmt = select(func.count(Participant.id)).where(Participant.sponsor_id == participant_id)
    result = await session.execute(stmt)
    count = result.scalar()  # Получаем одно значение (количество)
    sponsored = count

    return {
        "paket": participant.paket.name,
        "left_volume": participant.left_volume,
        "right_volume": participant.right_volume,
        "bonus_binar": participant.bonus_binar,
        "sponsored": sponsored,
        "descendants": {
            "left_descendants": participant.left_descendants,
            "right_descendants": participant.right_descendants
        }
    }

@router.get("/balance/")
async def get_participant_balance(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user())
):
    """
    БАЛАНС
    """
    balance = await get_bonuses_summary(current_user.id, session)
    return balance

@router.get("/balance/history")
async def get_participant_balance_history(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user())
):
    history = await get_participant_bonuses_history(current_user.id, session)
    return history


@router.get("/sponsored/structure/")
async def sponsored_participants(
    in_or_none: bool,
    page: int = Query(1, ge=1),
    page_size: int = Query(3, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user())
):
   data = await get_participant_with_sponsored(
        participant_id=current_user.id, 
        page=page, 
        page_size=page_size, 
        in_or_none=in_or_none, 
        session=session
    )
   return data


@router.put("/update")
async def update(
    new: ParticipantUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user())
):
    update_data = new.dict(exclude_unset=True)

    if 'password' in update_data:
        password_helper = PasswordHelper()
        update_data['hashed_password'] = password_helper.hash(new.password)
    update_data.pop('password', None)  # Удаляем оригинальный пароль

    if update_data:  # Если есть данные для обновления
        for key, value in update_data.items():
            setattr(current_user, key, value)
        session.add(current_user)  # Убедитесь, что объект добавлен в сессию
        await session.commit()
        await session.refresh(current_user)

    return {"message:" "update success"}



@router.get("/search/participants", response_model=List[ParticipantBase])
async def search_participants(
    query: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_async_session),
    current_user: Participant = Depends(fastapi_users.current_user())
):
    """
    Эндпоинт для поиска участников в структуре текущего пользователя.
    Показывает только потомков текущего пользователя (и их потомков, рекурсивно).
    """
    if not query:
        raise HTTPException(status_code=400, detail="Параметр поиска обязателен")
    
    # Рекурсивная функция для получения всех потомков текущего пользователя
    async def get_descendants_ids(user_id: int, collected_ids: set):
        # Отладочное сообщение
        print(f"Поиск потомков для ID: {user_id}")

        # Запрос для получения прямых потомков
        descendants = await session.execute(
            select(Participant.id).where(
                Participant.parent_id == user_id  # Проверяем только parent_id для ясности
            )
        )
        descendant_ids = descendants.scalars().all()

        # Лог отладки
        print(f"Найденные потомки для ID {user_id}: {descendant_ids}")

        for descendant_id in descendant_ids:
            if descendant_id not in collected_ids:
                collected_ids.add(descendant_id)
                # Рекурсивный вызов для поиска потомков текущего потомка
                await get_descendants_ids(descendant_id, collected_ids)


    # Собираем ID всех потомков текущего пользователя
    descendants_ids = set()
    await get_descendants_ids(current_user.id, descendants_ids)

    if not descendants_ids:
        raise HTTPException(status_code=404, detail="Потомки не найдены")

    # Основной фильтр для поиска
    search_filter = or_(
        Participant.name.ilike(f"%{query}%"),
        Participant.email.ilike(f"%{query}%"),
        Participant.phone_number.ilike(f"%{query}%"),
        Participant.number.ilike(f"%{query}%"),
        Participant.personal_number.ilike(f"%{query}%"),
    )

    # Запрос для поиска участников среди потомков текущего пользователя
    query = select(Participant).where(
        Participant.id.in_(descendants_ids),
        Participant.registered == True,
        search_filter
    ).order_by(Participant.name)

    result = await session.execute(query)
    participants = result.scalars().all()

    return participants
