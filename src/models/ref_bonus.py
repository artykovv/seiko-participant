from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.models_config import Base

# Таблица для реферального бонуса
class RefBonus(Base):
    __tablename__ = 'ref_bonus'
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    branch_id = Column(BigInteger, index=True, nullable=True)
    from_participant_id = Column(BigInteger, ForeignKey('participants.id'), nullable=False)  # ID спонсора
    participant_id = Column(BigInteger, ForeignKey('participants.id'), nullable=False)  # ID нового участника
    amount = Column(BigInteger, nullable=False)  # Сумма бонуса
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания транзакции

    from_participant = relationship('Participant', foreign_keys=[from_participant_id])  # Связь со спонсором
    participant = relationship('Participant', foreign_keys=[participant_id])  # Связь с новым участником