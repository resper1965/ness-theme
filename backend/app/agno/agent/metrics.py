"""
Métricas de Agentes
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class AgentMetrics:
    """Métricas de um agente"""
    agent_id: str
    total_interactions: int = 0
    total_tokens_used: int = 0
    average_response_time: float = 0.0
    error_rate: float = 0.0
    last_activity: Optional[datetime] = None
    knowledge_sources_accessed: List[str] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)


@dataclass
class SessionMetrics:
    """Métricas da sessão"""
    session_id: str
    total_messages: int = 0
    total_agents: int = 0
    total_tokens: int = 0
    session_duration: float = 0.0
    errors_count: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    agent_metrics: Dict[str, AgentMetrics] = field(default_factory=dict)
    
    def add_agent_metrics(self, agent_id: str, metrics: AgentMetrics):
        """Adiciona métricas de agente"""
        self.agent_metrics[agent_id] = metrics
        self.total_agents = len(self.agent_metrics)
    
    def update_session_duration(self):
        """Atualiza duração da sessão"""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.session_duration = delta.total_seconds()
        elif self.start_time:
            delta = datetime.now() - self.start_time
            self.session_duration = delta.total_seconds()


class MetricsCollector:
    """Coletor de métricas"""
    
    def __init__(self):
        self._session_metrics: Dict[str, SessionMetrics] = {}
        self._agent_metrics: Dict[str, AgentMetrics] = {}
    
    def start_session(self, session_id: str) -> SessionMetrics:
        """Inicia coleta de métricas para sessão"""
        metrics = SessionMetrics(
            session_id=session_id,
            start_time=datetime.now()
        )
        self._session_metrics[session_id] = metrics
        return metrics
    
    def end_session(self, session_id: str):
        """Finaliza coleta de métricas para sessão"""
        if session_id in self._session_metrics:
            self._session_metrics[session_id].end_time = datetime.now()
            self._session_metrics[session_id].update_session_duration()
    
    def get_session_metrics(self, session_id: str) -> Optional[SessionMetrics]:
        """Retorna métricas da sessão"""
        return self._session_metrics.get(session_id)
    
    def get_agent_metrics(self, agent_id: str) -> Optional[AgentMetrics]:
        """Retorna métricas do agente"""
        return self._agent_metrics.get(agent_id)
    
    def update_agent_metrics(self, agent_id: str, **kwargs):
        """Atualiza métricas do agente"""
        if agent_id not in self._agent_metrics:
            self._agent_metrics[agent_id] = AgentMetrics(agent_id=agent_id)
        
        agent_metrics = self._agent_metrics[agent_id]
        for key, value in kwargs.items():
            if hasattr(agent_metrics, key):
                setattr(agent_metrics, key, value)
        
        agent_metrics.last_activity = datetime.now()
