from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from config.models_config import Base




class ChequeBonus(Base):
    __tablename__ = 'cheque_bonus'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, index=True, nullable=True)
    participant_id = Column(BigInteger, ForeignKey('participants.id', ondelete='CASCADE'), nullable=False)
    # Бонус
    bonus_amount = Column(Float, default=0.0, nullable=False)
    from_id = Column(BigInteger, nullable=False)
    depth = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с участником
    participant = relationship('Participant', back_populates='cheque_bonus')