"""
Serviço de persistência para dados de ingestão
"""

import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, or_, desc, func
from app.models.database.ingestion_db import (
    IngestionRecordDB, DataContentDB, ProcessingLogDB, 
    IngestionAnalyticsDB, DataSearchIndexDB
)
from app.schemas.ingestion import (
    IngestionRecord, DataContent, ProcessingLog, 
    IngestionAnalytics, DataSearchResult
)

logger = logging.getLogger(__name__)

class IngestionPersistenceService:
    """Serviço para persistência de dados de ingestão"""
    
    def __init__(self, db_session: DBSession):
        self.db = db_session
    
    # ===== OPERAÇÕES CRUD BÁSICAS =====
    
    async def create_ingestion_record(self, record_data: Dict[str, Any]) -> IngestionRecord:
        """Cria um novo registro de ingestão"""
        try:
            ingestion_record = IngestionRecordDB(
                source_type=record_data.get("source_type"),
                source_name=record_data.get("source_name"),
                data_type=record_data.get("data_type"),
                file_path=record_data.get("file_path"),
                metadata=record_data.get("metadata", {}),
                status="pending",
                user_id=record_data.get("user_id"),
                session_id=record_data.get("session_id")
            )
            
            self.db.add(ingestion_record)
            self.db.commit()
            self.db.refresh(ingestion_record)
            
            logger.info(f"✅ Registro de ingestão {ingestion_record.id} criado")
            
            return IngestionRecord(
                id=ingestion_record.id,
                source_type=ingestion_record.source_type,
                source_name=ingestion_record.source_name,
                data_type=ingestion_record.data_type,
                file_path=ingestion_record.file_path,
                metadata=ingestion_record.metadata,
                status=ingestion_record.status,
                created_at=ingestion_record.created_at.isoformat(),
                processed_at=ingestion_record.processed_at.isoformat() if ingestion_record.processed_at else None,
                error_message=ingestion_record.error_message,
                user_id=ingestion_record.user_id,
                session_id=ingestion_record.session_id
            )
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Erro ao criar registro de ingestão: {e}")
            raise
    
    async def get_ingestion_record(self, record_id: str) -> Optional[IngestionRecord]:
        """Busca um registro de ingestão por ID"""
        try:
            record_db = self.db.query(IngestionRecordDB).filter(
                IngestionRecordDB.id == record_id
            ).first()
            
            if not record_db:
                return None
            
            return IngestionRecord(
                id=record_db.id,
                source_type=record_db.source_type,
                source_name=record_db.source_name,
                data_type=record_db.data_type,
                file_path=record_db.file_path,
                metadata=record_db.metadata,
                status=record_db.status,
                created_at=record_db.created_at.isoformat(),
                processed_at=record_db.processed_at.isoformat() if record_db.processed_at else None,
                error_message=record_db.error_message,
                user_id=record_db.user_id,
                session_id=record_db.session_id
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar registro de ingestão: {e}")
            raise
    
    async def get_ingestion_records(
        self, 
        user_id: str = None,
        session_id: str = None,
        status: str = None,
        source_type: str = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[IngestionRecord]:
        """Lista registros de ingestão com filtros"""
        try:
            query = self.db.query(IngestionRecordDB)
            
            if user_id:
                query = query.filter(IngestionRecordDB.user_id == user_id)
            if session_id:
                query = query.filter(IngestionRecordDB.session_id == session_id)
            if status:
                query = query.filter(IngestionRecordDB.status == status)
            if source_type:
                query = query.filter(IngestionRecordDB.source_type == source_type)
            
            records_db = query.order_by(desc(IngestionRecordDB.created_at)).limit(limit).offset(offset).all()
            
            return [
                IngestionRecord(
                    id=record.id,
                    source_type=record.source_type,
                    source_name=record.source_name,
                    data_type=record.data_type,
                    file_path=record.file_path,
                    metadata=record.metadata,
                    status=record.status,
                    created_at=record.created_at.isoformat(),
                    processed_at=record.processed_at.isoformat() if record.processed_at else None,
                    error_message=record.error_message,
                    user_id=record.user_id,
                    session_id=record.session_id
                )
                for record in records_db
            ]
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar registros de ingestão: {e}")
            raise
    
    async def update_ingestion_status(
        self, 
        record_id: str, 
        status: str, 
        error_message: str = None
    ) -> bool:
        """Atualiza status de um registro de ingestão"""
        try:
            record_db = self.db.query(IngestionRecordDB).filter(
                IngestionRecordDB.id == record_id
            ).first()
            
            if not record_db:
                return False
            
            record_db.status = status
            if status == "completed":
                record_db.processed_at = datetime.utcnow()
            if error_message:
                record_db.error_message = error_message
            
            self.db.commit()
            
            logger.info(f"✅ Status do registro {record_id} atualizado para {status}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Erro ao atualizar status: {e}")
            raise
    
    # ===== OPERAÇÕES DE CONTEÚDO =====
    
    async def add_data_content(self, content_data: Dict[str, Any]) -> DataContent:
        """Adiciona conteúdo a um registro de ingestão"""
        try:
            content = DataContentDB(
                ingestion_record_id=content_data.get("ingestion_record_id"),
                content_type=content_data.get("content_type"),
                content_data=content_data.get("content_data"),
                file_path=content_data.get("file_path"),
                extracted_text=content_data.get("extracted_text"),
                metadata=content_data.get("metadata", {}),
                size_bytes=content_data.get("size_bytes"),
                checksum=content_data.get("checksum")
            )
            
            self.db.add(content)
            self.db.commit()
            self.db.refresh(content)
            
            logger.info(f"✅ Conteúdo {content.id} adicionado ao registro {content.ingestion_record_id}")
            
            return DataContent(
                id=content.id,
                ingestion_record_id=content.ingestion_record_id,
                content_type=content.content_type,
                content_data=content.content_data,
                file_path=content.file_path,
                extracted_text=content.extracted_text,
                metadata=content.metadata,
                created_at=content.created_at.isoformat(),
                size_bytes=content.size_bytes,
                checksum=content.checksum
            )
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Erro ao adicionar conteúdo: {e}")
            raise
    
    async def get_data_content(self, ingestion_record_id: str) -> List[DataContent]:
        """Busca conteúdo de um registro de ingestão"""
        try:
            contents_db = self.db.query(DataContentDB).filter(
                DataContentDB.ingestion_record_id == ingestion_record_id
            ).all()
            
            return [
                DataContent(
                    id=content.id,
                    ingestion_record_id=content.ingestion_record_id,
                    content_type=content.content_type,
                    content_data=content.content_data,
                    file_path=content.file_path,
                    extracted_text=content.extracted_text,
                    metadata=content.metadata,
                    created_at=content.created_at.isoformat(),
                    size_bytes=content.size_bytes,
                    checksum=content.checksum
                )
                for content in contents_db
            ]
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar conteúdo: {e}")
            raise
    
    # ===== OPERAÇÕES DE LOG =====
    
    async def add_processing_log(self, log_data: Dict[str, Any]) -> ProcessingLog:
        """Adiciona log de processamento"""
        try:
            log = ProcessingLogDB(
                ingestion_record_id=log_data.get("ingestion_record_id"),
                step_name=log_data.get("step_name"),
                status=log_data.get("status"),
                processing_time_ms=log_data.get("processing_time_ms"),
                details=log_data.get("details", {}),
                error_message=log_data.get("error_message")
            )
            
            self.db.add(log)
            self.db.commit()
            self.db.refresh(log)
            
            logger.info(f"✅ Log de processamento {log.id} adicionado")
            
            return ProcessingLog(
                id=log.id,
                ingestion_record_id=log.ingestion_record_id,
                step_name=log.step_name,
                status=log.status,
                processing_time_ms=log.processing_time_ms,
                details=log.details,
                created_at=log.created_at.isoformat(),
                error_message=log.error_message
            )
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Erro ao adicionar log: {e}")
            raise
    
    async def get_processing_logs(self, ingestion_record_id: str) -> List[ProcessingLog]:
        """Busca logs de processamento de um registro"""
        try:
            logs_db = self.db.query(ProcessingLogDB).filter(
                ProcessingLogDB.ingestion_record_id == ingestion_record_id
            ).order_by(ProcessingLogDB.created_at).all()
            
            return [
                ProcessingLog(
                    id=log.id,
                    ingestion_record_id=log.ingestion_record_id,
                    step_name=log.step_name,
                    status=log.status,
                    processing_time_ms=log.processing_time_ms,
                    details=log.details,
                    created_at=log.created_at.isoformat(),
                    error_message=log.error_message
                )
                for log in logs_db
            ]
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar logs: {e}")
            raise
    
    # ===== OPERAÇÕES DE BUSCA =====
    
    async def search_data(
        self, 
        query: str, 
        content_type: str = None,
        source_type: str = None,
        limit: int = 20
    ) -> List[DataSearchResult]:
        """Busca dados por texto"""
        try:
            search_query = self.db.query(DataContentDB).join(IngestionRecordDB)
            
            # Filtro por texto
            search_query = search_query.filter(
                or_(
                    DataContentDB.extracted_text.ilike(f"%{query}%"),
                    DataContentDB.content_data.ilike(f"%{query}%")
                )
            )
            
            # Filtros adicionais
            if content_type:
                search_query = search_query.filter(DataContentDB.content_type == content_type)
            if source_type:
                search_query = search_query.filter(IngestionRecordDB.source_type == source_type)
            
            results_db = search_query.limit(limit).all()
            
            return [
                DataSearchResult(
                    content_id=result.id,
                    ingestion_record_id=result.ingestion_record_id,
                    content_type=result.content_type,
                    extracted_text=result.extracted_text,
                    file_path=result.file_path,
                    metadata=result.metadata,
                    created_at=result.created_at.isoformat()
                )
                for result in results_db
            ]
            
        except Exception as e:
            logger.error(f"❌ Erro na busca: {e}")
            raise
    
    # ===== OPERAÇÕES DE ANALYTICS =====
    
    async def get_ingestion_analytics(
        self, 
        start_date: datetime, 
        end_date: datetime,
        source_type: str = None
    ) -> IngestionAnalytics:
        """Busca analytics de ingestão"""
        try:
            query = self.db.query(IngestionRecordDB).filter(
                and_(
                    IngestionRecordDB.created_at >= start_date,
                    IngestionRecordDB.created_at <= end_date
                )
            )
            
            if source_type:
                query = query.filter(IngestionRecordDB.source_type == source_type)
            
            total_ingestions = query.count()
            successful_ingestions = query.filter(IngestionRecordDB.status == "completed").count()
            failed_ingestions = query.filter(IngestionRecordDB.status == "failed").count()
            
            # Calcular tamanho total
            total_size = self.db.query(func.sum(DataContentDB.size_bytes)).join(
                IngestionRecordDB
            ).filter(
                and_(
                    IngestionRecordDB.created_at >= start_date,
                    IngestionRecordDB.created_at <= end_date
                )
            ).scalar() or 0
            
            # Calcular tempo médio de processamento
            avg_processing_time = self.db.query(func.avg(ProcessingLogDB.processing_time_ms)).join(
                IngestionRecordDB
            ).filter(
                and_(
                    IngestionRecordDB.created_at >= start_date,
                    IngestionRecordDB.created_at <= end_date
                )
            ).scalar() or 0
            
            return IngestionAnalytics(
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                source_type=source_type,
                total_ingestions=total_ingestions,
                successful_ingestions=successful_ingestions,
                failed_ingestions=failed_ingestions,
                total_size_bytes=total_size,
                avg_processing_time_ms=float(avg_processing_time) if avg_processing_time else 0
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar analytics: {e}")
            raise
