from fastapi import APIRouter

from .auth.router import router as auth
from .participant.router import router as participant
from .bonuses.router import router as bonus
from .site.router import router as site

routers = APIRouter()


routers.include_router(auth)
routers.include_router(participant)
routers.include_router(bonus)
routers.include_router(site)
