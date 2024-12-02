
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from config.models_config import Base

# Таблица для филлиалов
class Branch(Base):
    __tablename__ = 'branches'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String) 
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    participants = relationship('Participant', back_populates='branch')
    users = relationship("User", secondary="user_branches", back_populates="branches")

# Ассоциативная таблица UserBranches (Филиалы пользователей)
user_branches = Table(
    'user_branches',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('branch_id', ForeignKey('branches.id'), primary_key=True)
)