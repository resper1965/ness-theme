"""
Modelos de banco de dados para persistência de dados de ingestão
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, ForeignKey, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()

class IngestionRecordDB(Base):
    """Tabela de registros de ingestão"""
    __tablename__ = "ingestion_records"
    
    id = Column(String, primary_key=True, default=lambda: f"ingestion-{uuid.uuid4().hex[:8]}")
    source_type = Column(String(50), nullable=False)  # 'api', 'file', 'web', 'manual'
    source_name = Column(String(255), nullable=False)
    data_type = Column(String(100), nullable=False)  # 'text', 'image', 'document', 'structured'
    file_path = Column(String(500))
    meta_data = Column(JSON)
    status = Column(String(20), default="pending")  # 'pending', 'processing', 'completed', 'failed'
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    error_message = Column(Text)
    user_id = Column(String(255))  # Usuário que iniciou a ingestão
    session_id = Column(String(255))  # Sessão relacionada
    
    # Relacionamentos
    data_content = relationship("DataContentDB", back_populates="ingestion_record", cascade="all, delete-orphan")
    processing_logs = relationship("ProcessingLogDB", back_populates="ingestion_record", cascade="all, delete-orphan")

class DataContentDB(Base):
    """Tabela de conteúdo dos dados ingeridos"""
    __tablename__ = "data_content"
    
    id = Column(String, primary_key=True, default=lambda: f"content-{uuid.uuid4().hex[:8]}")
    ingestion_record_id = Column(String, ForeignKey("ingestion_records.id"), nullable=False)
    content_type = Column(String(100), nullable=False)
    content_data = Column(Text)
    file_path = Column(String(500))
    extracted_text = Column(Text)
    meta_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    size_bytes = Column(Integer)
    checksum = Column(String(64))  # Para verificação de integridade
    
    # Relacionamentos
    ingestion_record = relationship("IngestionRecordDB", back_populates="data_content")

class ProcessingLogDB(Base):
    """Tabela de logs de processamento"""
    __tablename__ = "processing_logs"
    
    id = Column(String, primary_key=True, default=lambda: f"log-{uuid.uuid4().hex[:8]}")
    ingestion_record_id = Column(String, ForeignKey("ingestion_records.id"), nullable=False)
    step_name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)  # 'started', 'completed', 'failed'
    processing_time_ms = Column(Integer)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    error_message = Column(Text)
    
    # Relacionamentos
    ingestion_record = relationship("IngestionRecordDB", back_populates="processing_logs")

class IngestionAnalyticsDB(Base):
    """Tabela de analytics de ingestão"""
    __tablename__ = "ingestion_analytics"
    
    id = Column(String, primary_key=True, default=lambda: f"analytics-{uuid.uuid4().hex[:8]}")
    date = Column(DateTime, nullable=False)
    source_type = Column(String(50), nullable=False)
    total_ingestions = Column(Integer, default=0)
    successful_ingestions = Column(Integer, default=0)
    failed_ingestions = Column(Integer, default=0)
    total_size_bytes = Column(Integer, default=0)
    avg_processing_time_ms = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Índices para performance
    __table_args__ = (
        {'extend_existing': True}
    )

class DataSearchIndexDB(Base):
    """Tabela de índice de busca para dados"""
    __tablename__ = "data_search_index"
    
    id = Column(String, primary_key=True, default=lambda: f"search-{uuid.uuid4().hex[:8]}")
    ingestion_record_id = Column(String, ForeignKey("ingestion_records.id"), nullable=False)
    content_id = Column(String, ForeignKey("data_content.id"), nullable=False)
    searchable_text = Column(Text)  # Texto processado para busca
    keywords = Column(JSON)  # Palavras-chave extraídas
    categories = Column(JSON)  # Categorias automáticas
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    ingestion_record = relationship("IngestionRecordDB")
    content = relationship("DataContentDB")
