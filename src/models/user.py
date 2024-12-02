from datetime import datetime
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from config.models_config import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    branch = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    register_at = Column(DateTime, nullable=True, default=datetime.utcnow)

    # Отношения
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    branches = relationship("Branch", secondary="user_branches", back_populates="users")
    permissions = relationship("Permission", secondary="user_permissions", back_populates="users")