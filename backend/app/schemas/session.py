"""
Schemas Pydantic para sessões
"""

from typing import List, Optional
from pydantic import BaseModel

class SessionCreate(BaseModel):
    """Schema para criação de sessão"""
    id: str
    name: str
    description: str

class SessionResponse(BaseModel):
    """Schema de resposta de sessão"""
    id: str
    name: str
    description: str
    status: str
    agents_count: int
    orchestrator_count: int

class SessionUpdate(BaseModel):
    """Schema para atualização de sessão"""
    name: Optional[str] = None
    description: Optional[str] = None

class MessageRequest(BaseModel):
    """Schema para envio de mensagem"""
    message: str
    session_id: str

class MessageResponse(BaseModel):
    """Schema de resposta de mensagem"""
    message: str
    session_id: str
    orchestrator_id: str
    agents_involved: List[str]
