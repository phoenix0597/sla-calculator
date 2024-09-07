# schemas.py
# Создание схемы данных (описание Pydantic-моделей) для SQLAlchemy

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class ServiceStatus(str, Enum):
    WORKING = "working"
    NOT_WORKING = "not working"
    UNSTABLE = "unstable"

class ServiceCreate(BaseModel):
    name: str
    description: str

class ServiceStatusHistoryResponse(BaseModel):
    status: ServiceStatus
    timestamp: datetime
    # для создания экземпляров модели из объектов, у которых атрибуты соответствуют полям модели
    model_config = ConfigDict(from_attributes=True)

class ServiceResponse(BaseModel):
    name: str
    description: str
    current_status: ServiceStatus
    model_config = ConfigDict(from_attributes=True)

class ServiceHistoryResponse(BaseModel):
    name: str
    description: str
    history: list[ServiceStatusHistoryResponse]
    model_config = ConfigDict(from_attributes=True)

class SLACalculationResponse(BaseModel):
    total_downtime: float
    sla_percentage: float