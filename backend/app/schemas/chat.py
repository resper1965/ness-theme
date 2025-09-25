"""
Schemas para chat funcional
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ChatMessageRequest(BaseModel):
    """Request para enviar mensagem"""
    message: str
    session_id: str = "default-session"
    agent_id: Optional[str] = None

class ChatMessageResponse(BaseModel):
    """Response de mensagem do chat"""
    id: str
    content: str
    agent_id: str
    session_id: str
    timestamp: datetime
    metadata: Dict[str, Any] = {}

class ChatSessionStatus(BaseModel):
    """Status da sessão de chat"""
    session_id: str
    status: str
    agents_count: int
    orchestrator_available: bool
    agno_sdk_available: bool

class ChatSessionStart(BaseModel):
    """Iniciar sessão de chat"""
    session_id: str
    status: str
    agents_count: int
    message: str
