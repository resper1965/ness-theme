"""
Schemas Pydantic para agentes - Clone exato do Agno UI
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class AgentType(str, Enum):
    AGENT = "agent"
    ORCHESTRATOR = "orchestrator"

class Model(BaseModel):
    """Modelo de IA usado pelo agente"""
    name: str
    provider: str = "openai"
    api_key: Optional[str] = None

class AgentDetails(BaseModel):
    """Detalhes do agente - compatível com frontend"""
    id: str
    name: Optional[str] = None
    db_id: Optional[str] = None
    model: Optional[Model] = None

class AgentCreate(BaseModel):
    """Dados para criação de agente"""
    id: str
    name: str
    description: str
    type: AgentType
    model: str
    knowledge_sources: List[str] = []

class AgentResponse(BaseModel):
    """Resposta de agente criado"""
    id: str
    name: str
    description: str
    type: AgentType
    model: str
    status: str = "active"
    session_id: Optional[str] = None

class TeamDetails(BaseModel):
    """Detalhes do time - compatível com frontend"""
    id: str
    name: Optional[str] = None
    db_id: Optional[str] = None
    model: Optional[Model] = None

class MessageRequest(BaseModel):
    """Requisição de mensagem"""
    session_id: str
    message: str
    stream: bool = True

class MessageResponse(BaseModel):
    """Resposta de mensagem"""
    message: str
    session_id: str
    agent_id: Optional[str] = None
    agents_involved: List[str] = []

class AgentUpdate(BaseModel):
    """Dados para atualização de agente"""
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None
    knowledge_sources: Optional[List[str]] = None
    status: Optional[str] = None

class AgentTemplate(BaseModel):
    """Template de agente"""
    id: str
    name: str
    description: str
    type: AgentType
    model: str
    knowledge_sources: List[str] = []
    capabilities: List[str] = []
    is_system: bool = False

class AgentHealth(BaseModel):
    """Status de saúde do agente"""
    agent_id: str
    status: str  # "healthy", "warning", "error"
    last_check: str
    metrics: Dict[str, Any] = {}
    issues: List[str] = []

class AgentUpdate(BaseModel):
    """Dados para atualização de agente"""
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None
    knowledge_sources: Optional[List[str]] = None
    status: Optional[str] = None

class AgentClone(BaseModel):
    """Dados para clonagem de agente"""
    source_agent_id: str
    new_name: str
    new_description: Optional[str] = None
    session_id: Optional[str] = None
