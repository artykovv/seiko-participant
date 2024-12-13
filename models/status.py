
from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship
from config.models_config import Base

# Таблица для статусов участников
class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    required_turnover = Column(BigInteger, nullable=True) # Необходимый товарооборот для достижения уровня
    bonus_percentage = Column(Integer, nullable=True)  # Приз виде денег при достжении этого статуса

    sponsor_bonus = Column(Integer, nullable=True) # Приз который получит спонсор

    # Для бонуса чек от чека
    depth_1 = Column(Float, nullable=True)
    depth_2 = Column(Float, nullable=True)
    depth_3 = Column(Float, nullable=True)
    depth_4 = Column(Float, nullable=True)
    depth_5 = Column(Float, nullable=True)
    depth_6 = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    participants = relationship('Participant', back_populates='status')
    status_bonuses = relationship("StatusBonus", back_populates="status")