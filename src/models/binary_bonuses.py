from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from config.models_config import Base

# Бинарный бонус пока что предварительный вариант
class BinaryBonus(Base):
    __tablename__ = 'binary_bonuses'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, index=True, nullable=True)
    participant_id = Column(BigInteger, ForeignKey('participants.id', ondelete='CASCADE'), nullable=False)
    # Бонус
    bonus_amount = Column(Float, default=0.0, nullable=False)
    # ТО малой ветки
    small_volume = Column(BigInteger, nullable=False, default=0)
    # ТО больщой ветки
    big_volume = Column(BigInteger, nullable=False, default=0)
    # Остаток от большой ветки
    residual_volume = Column(Float, default=0.0, nullable=False)
    # Большая ветка
    big_branch_side = Column(String, nullable=False)  # 'left' или 'right'
    # Поля для хранения объёмов на момент расчёта
    left_volume_snapshot = Column(BigInteger, nullable=False,)
    right_volume_snapshot = Column(BigInteger, nullable=False,)
    # Поле для указания периода (например, месяц)
    period = Column(String, nullable=False)
    # Когда был создан
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с участником
    participant = relationship('Participant', back_populates='binary_bonuses')