from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from sqlalchemy import UUID, select
from sqlalchemy.orm import selectinload
from models import Participant
from .user_db import get_user_db
from config.config import SECRET
from database import async_session_maker

class UserManager(IntegerIDMixin, BaseUserManager[Participant, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def get(self, user_id: int) -> Optional[Participant]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Participant)
                .options(
                    selectinload(Participant.paket),
                    selectinload(Participant.status)
                )
                .where(Participant.id == user_id)
            )
            user = result.scalars().first()
            return user

    async def on_after_register(self, user: Participant, request: Optional[Request] = None):
        pass

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)