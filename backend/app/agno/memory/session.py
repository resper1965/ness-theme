"""
Memória de Sessão
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel

from .memory import MemoryItem


class SessionMemory(BaseModel):
    """Memória específica de uma sessão"""
    
    session_id: str
    agent_id: str
    messages: List[Dict[str, Any]] = []
    context: Dict[str, Any] = {}
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """Adiciona mensagem à sessão"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.messages.append(message)
        self.updated_at = datetime.now()
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna mensagens recentes"""
        return self.messages[-limit:] if self.messages else []
    
    def update_context(self, key: str, value: Any):
        """Atualiza contexto da sessão"""
        self.context[key] = value
        self.updated_at = datetime.now()
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Retorna valor do contexto"""
        return self.context.get(key, default)
    
    def clear_messages(self):
        """Limpa mensagens da sessão"""
        self.messages.clear()
        self.updated_at = datetime.now()
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Retorna resumo da sessão"""
        return {
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "total_messages": len(self.messages),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "context_keys": list(self.context.keys())
        }
