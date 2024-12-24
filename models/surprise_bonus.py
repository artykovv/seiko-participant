
from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from config.models_config import Base


class SurpriseBonus(Base):
    __tablename__ = 'surprise_bonus'
    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(BigInteger, ForeignKey('participants.id', ondelete='CASCADE'), nullable=False)
    
     # Поля для хранения объёмов на момент расчёта
    left_volume_snapshot = Column(BigInteger, nullable=False,)
    right_volume_snapshot = Column(BigInteger, nullable=False,)

    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания транзакции

    participant = relationship('Participant', back_populates='surprise_bonus')