"""
Schemas para dados de ingestão
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from datetime import datetime

class IngestionRecord(BaseModel):
    """Registro de ingestão"""
    id: str
    source_type: str  # 'api', 'file', 'web', 'manual'
    source_name: str
    data_type: str  # 'text', 'image', 'document', 'structured'
    file_path: Optional[str] = None
    metadata: Dict[str, Any] = {}
    status: str  # 'pending', 'processing', 'completed', 'failed'
    created_at: str
    processed_at: Optional[str] = None
    error_message: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class DataContent(BaseModel):
    """Conteúdo dos dados ingeridos"""
    id: str
    ingestion_record_id: str
    content_type: str
    content_data: Optional[str] = None
    file_path: Optional[str] = None
    extracted_text: Optional[str] = None
    metadata: Dict[str, Any] = {}
    created_at: str
    size_bytes: Optional[int] = None
    checksum: Optional[str] = None

class ProcessingLog(BaseModel):
    """Log de processamento"""
    id: str
    ingestion_record_id: str
    step_name: str
    status: str  # 'started', 'completed', 'failed'
    processing_time_ms: Optional[int] = None
    details: Dict[str, Any] = {}
    created_at: str
    error_message: Optional[str] = None

class IngestionAnalytics(BaseModel):
    """Analytics de ingestão"""
    start_date: str
    end_date: str
    source_type: Optional[str] = None
    total_ingestions: int
    successful_ingestions: int
    failed_ingestions: int
    total_size_bytes: int
    avg_processing_time_ms: float

class DataSearchResult(BaseModel):
    """Resultado de busca de dados"""
    content_id: str
    ingestion_record_id: str
    content_type: str
    extracted_text: Optional[str] = None
    file_path: Optional[str] = None
    metadata: Dict[str, Any] = {}
    created_at: str

class IngestionCreate(BaseModel):
    """Dados para criação de ingestão"""
    source_type: str
    source_name: str
    data_type: str
    file_path: Optional[str] = None
    metadata: Dict[str, Any] = {}
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class IngestionUpdate(BaseModel):
    """Dados para atualização de ingestão"""
    status: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class DataSearchRequest(BaseModel):
    """Requisição de busca"""
    query: str
    content_type: Optional[str] = None
    source_type: Optional[str] = None
    limit: int = 20
    offset: int = 0

class IngestionStats(BaseModel):
    """Estatísticas de ingestão"""
    total_records: int
    pending_records: int
    processing_records: int
    completed_records: int
    failed_records: int
    total_size_bytes: int
    avg_processing_time_ms: float
