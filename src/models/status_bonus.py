
from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from config.models_config import Base

class StatusBonus(Base):
    __tablename__ = 'status_bonuses'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, index=True, nullable=True)
    participant_id = Column(BigInteger, ForeignKey('participants.id', ondelete='CASCADE'), nullable=False)
    status_id = Column(Integer, ForeignKey('status.id', ondelete='CASCADE'), nullable=False)
    bonus = Column(BigInteger, nullable=False)
    
    # Поля для хранения объёмов на момент расчёта
    left_volume_snapshot = Column(BigInteger, nullable=False,)
    right_volume_snapshot = Column(BigInteger, nullable=False,)

    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания транзакции

    participant = relationship('Participant', back_populates='status_bonuses')
    status = relationship('Status', back_populates='status_bonuses')