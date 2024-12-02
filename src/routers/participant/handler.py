from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from models import RefBonus, BinaryBonus, ChequeBonus, StatusBonus, SponsorBonus, Participant, Status, СashRefBonus
from sqlalchemy import extract, func, literal, select, text, union_all
from sqlalchemy.orm import selectinload


async def bonuses(
    participant_id: int,
    session: AsyncSession
):
    current_date = datetime.utcnow()
    current_year = current_date.year
    current_month = current_date.month

    first_day_of_current_month = current_date.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    previous_month = last_day_of_previous_month.month
    previous_year = last_day_of_previous_month.year

    async def calculate_bonus_sum(table, column, filters):
        query = select(func.sum(column)).where(*filters)
        result = await session.execute(query)
        return round(float(result.scalar() or 0), 2)

    bonuses = {
        "referral": {"table": RefBonus, "column": RefBonus.amount, "id_column": RefBonus.participant_id},
        "binary": {"table": BinaryBonus, "column": BinaryBonus.bonus_amount, "id_column": BinaryBonus.participant_id},
        "cheque": {"table": ChequeBonus, "column": ChequeBonus.bonus_amount, "id_column": ChequeBonus.participant_id},
        "status": {"table": StatusBonus, "column": StatusBonus.bonus, "id_column": StatusBonus.participant_id},
        "sponsor": {"table": SponsorBonus, "column": SponsorBonus.bonus, "id_column": SponsorBonus.participant_id}
    }

    summary = {"total": 0, "current_month": 0, "previous_month": 0}

    for bonus_data in bonuses.values():
        table = bonus_data["table"]
        column = bonus_data["column"]
        id_column = bonus_data["id_column"]

        # Total
        summary["total"] += await calculate_bonus_sum(
            table, column, [id_column == participant_id]
        )

        # Current month
        summary["current_month"] += await calculate_bonus_sum(
            table,
            column,
            [
                id_column == participant_id,
                extract('year', table.created_at) == current_year,
                extract('month', table.created_at) == current_month
            ]
        )

        # Previous month
        summary["previous_month"] += await calculate_bonus_sum(
            table,
            column,
            [
                id_column == participant_id,
                extract('year', table.created_at) == previous_year,
                extract('month', table.created_at) == previous_month
            ]
        )

    # Округляем итоговые суммы
    summary = {key: round(value, 2) for key, value in summary.items()}

    return summary



async def status(
    participant_id: int,
    session: AsyncSession 
):
    """
    Получение необходимого оборота для повышения статуса участника.
    """
    # Получаем данные участника
    participant_query = select(Participant).where(Participant.id == participant_id)
    participant_result = await session.execute(participant_query)
    participant = participant_result.scalar()

    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    # Вычисляем минимальный объем (например, для расчета бонуса)
    small_volume = min(participant.left_volume, participant.right_volume)

    # Увеличиваем статус участника
    next_status_id = participant.status_id + 1

    # Получаем данные следующего статуса
    status_query = select(Status).where(Status.id == next_status_id)
    status_result = await session.execute(status_query)
    next_status = status_result.scalar()

    if not next_status:
        raise HTTPException(status_code=404, detail="Next status not found")

    return {
        "status_name": next_status.name,
        "required_turnover": next_status.required_turnover
        }


async def gifts(
    participant_id: int,
    session: AsyncSession
):
    """
    For homepage
    """
    participant_query = select(Participant).where(Participant.id == participant_id)
    participant_result = await session.execute(participant_query)
    participant = participant_result.scalar()

     # Логика определения бонусов по статусу
    if participant.status_id < 8:
        status_query = select(Status).where(Status.id == 8)
        status_result = await session.execute(status_query)
        status = status_result.scalar()
        return {
            "bonus_name": "Особый бонус",
            "required_turnover": status.required_turnover
        }
    elif participant.status_id < 9:
        status_query = select(Status).where(Status.id == 9)
        status_result = await session.execute(status_query)
        status = status_result.scalar()
        return {
            "bonus_name": "Туристический бонус",
            "required_turnover": status.required_turnover
        }
    elif participant.status_id < 12:
        return {
            "bonus_name": "Туристический бонус",
            "required_turnover":"1 Личник GOLD SEIKO"
        }
    else:
        bonus_message = "Статус неизвестен или нет дополнительных бонусов"


# Рекурсивная функция для получения потомков
async def get_descendants(participant_id: int, session: AsyncSession, level: int = 1):
    if level > 2:  # Ограничиваем уровень глубины
        return None
    
    # Находим участника по ID
    participant = await session.execute(
        select(Participant)
        .options(
            selectinload(Participant.paket)
        )
        .filter(Participant.id == participant_id)
    )
    participant = participant.scalars().first()

    if not participant:
        return None

    # Получаем левых и правых потомков
    left_child = await get_descendants(participant.left_child_id, session, level + 1) if participant.left_child_id else None
    right_child = await get_descendants(participant.right_child_id, session, level + 1) if participant.right_child_id else None

    # Формируем ответ для текущего участника
    return {
        "participant_id": participant.id,
        "participant_name": participant.name,
        "participant_lastname": participant.lastname,
        "participant_patronymic": participant.patronymic,
        "color": participant.paket.color,
        "participant_personal_number": participant.personal_number,
        "left_child": left_child,
        "right_child": right_child
    }


async def get_participant(participant_id, session):
    query = (
        select(
            Participant
        )
        .options(
            selectinload(Participant.status),
            selectinload(Participant.paket)
        )
        .where(
            Participant.id == participant_id, 
            Participant.registered == True
        )
    )
    result = await session.execute(query)
    participant = result.scalars().first()
    return participant

async def get_bonuses_summary(
    participant_id: int,
    session: AsyncSession
):
    """
    Для страницы Участники кнопка "B" бонусы
    """
    # Текущая дата
    current_date = datetime.utcnow()
    current_year = current_date.year
    current_month = current_date.month

    # Предыдущий месяц
    first_day_of_current_month = current_date.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    previous_month = last_day_of_previous_month.month
    previous_year = last_day_of_previous_month.year

    # Helper function to calculate bonuses
    async def calculate_bonus_sum(table, column, filters):
        query = select(func.sum(column)).where(*filters)
        result = await session.execute(query)
        return round(float(result.scalar() or 0), 2)  # Приведение к float и округление

    # Calculate all types of bonuses
    bonuses = {
        "referral": {"table": RefBonus, "column": RefBonus.amount, "id_column": RefBonus.participant_id},
        "binary": {"table": BinaryBonus, "column": BinaryBonus.bonus_amount, "id_column": BinaryBonus.participant_id},
        "cheque": {"table": ChequeBonus, "column": ChequeBonus.bonus_amount, "id_column": ChequeBonus.participant_id},
        "status": {"table": StatusBonus, "column": StatusBonus.bonus, "id_column": StatusBonus.participant_id},
        "sponsor": {"table": SponsorBonus, "column": SponsorBonus.bonus, "id_column": SponsorBonus.participant_id}
    }

    summary = {"total": {}, "current_month": {}, "previous_month": {}}

    for bonus_name, bonus_data in bonuses.items():
        table = bonus_data["table"]
        column = bonus_data["column"]
        id_column = bonus_data["id_column"]

        # Total
        summary["total"][bonus_name] = await calculate_bonus_sum(
            table, column, [id_column == participant_id]
        )

        # Current month
        summary["current_month"][bonus_name] = await calculate_bonus_sum(
            table,
            column,
            [
                id_column == participant_id,
                extract('year', table.created_at) == current_year,
                extract('month', table.created_at) == current_month
            ]
        )

        # Previous month
        summary["previous_month"][bonus_name] = await calculate_bonus_sum(
            table,
            column,
            [
                id_column == participant_id,
                extract('year', table.created_at) == previous_year,
                extract('month', table.created_at) == previous_month
            ]
        )

    # Calculate total for all bonuses
    for period in ["total", "current_month", "previous_month"]:
        summary[period]["all_bonuses"] = round(
            sum(summary[period].values()), 2
        )

    return summary


# Маппинг для русификации типов бонусов
BONUS_TYPE_TRANSLATIONS = {
    "status_bonus": "Статусный",
    "sponsor_bonus": "Спонсорский",
    "ref_bonus": "Реферальный",
    "cheque_bonus": "Чек от чека",
    "binary_bonus": "Бинарный",
}


async def get_participant_bonuses_history(
    participant_id: int,
    session: AsyncSession
):
    """
    Для страницы Участники кнопка "B" бонусы и дальше кнопка история бонусов
    
    """
    # Запросы для каждого типа бонусов
    queries = []

    queries.append(
        select(
            StatusBonus.bonus.label("bonus_amount"),
            literal("status_bonus").label("bonus_type"),
            StatusBonus.created_at
        ).where(
            StatusBonus.participant_id == participant_id
        )
    )

    queries.append(
        select(
            SponsorBonus.bonus.label("bonus_amount"),
            literal("sponsor_bonus").label("bonus_type"),
            SponsorBonus.created_at
        ).where(
            SponsorBonus.participant_id == participant_id
        )
    )

    queries.append(
        select(
            RefBonus.amount.label("bonus_amount"),
            literal("ref_bonus").label("bonus_type"),
            RefBonus.created_at
        ).where(
            RefBonus.participant_id == participant_id
        )
    )

    queries.append(
        select(
            ChequeBonus.bonus_amount.label("bonus_amount"),
            literal("cheque_bonus").label("bonus_type"),
            ChequeBonus.created_at
        ).where(
            ChequeBonus.participant_id == participant_id
        )
    )

    queries.append(
        select(
            СashRefBonus.amount.label("bonus_amount"),
            СashRefBonus.bonus_type.label("bonus_type"),
            СashRefBonus.created_at
        ).where(
            СashRefBonus.participant_id == participant_id
        )
    )

    queries.append(
        select(
            BinaryBonus.bonus_amount.label("bonus_amount"),
            literal("binary_bonus").label("bonus_type"),
            BinaryBonus.created_at
        ).where(
            BinaryBonus.participant_id == participant_id
        )
    )

    # Объединяем все запросы
    unified_query = union_all(*queries).order_by(text("created_at DESC"))  # Используем text() для сортировки

    # Выполнение объединённого запроса
    result = await session.execute(unified_query)

    # Форматируем результаты с переводом типов бонусов
    bonuses = [
        {
            "bonus_type": BONUS_TYPE_TRANSLATIONS.get(row.bonus_type, "Неизвестный бонус"),
            "bonus_amount": row.bonus_amount,
            "created_at": row.created_at
        }
        for row in result.fetchall()
    ]

    return {"participant_id": participant_id, "bonuses": bonuses}



async def get_participant_with_sponsored(
    participant_id: int,
    page: int,
    page_size: int,
    in_or_none: bool,
    session: AsyncSession
    # current_user: User = Depends(fastapi_users.current_user())
):
    """
    Для страницы Личники
    """
    offset = (page - 1) * page_size

    # return participants
    total_count_query = select(func.count()).select_from(Participant).where(Participant.sponsor_id == participant_id, Participant.registered == in_or_none)
    total_count = await session.scalar(total_count_query)
    total_pages = (total_count + page_size - 1) // page_size

    result = await session.execute(
        select(Participant)
        .options(
            selectinload(Participant.branch),
            selectinload(Participant.paket)
        )
        .where(Participant.sponsor_id == participant_id, Participant.registered == in_or_none)
        .offset(offset)
        .limit(page_size)
    )
    participants = result.scalars().all()

    # Преобразование данных в нужный формат
    response = []
    for p in participants:

        # Определение small_volume и big_volume
        small_volume = min(p.left_volume, p.right_volume)
        big_volume = max(p.left_volume, p.right_volume)

        response.append({
            "id": p.id,
            "personal_number": p.personal_number,
            "name": p.name,
            "lastname": p.lastname,
            "patronymic": p.patronymic,
            "register_at": p.register_at,
            "paket": {
                "id": p.paket.id if p.paket else None,
                "name": p.paket.name if p.paket else None
            },
            "branch": {
                "id": p.branch.id if p.branch else None,
                "name": p.branch.name if p.branch else None
            },
            "volumes": {
                "small_volume": small_volume,
                "big_volume": big_volume
            }
        })
    
    return {
        "page": page,
        "total_pages": total_pages,
        "participants": response
    }