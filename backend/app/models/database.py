"""
Modelos SQLAlchemy para banco de dados
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base

class User(Base):
    """Usuário do sistema"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relacionamentos
    sessions = relationship("Session", back_populates="user")

class Session(Base):
    """Sessão de chat"""
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relacionamentos
    user = relationship("User", back_populates="sessions")
    agents = relationship("Agent", back_populates="session")
    messages = relationship("Message", back_populates="session")

class Agent(Base):
    """Agente criado dinamicamente"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String, nullable=False)  # "agent" ou "orchestrator"
    model = Column(String, nullable=False)
    knowledge_sources = Column(JSON, default=list)
    config = Column(JSON, default=dict)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    session = relationship("Session", back_populates="agents")
    messages = relationship("Message", back_populates="agent")

class Message(Base):
    """Mensagem do chat"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=True)
    role = Column(String, nullable=False)  # "user", "assistant", "system"
    content = Column(Text, nullable=False)
    message_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    session = relationship("Session", back_populates="messages")
    agent = relationship("Agent", back_populates="messages")

class KnowledgeSource(Base):
    """Fonte de conhecimento"""
    __tablename__ = "knowledge_sources"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "rag", "website", "document", "mcp"
    config = Column(JSON, default=dict)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
