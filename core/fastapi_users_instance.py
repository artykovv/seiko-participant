from fastapi_users import FastAPIUsers
from uuid import UUID
from models import Participant
from .auth import auth_backend
from .user_manager import get_user_manager

fastapi_users = FastAPIUsers[Participant, int](
    get_user_manager,
    [auth_backend],
)