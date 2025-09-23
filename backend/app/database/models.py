"""
Modelos de banco de dados SQLAlchemy
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class SessionDB(Base):
    """Tabela de sessões"""
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    max_agents = Column(Integer, default=3)
    max_orchestrator = Column(Integer, default=1)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    agents = relationship("AgentDB", back_populates="session", cascade="all, delete-orphan")
    messages = relationship("MessageDB", back_populates="session", cascade="all, delete-orphan")

class AgentDB(Base):
    """Tabela de agentes"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String, nullable=False)  # "agent" ou "orchestrator"
    model = Column(String, nullable=False)
    status = Column(String, default="active")
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    session = relationship("SessionDB", back_populates="agents")
    knowledge_sources = relationship("KnowledgeSourceDB", back_populates="agent", cascade="all, delete-orphan")

class KnowledgeSourceDB(Base):
    """Tabela de fontes de conhecimento"""
    __tablename__ = "knowledge_sources"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "rag", "website", "document", "mcp"
    config = Column(JSON)
    status = Column(String, default="active")
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    agent = relationship("AgentDB", back_populates="knowledge_sources")

class MessageDB(Base):
    """Tabela de mensagens"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    role = Column(String, nullable=False)  # "user", "agent", "system"
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    agent_id = Column(String, nullable=True)  # ID do agente que respondeu
    message_metadata = Column(JSON)  # Metadados adicionais
    created_at = Column(DateTime, default=func.now())
    
    # Relacionamentos
    session = relationship("SessionDB", back_populates="messages")

class UserDB(Base):
    """Tabela de usuários (para futuras funcionalidades)"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
