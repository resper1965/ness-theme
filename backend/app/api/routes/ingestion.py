"""
Rotas para persistência de dados de ingestão
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime, timedelta
from app.services.ingestion_persistence_service import IngestionPersistenceService
from app.schemas.ingestion import (
    IngestionRecord, DataContent, ProcessingLog, IngestionAnalytics,
    DataSearchResult, IngestionCreate, IngestionUpdate, DataSearchRequest,
    IngestionStats
)
from sqlalchemy.orm import Session
from app.database.connection import get_database

router = APIRouter()

def get_ingestion_service(db: Session = Depends(get_database)) -> IngestionPersistenceService:
    """Dependency para obter serviço de persistência"""
    return IngestionPersistenceService(db)

# ===== ROTAS DE INGESTÃO =====

@router.post("/", response_model=IngestionRecord)
async def create_ingestion(
    ingestion_data: IngestionCreate,
    service: IngestionPersistenceService = Depends(get_ingestion_service)
):
    """Cria um novo registro de ingestão"""
    try:
        record_data = ingestion_data.dict()
        return await service.create_ingestion_record(record_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar ingestão: {str(e)}")

@router.get("/{record_id}", response_model=IngestionRecord)
async def get_ingestion(
    record_id: str,
    service: IngestionPersistenceService = Depends(get_ingestion_service)
):
    """Busca um registro de ingestão por ID"""
    try:
        record = await service.get_ingestion_record(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar registro: {str(e)}")

@router.get("/", response_model=List[IngestionRecord])
async def list_ingestions(
    user_id: Optional[str] = Query(None),
    session_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    source_type: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    service: IngestionPersistenceService = Depends(get_ingestion_service)
):
    """Lista registros de ingestão com filtros"""
    try:
        return await service.get_ingestion_records(
            user_id=user_id,
            session_id=session_id,
            status=status,
            source_type=source_type,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar registros: {str(e)}")

@router.put("/{record_id}/status")
async def update_ingestion_status(
    record_id: str,
    status_update: IngestionUpdate,
    service: IngestionPersistenceService = Depends(get_ingestion_service)
):
    """Atualiza status de um registro de ingestão"""
    try:
        success = await service.update_ingestion_status(
            record_id=record_id,
            status=status_update.status,
            error_message=status_update.error_message
        )
        if not success:
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        return {"message": "Status atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar status: {str(e)}")

# ===== ROTAS DE CONTEÚDO =====

@router.post("/{record_id}/content", response_model=DataContent)
async def add_content(
    record_id: str,
    content_data: dict,
    service: IngestionPersistenceService = Depends(get_ingestion_service)
):
    """Adiciona conteúdo a um registro de ingestão"""
    try:
        content_data["ingestion_record_id"] = record_id
        return await service.add_data_content(content_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar conteúdo: {str(e)}")

@router.get("/{record_id}/content", response_model=List[DataContent])
async def get_content(
    record_id: str,
    service: IngestionPersistenceService = Depends(get_ingestion_service)
):
    """Busca conteúdo de um registro de ingestão"""
    try:
        return await service.get_data_content(record_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar conteúdo: {str(e)}")

# ===== ROTAS DE LOG =====

@router.post("/{record_id}/logs", response_model=ProcessingLog)
async def add_processing_log(
    record_id: str,
    log_data: dict,
    service: IngestionPersistenceService = Depends(get_ingestion_service)
):
    """Adiciona log de processamento"""
    try:
        log_data["ingestion_record_id"] = record_id
        return await service.add_processing_log(log_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar log: {str(e)}")

@router.get("/{record_id}/logs", response_model=List[ProcessingLog])
async def get_processing_logs(
    record_id: str,
    service: IngestionPersistenceService = Depends(get_ingestion_service)
):
    """Busca logs de processamento"""
    try:
        return await service.get_processing_logs(record_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar logs: {str(e)}")

# ===== ROTAS DE BUSCA =====

@router.post("/search", response_model=List[DataSearchResult])
async def search_data(
    search_request: DataSearchRequest,
    service: IngestionPersistenceService = Depends(get_ingestion_service)
):
    """Busca dados por texto"""
    try:
        return await service.search_data(
            query=search_request.query,
            content_type=search_request.content_type,
            source_type=search_request.source_type,
            limit=search_request.limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")

# ===== ROTAS DE ANALYTICS =====

@router.get("/analytics/stats", response_model=IngestionStats)
async def get_ingestion_stats(
    days: int = Query(30, ge=1, le=365),
    service: IngestionPersistenceService = Depends(get_ingestion_service)
):
    """Busca estatísticas de ingestão"""
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Buscar registros do período
        records = await service.get_ingestion_records(
            limit=1000  # Limite para analytics
        )
        
        # Filtrar por período
        filtered_records = [
            r for r in records 
            if datetime.fromisoformat(r.created_at.replace('Z', '+00:00')) >= start_date
        ]
        
        total_records = len(filtered_records)
        pending_records = len([r for r in filtered_records if r.status == "pending"])
        processing_records = len([r for r in filtered_records if r.status == "processing"])
        completed_records = len([r for r in filtered_records if r.status == "completed"])
        failed_records = len([r for r in filtered_records if r.status == "failed"])
        
        return IngestionStats(
            total_records=total_records,
            pending_records=pending_records,
            processing_records=processing_records,
            completed_records=completed_records,
            failed_records=failed_records,
            total_size_bytes=0,  # Implementar cálculo de tamanho
            avg_processing_time_ms=0.0  # Implementar cálculo de tempo
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar estatísticas: {str(e)}")

@router.get("/analytics/period", response_model=IngestionAnalytics)
async def get_analytics_period(
    start_date: str,
    end_date: str,
    source_type: Optional[str] = Query(None),
    service: IngestionPersistenceService = Depends(get_ingestion_service)
):
    """Busca analytics de um período específico"""
    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        
        return await service.get_ingestion_analytics(
            start_date=start_dt,
            end_date=end_dt,
            source_type=source_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar analytics: {str(e)}")
