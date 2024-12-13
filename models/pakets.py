
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship
from config.models_config import Base

# Таблица для пакетов
class Paket(Base):
    __tablename__ = 'pakets'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)  # Название пакета
    price = Column(Integer, nullable=False)  # Стоимость пакета
    referral_bonus = Column(Integer, nullable=False)  # Реферальный бонус
    binary_bonus_percentage = Column(Float, nullable=False)  # Процент бонуса в бинарной структуре
    color = Column(String, nullable=True)

    participants = relationship('Participant', back_populates='paket')