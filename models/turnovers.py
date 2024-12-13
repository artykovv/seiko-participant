
from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from config.models_config import Base

# Таблица для товарооборота можно добавить или изменить
class Turnover(Base):
    __tablename__ = 'turnovers'
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    branch_id = Column(Integer, index=True, nullable=True)
    participant_id = Column(BigInteger, ForeignKey('participants.id', ondelete='CASCADE'))
    amount = Column(Float)
    transaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    participant = relationship('Participant', backref='turnovers')