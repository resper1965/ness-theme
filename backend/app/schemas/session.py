"""
Schemas Pydantic para sessões - Implementação baseada no documento oficial do Agno
Compatível com Agno UI seguindo padrão BMAD
"""

from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class SessionEntry(BaseModel):
    """Entrada de sessão - compatível com frontend"""
    session_id: str
    session_name: str
    created_at: int
    updated_at: Optional[int] = None

class Pagination(BaseModel):
    """Paginação - compatível com frontend"""
    page: int = 1
    limit: int = 10
    total_pages: int = 1
    total_count: int = 0

class Sessions(BaseModel):
    """Lista de sessões - compatível com frontend"""
    data: List[SessionEntry]
    meta: Pagination

class SessionCreate(BaseModel):
    """Dados para criação de sessão"""
    id: str
    name: str
    description: str = ""

class SessionResponse(BaseModel):
    """Resposta de sessão criada"""
    id: str
    name: str
    description: str
    status: str = "active"
    agents_count: int = 0
    orchestrator_count: int = 0

class SessionUpdate(BaseModel):
    """Dados para atualização de sessão"""
    name: Optional[str] = None
    description: Optional[str] = None