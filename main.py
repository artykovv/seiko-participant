from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.cashe import lifespan
from routers.routers import routers
import logging



logging.basicConfig(level=logging.DEBUG)

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)


app.include_router(routers)