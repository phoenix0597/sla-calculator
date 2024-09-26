# models.py
# Описание моделей данных для SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import enum

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class ServiceStatus(enum.Enum):
    WORKING = "WORKING"
    NOT_WORKING = "NOT_WORKING"
    UNSTABLE = "UNSTABLE"


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    # statuses = relationship('service_status_history', back_populates='service')
    statuses = relationship('ServiceStatusHistory', back_populates='service')

    def __repr__(self):
        return f"<Service(id={self.id}, name={self.name}, description={self.description})>"


class ServiceStatusHistory(Base):
    __tablename__ = 'service_status_history'

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    status = Column(Enum(ServiceStatus), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), default=func.now(), nullable=False)
    # service = relationship('Service', back_populates='status')
    service = relationship('Service', back_populates='statuses')