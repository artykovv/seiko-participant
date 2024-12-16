
import asyncio
from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Participant, BinaryBonus



async def get_participant_and_package(participant_id: int, session: AsyncSession):

    result = await session.execute(
        select(Participant)
        .options(selectinload(Participant.paket))
        .where(Participant.id == participant_id)
    )
    participant = result.scalars().first()
    if not participant:
        return None, {"error": f"Участник с ID {participant_id} не найден"}
    
    package = participant.paket

    if not package:
        return None, {"error": "У участника нет пакета"}
    
    return participant, None

def validate_participant_structure(participant):
    if not participant.left_child_id or not participant.right_child_id:
        return {"error": "У участника нет обеих ветвей"}
    return None


# Главная Бинарный бонус
async def calculate_binary_bonus_no_DB(
    participant_id: int, 
    session: AsyncSession
):
    # Получаем участника и его пакет, проверяем ошибки
    participant, error = await get_participant_and_package(participant_id, session)
    if error:
        return error
    
    # Проверяем наличие обеих ветвей у участника
    structure_error = validate_participant_structure(participant)
    if structure_error:
        return structure_error
    
    # Большая и малая ветка
    left_volume = participant.left_volume
    right_volume = participant.right_volume
    small_volume = min(participant.left_volume, participant.right_volume)
    big_volume = max(participant.left_volume, participant.right_volume)


    big_branch_side = 'left' if left_volume > right_volume else 'right'


    # Определение текущего и предыдущего месяца
    current_date = datetime.now()
    previous_month = (current_date.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

    query = select(BinaryBonus).where(
        BinaryBonus.participant_id == participant_id,
        BinaryBonus.period == previous_month
        )
    result = await session.execute(query)

    binary_bonuses = result.scalars().first()



    if left_volume < right_volume:
        small_branch = 'left'
    else:
        small_branch = 'right'

    # Расчет бонуса 

    if small_branch == 'left':
        bonus = small_volume - (binary_bonuses.left_volume_snapshot if binary_bonuses else 0)
        ost = big_volume - (binary_bonuses.right_volume_snapshot if binary_bonuses else 0)

    else:
        bonus = small_volume - (binary_bonuses.right_volume_snapshot if binary_bonuses else 0)
        ost = big_volume - (binary_bonuses.left_volume_snapshot if binary_bonuses else 0)




    b =round(bonus * participant.paket.binary_bonus_percentage, 2)

    if binary_bonuses and binary_bonuses.big_branch_side != big_branch_side:
        residual_volume = (binary_bonuses.residual_volume if binary_bonuses else 0)
        b2 = round(b + residual_volume, 2)
    else:
        b2  = b
        


    # Расчет остатка
    ost2 = round(ost * participant.paket.binary_bonus_percentage, 2)
    ost3 = round(ost2 - b , 2)

    if (binary_bonuses and binary_bonuses.big_branch_side if binary_bonuses else 0) == big_branch_side:
        residual_volume = (binary_bonuses.residual_volume if binary_bonuses else 0)
        df = ost3 + residual_volume
    else:
        df = ost3

    return {
        "small_volume": small_volume,
        "big_volume":big_volume,
        "bonus": b2,
        "ost": df,
    }

    # participant.bonus_binar += b2  # Сначала увеличиваем значение
    # participant.bonus_binar = round(participant.bonus_binar, 2)  # Затем округляем

    # # Сохраняем запись о бонусе
    # binary_bonus = BinaryBonus(
    #     branch_id=participant.branch_id,
    #     participant_id=participant.id,
    #     bonus_amount=b2,
    #     small_volume=small_volume,
    #     big_volume=big_volume,
    #     residual_volume=df,
    #     big_branch_side=big_branch_side,
    #     left_volume_snapshot=participant.left_volume,
    #     right_volume_snapshot=participant.right_volume,
    #     period=datetime.utcnow().strftime("%Y-%m"),
    #     created_at=datetime.utcnow(),
    # )
    # session.add(binary_bonus)
    # await session.commit()