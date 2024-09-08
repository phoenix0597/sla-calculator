from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from dependency import get_db
from schemas import (
    ServiceResponseSchema, ServiceCreateSchema, ServiceStatusHistoryResponseSchema,
    SLACalculationResponseSchema, ServiceHistoryResponseSchema, ServiceStatusSchema
)
from models import Service, ServiceStatusHistory, ServiceStatus

router = APIRouter(
    prefix="/services",
    tags=["Сервисы"],
)


@router.post("/", summary="Создание сервиса", response_model=ServiceResponseSchema)
async def create_service(service: ServiceCreateSchema, db: AsyncSession = Depends(get_db)):
    db_service = Service(name=service.name, description=service.description)
    db.add(db_service)
    await db.commit()
    await db.refresh(db_service)

    return db_service


@router.post(
    "/{service_name}/status",
    summary="Изменение статуса сервиса",
    response_model=ServiceStatusHistoryResponseSchema
)
async def update_service_status(
        service_name: str,
        # status: ServiceStatusSchema,
        status: ServiceStatusSchema = Query(...),
        db: AsyncSession = Depends(get_db)
):
    query = select(Service).filter(Service.name == service_name)
    result = await db.execute(query)
    db_service = result.scalars().first()

    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    status_entry = ServiceStatusHistory(service_id=db_service.id, status=status)
    db.add(status_entry)
    await db.commit()
    await db.refresh(status_entry)

    return status_entry


@router.get("/services/", response_model=list[ServiceResponseSchema])
async def list_services(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).options(joinedload(Service.statuses)))
    services = result.unique().scalars().all()
    response = []
    for service in services:
        last_status = await db.execute(
            select(ServiceStatusHistory)
            .filter_by(service_id=service.id)
            .order_by(ServiceStatusHistory.timestamp.desc())
        )
        last_status = last_status.scalars().first()
        response.append(ServiceResponseSchema(name=service.name, description=service.description,
                                                current_status=last_status.status))
    return response


@router.get("/services/{service_name}/history", response_model=ServiceHistoryResponseSchema)
async def get_service_history(service_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Service).filter(Service.name == service_name).options(joinedload(Service.statuses)))
    db_service = result.scalars().first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    history = await db.execute(
        select(ServiceStatusHistory).filter_by(service_id=db_service.id).order_by(
            ServiceStatusHistory.timestamp)
    )
    history = history.scalars().all()
    return ServiceHistoryResponseSchema(name=db_service.name, description=db_service.description, history=history)


@router.get("/services/{service_name}/sla", response_model=SLACalculationResponseSchema)
async def calculate_sla(service_name: str, start_date: datetime, end_date: datetime,
                        db: AsyncSession = Depends(get_db)):

    # Приведение start_date и end_date к naive datetime
    start_date = make_naive(start_date)
    end_date = make_naive(end_date)

    result = await db.execute(select(Service).filter(Service.name == service_name))
    db_service = result.scalars().first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    history = await db.execute(
        select(ServiceStatusHistory)
        .filter(
            ServiceStatusHistory.service_id == db_service.id,
            ServiceStatusHistory.timestamp >= start_date,
            ServiceStatusHistory.timestamp <= end_date
        )
        .order_by(ServiceStatusHistory.timestamp)
    )
    history = history.scalars().all()

    total_time = (end_date - start_date).total_seconds()
    downtime = 0
    # last_status = None
    last_timestamp = start_date

    # If there's no history, assume the service was working for the entire period
    if not history:
        last_status = ServiceStatus.WORKING
    else:
        # Установим начальное состояние и временную метку на начало периода
        last_status = ServiceStatus.WORKING  # Предположим, что сервис рабочий в начале
        last_timestamp = start_date

    for entry in history:
        # Приведение entry.timestamp к naive datetime
        entry_timestamp_naive = make_naive(entry.timestamp)

        # Добавляем время простоя, если предыдущий статус был NOT_WORKING
        # if last_status == ServiceStatusSchema.NOT_WORKING:
        if last_status == ServiceStatus.NOT_WORKING:
            downtime += (entry_timestamp_naive - last_timestamp).total_seconds()

        # Обновляем статус и временную метку
        last_status = entry.status
        last_timestamp = entry_timestamp_naive

    # Check if the last status was NOT_WORKING and add the remaining time to downtime
    if last_status == ServiceStatus.NOT_WORKING:
        downtime += (end_date - last_timestamp).total_seconds()

    # Если первый статус в истории был NOT_WORKING, нужно учесть это время
    if history and history[0].status == ServiceStatus.NOT_WORKING:
        downtime += (make_naive(history[0].timestamp) - start_date).total_seconds()

    sla_percentage = ((total_time - downtime) / total_time) * 100
    return SLACalculationResponseSchema(
        total_time=total_time,
        total_downtime=downtime,
        sla_percentage=round(sla_percentage, 3)
    )


def make_naive(dt: datetime) -> datetime:
    """Приводит datetime к naive (без временной зоны), если он имеет временную зону."""
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt