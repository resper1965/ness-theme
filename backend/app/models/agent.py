"""
Modelos de dados para agentes
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class AgentType(str, Enum):
    """Tipos de agentes disponíveis"""
    AGENT = "agent"
    ORCHESTRATOR = "orchestrator"

class KnowledgeSource(BaseModel):
    """Fonte de conhecimento"""
    id: str
    name: str
    type: str  # "rag", "website", "document", "mcp"
    config: Dict[str, Any]
    status: str = "active"

class Agent(BaseModel):
    """Modelo de agente"""
    id: str
    name: str
    description: str
    type: AgentType
    model: str
    knowledge_sources: List[KnowledgeSource] = []
    session_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "active"
    
    class Config:
        use_enum_values = True

class AgentCreate(BaseModel):
    """Dados para criação de agente"""
    id: str
    name: str
    description: str
    type: AgentType
    model: str
    knowledge_sources: List[KnowledgeSource] = []
    
    class Config:
        use_enum_values = True

class AgentResponse(BaseModel):
    """Resposta de agente"""
    id: str
    name: str
    description: str
    type: AgentType
    model: str
    status: str
    session_id: str
    
    class Config:
        use_enum_values = True
