from fastapi import APIRouter

from .auth.router import router as auth
from .participant.router import router as participant
from .bonuses.router import router as bonus

routers = APIRouter()


routers.include_router(auth)
routers.include_router(participant)
routers.include_router(bonus)