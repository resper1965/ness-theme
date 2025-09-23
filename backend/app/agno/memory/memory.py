"""
Sistema de Memória para Agentes
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class MemoryItem(BaseModel):
    """Item de memória"""
    id: str
    agent_id: str
    session_id: str
    content: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime
    importance: float = 0.5  # 0.0 a 1.0


class Memory(BaseModel, ABC):
    """Classe base para sistema de memória"""
    
    @abstractmethod
    async def save_interaction(
        self,
        agent_id: str,
        user_message: str,
        agent_response: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Salva interação na memória"""
        pass
    
    @abstractmethod
    async def search(
        self,
        query: str,
        agent_id: Optional[str] = None,
        limit: int = 10
    ) -> List[MemoryItem]:
        """Busca na memória"""
        pass
    
    @abstractmethod
    async def get_session_memory(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[MemoryItem]:
        """Retorna memória da sessão"""
        pass
    
    @abstractmethod
    async def clear_session_memory(self, session_id: str):
        """Limpa memória da sessão"""
        pass


class InMemoryStorage(Memory):
    """Armazenamento em memória (para desenvolvimento)"""
    
    def __init__(self):
        self._storage: List[MemoryItem] = []
    
    async def save_interaction(
        self,
        agent_id: str,
        user_message: str,
        agent_response: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Salva interação na memória"""
        from uuid import uuid4
        
        # Criar item de memória
        memory_item = MemoryItem(
            id=str(uuid4()),
            agent_id=agent_id,
            session_id=metadata.get("session_id", "default"),
            content=f"User: {user_message}\nAgent: {agent_response}",
            metadata=metadata,
            timestamp=datetime.now(),
            importance=0.7
        )
        
        self._storage.append(memory_item)
        return memory_item.id
    
    async def search(
        self,
        query: str,
        agent_id: Optional[str] = None,
        limit: int = 10
    ) -> List[MemoryItem]:
        """Busca na memória"""
        results = []
        
        for item in self._storage:
            if agent_id and item.agent_id != agent_id:
                continue
            
            if query.lower() in item.content.lower():
                results.append(item)
        
        # Ordenar por importância e timestamp
        results.sort(key=lambda x: (x.importance, x.timestamp), reverse=True)
        return results[:limit]
    
    async def get_session_memory(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[MemoryItem]:
        """Retorna memória da sessão"""
        session_memories = [
            item for item in self._storage 
            if item.session_id == session_id
        ]
        
        # Ordenar por timestamp
        session_memories.sort(key=lambda x: x.timestamp, reverse=True)
        return session_memories[:limit]
    
    async def clear_session_memory(self, session_id: str):
        """Limpa memória da sessão"""
        self._storage = [
            item for item in self._storage 
            if item.session_id != session_id
        ]
