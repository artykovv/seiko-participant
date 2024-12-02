from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from config.models_config import Base

# Таблица Permissions (Разрешения)
class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String, unique=True, nullable=False)

    # Отношения
    users = relationship("User", secondary="user_permissions", back_populates="permissions")

user_permissions = Table(
    'user_permissions',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('permission_id', ForeignKey('permissions.id'), primary_key=True)
)