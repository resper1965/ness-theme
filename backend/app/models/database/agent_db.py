"""
Modelos de banco de dados para persistência de agentes
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()

class AgentDB(Base):
    """Tabela de agentes no banco de dados"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, default=lambda: f"agent-{uuid.uuid4().hex[:8]}")
    name = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)  # "agent" ou "orchestrator"
    model = Column(String(100), nullable=False)
    status = Column(String(50), default="active")  # "active", "inactive", "archived", "deleted"
    session_id = Column(String, ForeignKey("sessions.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_system = Column(Boolean, default=False)  # Agentes do sistema vs usuário
    metadata = Column(JSON)  # Dados adicionais flexíveis
    
    # Relacionamentos
    session = relationship("SessionDB", back_populates="agents")
    knowledge_sources = relationship("KnowledgeSourceDB", back_populates="agent", cascade="all, delete-orphan")
    metrics = relationship("AgentMetricsDB", back_populates="agent", cascade="all, delete-orphan")

class KnowledgeSourceDB(Base):
    """Tabela de fontes de conhecimento"""
    __tablename__ = "knowledge_sources"
    
    id = Column(String, primary_key=True, default=lambda: f"kb-{uuid.uuid4().hex[:8]}")
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # "rag", "website", "document", "mcp"
    config = Column(JSON)  # Configuração específica da fonte
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    agent = relationship("AgentDB", back_populates="knowledge_sources")

class SessionDB(Base):
    """Tabela de sessões"""
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, default=lambda: f"session-{uuid.uuid4().hex[:8]}")
    name = Column(String(255), nullable=False)
    description = Column(Text)
    max_agents = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(50), default="active")
    metadata = Column(JSON)
    
    # Relacionamentos
    agents = relationship("AgentDB", back_populates="session")

class AgentMetricsDB(Base):
    """Tabela de métricas de agentes"""
    __tablename__ = "agent_metrics"
    
    id = Column(String, primary_key=True, default=lambda: f"metric-{uuid.uuid4().hex[:8]}")
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(JSON)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    agent = relationship("AgentDB", back_populates="metrics")

class AgentTemplateDB(Base):
    """Tabela de templates de agentes"""
    __tablename__ = "agent_templates"
    
    id = Column(String, primary_key=True, default=lambda: f"template-{uuid.uuid4().hex[:8]}")
    name = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    knowledge_sources_config = Column(JSON)  # Configuração padrão das fontes
    capabilities = Column(JSON)  # Lista de capacidades
    is_system = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
