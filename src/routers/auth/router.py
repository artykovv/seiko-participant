from fastapi import APIRouter, Depends
from core.fastapi_users_instance import fastapi_users
from core.auth import auth_backend
from schemas.participants import ParticipantRead, ParticipantUpdate, ParticipantReadResponse
from models import Participant

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

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

