# schemas.py
# Создание схемы данных (описание Pydantic-моделей) для SQLAlchemy
from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

# class ServiceStatus(str, Enum):
class ServiceStatusSchema(str, Enum):
    WORKING = "WORKING"
    NOT_WORKING = "NOT_WORKING"
    UNSTABLE = "UNSTABLE"

class ServiceCreateSchema(BaseModel):
    name: str
    description: str

class ServiceStatusHistoryResponseSchema(BaseModel):
    status: ServiceStatusSchema
    timestamp: datetime
    # для создания экземпляров модели из объектов, у которых атрибуты соответствуют полям модели
    model_config = ConfigDict(from_attributes=True)

class ServiceStatusCreateSchema(BaseModel):
    status: ServiceStatusSchema

class ServiceResponseSchema(BaseModel):
    name: str
    description: str
    # current_status: ServiceStatus
    current_status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ServiceHistoryResponseSchema(BaseModel):
    name: str
    description: str
    history: list[ServiceStatusHistoryResponseSchema]
    model_config = ConfigDict(from_attributes=True)

class SLACalculationResponseSchema(BaseModel):
    total_time: float
    total_downtime: float
    sla_percentage: float