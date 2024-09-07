# models.py
# Описание моделей данных для SQLAlchemy
from datetime import datetime
from time import timezone

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
import enum

from sqlalchemy.orm import relationship

Base = declarative_base()

class ServiceStatus(enum):
    WORKING = "working"
    NOT_WORKING = "not working"
    UNSTABLE = "unstable"


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    statuses = relationship('service_status_history', back_populates='service')

    def __repr__(self):
        return f"<Service(id={self.id}, name={self.name}, description={self.description}, statuses={self.statuses})>"


class ServiceStatusHistory(Base):
    __tablename__ = 'service_status_history'

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    status = Column(Enum(ServiceStatus), nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone = timezone.utc), nullable=False)
    service = relationship('Service', back_populates='status')