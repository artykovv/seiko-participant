
from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from config.models_config import Base

class SponsorBonus(Base):
    __tablename__ = 'sponsor_bonus'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, index=True, nullable=True)
    participant_id = Column(BigInteger, ForeignKey('participants.id', ondelete='CASCADE'), nullable=False)
    sponsored = Column(BigInteger, nullable=False)
    bonus = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания транзакции
    participant = relationship('Participant', back_populates='sponsor_bonus')