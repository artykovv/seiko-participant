
from datetime import datetime
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from config.models_config import Base

# Таблица для участников
class Participant(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'participants'
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    personal_info = Column(String, nullable=True)


    # number хранить код который не видет пользователй
    number = Column(String, nullable=True)

    # personal_number для пользователей видны
    personal_number = Column(String, nullable=True)
    
    # Паспротные данные 
    pin = Column(String, nullable=True)
    passport_id = Column(String, nullable=True)
    passport_issuer = Column(String, nullable=True)
    passport_issue_date = Column(Date, nullable=True)
    bank = Column(String, nullable=True)
    ip_inn = Column(Boolean)
    pensioner = Column(Boolean)
    
    # Для определения кто в струткре а кто не в ней
    register_at = Column(DateTime, nullable=True)
    registered = Column(Boolean, default=False)

    # Внешние ключи
    sponsor_id = Column(BigInteger, ForeignKey('participants.id', ondelete='SET NULL'), nullable=True)
    mentor_id = Column(BigInteger, ForeignKey('participants.id', ondelete='SET NULL'), nullable=True)
    status_id = Column(Integer, ForeignKey('status.id', ondelete='SET NULL'), nullable=True, default=1)
    paket_id = Column(Integer, ForeignKey('pakets.id', ondelete='SET NULL'), nullable=True)
    branch_id = Column(Integer, ForeignKey('branches.id', ondelete='SET NULL'), nullable=True)

    # Бинарная структура
    left_child_id = Column(BigInteger, ForeignKey('participants.id', ondelete='SET NULL'), nullable=True)
    right_child_id = Column(BigInteger, ForeignKey('participants.id', ondelete='SET NULL'), nullable=True)

    # Поля для накопительных объёмов ветвей
    left_volume = Column(BigInteger, default=0)
    right_volume = Column(BigInteger, default=0)
    total_volume = Column(BigInteger, default=0)

    # Колчество пользователей в ветках 
    left_descendants = Column(BigInteger, default=0)
    right_descendants = Column(BigInteger, default=0)

    # Для удобства перемещения вверх по дереву и обновления накопительных объёмов
    parent_id = Column(BigInteger, ForeignKey('participants.id', ondelete='SET NULL'), nullable=True)
    parent = relationship('Participant', remote_side=[id], foreign_keys=[parent_id], backref='children')
    
    # Значения 'left' или 'right'
    branch_side = Column(String, nullable=True) 

    # Поля балансов и бонусов
    balance_total = Column(BigInteger, default=0)
    bonus_turnover = Column(BigInteger, nullable=True, default=0)
    
    bonus_referral = Column(BigInteger, nullable=True, default=0)

    bonus_binar = Column(Float, nullable=True, default=0.0)
    bonus_chek = Column(Float, nullable=True, default=0.0)

    bonus_status = Column(BigInteger, nullable=True, default=0)
    bonus_sponsor = Column(BigInteger, nullable=True, default=0)

    # Дата создания и обновления
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


    # Связи
    sponsor = relationship('Participant', remote_side=[id], foreign_keys=[sponsor_id], backref='sponsored_participants')
    mentor = relationship('Participant', remote_side=[id], foreign_keys=[mentor_id], backref='mentored_participants')
    left_child = relationship('Participant', remote_side=[id], foreign_keys=[left_child_id], backref='left_parent')
    right_child = relationship('Participant', remote_side=[id], foreign_keys=[right_child_id], backref='right_parent')
    
    status = relationship('Status', back_populates='participants')
    paket = relationship('Paket', back_populates='participants')
    branch = relationship('Branch', back_populates='participants')
    status_bonuses = relationship("StatusBonus", back_populates="participant")
    sponsor_bonus = relationship("SponsorBonus", back_populates="participant")


    # Связь с BinaryBonus
    binary_bonuses = relationship('BinaryBonus', back_populates='participant')
    
    # Связь с ChequeBonus
    cheque_bonus = relationship("ChequeBonus", back_populates="participant")

    surprise_bonus = relationship("SurpriseBonus", back_populates="participant")
    tour_bonus = relationship("TourBonus", back_populates="participant")
    auto_bonus = relationship("AutoBonus", back_populates="participant")