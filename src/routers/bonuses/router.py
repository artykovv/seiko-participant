from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_async_session
from models import Participant, BinaryBonus, RefBonus, ChequeBonus, StatusBonus, SponsorBonus, Status
from core.fastapi_users_instance import fastapi_users
from schemas.bonuses import BinarSchema, ChequeBonusSchema, StatusBonusSchema

router = APIRouter(prefix="/bonus" ,tags=["bonuses"])

@router.get("/binar")
async def binar(
    session: AsyncSession = Depends(get_async_session),
    current_user: Participant = Depends(fastapi_users.current_user())
):
    query = (
        select(
            BinaryBonus
        ).where(
            BinaryBonus.participant_id == current_user.id
        )
    )
    result = await session.execute(query)
    bibar = result.scalars().all()
    return bibar


@router.get("/referal", response_model=List[BinarSchema])
async def referal(
    session: AsyncSession = Depends(get_async_session),
    current_user: Participant = Depends(fastapi_users.current_user())
):
    query = (
        select(
            RefBonus
        )
        .options(
            selectinload(RefBonus.from_participant)
        )
        .where(
            RefBonus.participant_id == current_user.id
        )
    )
    result = await session.execute(query)
    referal = result.scalars().all()
    return referal

@router.get("/cheque")
async def get_cheque_bonuses(
    session: AsyncSession = Depends(get_async_session),
    current_user: Participant = Depends(fastapi_users.current_user())
):
    # Извлечение данных из ChequeBonus
    query = (
        select(ChequeBonus)
        .where(ChequeBonus.participant_id == current_user.id)
    )
    result = await session.execute(query)
    cheque_bonuses = result.scalars().all()


    from_ids = [bonus.from_id for bonus in cheque_bonuses]
    participants_query = (
        select(Participant)
        .where(Participant.id.in_(from_ids))
    )
    participants_result = await session.execute(participants_query)
    participants = {p.id: p for p in participants_result.scalars().all()}

    # Формирование ответа
    response = [
        {
            "id": bonus.id,
            "branch_id": bonus.branch_id,
            "bonus_amount": bonus.bonus_amount,
            "from": participants.get(bonus.from_id).personal_number if bonus.from_id in participants else None,
            "depth": bonus.depth,
            "created_at": bonus.created_at,
        }
        for bonus in cheque_bonuses
    ]

    return response

@router.get("/status", response_model=List[StatusBonusSchema])
async def referal(
    session: AsyncSession = Depends(get_async_session),
    current_user: Participant = Depends(fastapi_users.current_user())
):
    query = (
        select(
            StatusBonus
        )
        .options(
            selectinload(StatusBonus.status)
        )
        .where(
            StatusBonus.participant_id == current_user.id
        )
    )
    result = await session.execute(query)
    referal = result.scalars().all()
    return referal

@router.get("/sponsor",)
async def referal(
    session: AsyncSession = Depends(get_async_session),
    current_user: Participant = Depends(fastapi_users.current_user())
):
    query = (
        select(SponsorBonus)
        .where(SponsorBonus.participant_id == current_user.id)
    )
    result = await session.execute(query)
    sponsor_bonuses = result.scalars().all()

    from_ids = [i.sponsored for i in sponsor_bonuses]
    participants_query = (
        select(Participant)
        .where(Participant.id.in_(from_ids))
    )
    participants_result = await session.execute(participants_query)
    participants = {p.id: p for p in participants_result.scalars().all()}

    # Формирование ответа
    response = [
        {
            "id": bonus.id,
            "branch_id": bonus.branch_id,
            "bonus": bonus.bonus,
            "from": participants.get(bonus.sponsored).personal_number if bonus.sponsored in participants else None,
            "created_at": bonus.created_at,
        }
        for bonus in sponsor_bonuses
    ]

    return response
    

@router.get("/gift")
async def gift(
    current_user: Participant = Depends(fastapi_users.current_user())
):
    id = current_user.status_id
    volume = {
        "left_volume": current_user.left_volume,
        "right_volume": current_user.right_volume
    }
    # Логика определения бонусов по статусу
    if id < 8:
        return {
            "bonus_name": "Особый бонус",
            "volumes": volume,
            "required_turnover": "73000",
            "bonus_description": "При достижении статуса RED DIAMOND и выше компания может предоставить неопределенный бонус по своему усмотрению."
        }
    elif id < 9:
        return {
            "bonus_name": "Туристический бонус",
            "required_turnover": "147000",
            "volumes": volume,
            "bonus_description": "Этот бонус активируется при достижении статуса BLACK DIAMOND и предоставляет участнику возможность совершить поездку за границу."
        }
    elif id < 12:
        return {
            "bonus_name": "Автопрограмма",
            "required_turnover": "1 Личник DIAMOND SEIKO",
            "volumes": volume,
            "bonus_description":"При достижении статуса DIAMOND SEIKO участник получает единоразовый бонус в рамках программы автопрограммы."
        }
    else:
        return{
            "bonus_name": "Статус неизвестен или нет дополнительных бонусов"
        }
        