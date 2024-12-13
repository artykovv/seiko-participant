from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from config.models_config import Base

# Таблица для снятия наличных 
class СashRefBonus(Base):
    __tablename__ = 'cashrefbonus'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    branch_id = Column(Integer, index=True, nullable=True)
    participant_id = Column(BigInteger, ForeignKey('participants.id', ondelete='CASCADE'))
    amount = Column(BigInteger, nullable=False)
    transaction_type = Column(String, nullable=False)  # Например, "withdrawal", "deposit" и т.д.
    bonus_type = Column(String, nullable=False)  # Например, "bonus_referral"
    created_at = Column(DateTime, default=datetime.utcnow)

    participant = relationship('Participant', backref='transactions')