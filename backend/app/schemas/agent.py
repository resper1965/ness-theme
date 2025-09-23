"""
Schemas Pydantic para agentes
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.agent import AgentType, KnowledgeSource

class KnowledgeSourceCreate(BaseModel):
    """Schema para criação de fonte de conhecimento"""
    id: str
    name: str
    type: str
    config: Dict[str, Any]

class AgentCreate(BaseModel):
    """Schema para criação de agente"""
    id: str
    name: str
    description: str
    type: AgentType
    model: str
    knowledge_sources: List[KnowledgeSourceCreate] = []
    
    class Config:
        use_enum_values = True

class AgentResponse(BaseModel):
    """Schema de resposta de agente"""
    id: str
    name: str
    description: str
    type: AgentType
    model: str
    status: str
    session_id: str
    
    class Config:
        use_enum_values = True

class AgentUpdate(BaseModel):
    """Schema para atualização de agente"""
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None
    knowledge_sources: Optional[List[KnowledgeSourceCreate]] = None
