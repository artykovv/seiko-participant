from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from config.models_config import Base

# Таблица Roles (Роли)
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String, unique=True, nullable=False)

    # Отношения
    users = relationship("User", secondary="user_roles", back_populates="roles")

# Ассоциативная таблица UserRoles (Роли пользователей)
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True)
)