"""
Modelos de dados para sessões
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.agent import Agent

class Session(BaseModel):
    """Modelo de sessão de chat"""
    id: str
    name: str
    description: str
    max_agents: int = 3
    max_orchestrator: int = 1
    agent_ids: List[str] = []
    orchestrator_ids: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "active"
    
    @property
    def agents_count(self) -> int:
        """Conta agentes regulares"""
        return len([aid for aid in self.agent_ids if aid not in self.orchestrator_ids])
    
    @property
    def orchestrator_count(self) -> int:
        """Conta orquestradores"""
        return len(self.orchestrator_ids)
    
    def add_agent(self, agent: Agent) -> bool:
        """Adiciona agente à sessão"""
        if agent.id not in self.agent_ids:
            self.agent_ids.append(agent.id)
            
            if agent.type == "orchestrator":
                if agent.id not in self.orchestrator_ids:
                    self.orchestrator_ids.append(agent.id)
            
            return True
        return False
    
    def remove_agent(self, agent_id: str) -> bool:
        """Remove agente da sessão"""
        if agent_id in self.agent_ids:
            self.agent_ids.remove(agent_id)
            
            if agent_id in self.orchestrator_ids:
                self.orchestrator_ids.remove(agent_id)
            
            return True
        return False

class SessionCreate(BaseModel):
    """Dados para criação de sessão"""
    id: str
    name: str
    description: str

class SessionResponse(BaseModel):
    """Resposta de sessão"""
    id: str
    name: str
    description: str
    status: str
    agents_count: int
    orchestrator_count: int
