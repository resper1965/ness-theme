"""
Classe Agent baseada no Agno SDK
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4
from pydantic import BaseModel

from ..constants import *
from ..exceptions import *
from ..models import Model
from ..memory import Memory
from ..knowledge import KnowledgeBase


class AgentConfig(BaseModel):
    """Configuração do agente"""
    name: str
    description: str
    model: str
    knowledge_sources: List[str] = []
    tools: List[str] = []
    memory_enabled: bool = True
    max_iterations: int = 10
    temperature: float = 0.7
    max_tokens: Optional[int] = None


class AgentMessage(BaseModel):
    """Mensagem do agente"""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = {}


class AgentResponse(BaseModel):
    """Resposta do agente"""
    content: str
    metadata: Dict[str, Any] = {}
    citations: List[str] = []
    tools_used: List[str] = []


@dataclass
class SessionMetrics:
    """Métricas da sessão"""
    total_messages: int = 0
    total_tokens: int = 0
    execution_time: float = 0.0
    errors_count: int = 0


class Agent:
    """
    Agente baseado no Agno SDK
    """
    
    def __init__(
        self,
        config: AgentConfig,
        model: Model,
        memory: Optional[Memory] = None,
        knowledge_base: Optional[KnowledgeBase] = None
    ):
        self.id = str(uuid4())
        self.config = config
        self.model = model
        self.memory = memory
        self.knowledge_base = knowledge_base
        self.session_metrics = SessionMetrics()
        self._conversation_history: List[AgentMessage] = []
        
    async def process_message(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Processa uma mensagem e retorna resposta do agente
        """
        try:
            # Adicionar mensagem do usuário ao histórico
            user_message = AgentMessage(
                role="user",
                content=message,
                timestamp=self._get_timestamp()
            )
            self._conversation_history.append(user_message)
            
            # Buscar conhecimento relevante se disponível
            relevant_knowledge = []
            if self.knowledge_base:
                relevant_knowledge = await self.knowledge_base.search(message)
            
            # Preparar contexto para o modelo
            model_context = self._prepare_model_context(
                message, 
                relevant_knowledge, 
                context
            )
            
            # Gerar resposta usando o modelo
            response_content = await self.model.generate_response(model_context)
            
            # Criar resposta do agente
            response = AgentResponse(
                content=response_content,
                metadata={
                    "agent_id": self.id,
                    "model": self.config.model,
                    "knowledge_sources_used": len(relevant_knowledge),
                    "timestamp": self._get_timestamp()
                },
                citations=[kb.get("source", "") for kb in relevant_knowledge]
            )
            
            # Adicionar resposta ao histórico
            assistant_message = AgentMessage(
                role="assistant",
                content=response_content,
                timestamp=self._get_timestamp(),
                metadata=response.metadata
            )
            self._conversation_history.append(assistant_message)
            
            # Salvar no memory se disponível
            if self.memory:
                await self.memory.save_interaction(
                    self.id,
                    message,
                    response_content,
                    response.metadata
                )
            
            # Atualizar métricas
            self.session_metrics.total_messages += 1
            
            return response
            
        except Exception as e:
            self.session_metrics.errors_count += 1
            raise AgentError(f"Erro ao processar mensagem: {str(e)}")
    
    def _prepare_model_context(
        self,
        message: str,
        knowledge: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Prepara contexto para o modelo"""
        return {
            "message": message,
            "knowledge": knowledge,
            "conversation_history": [
                {"role": msg.role, "content": msg.content} 
                for msg in self._conversation_history[-10:]  # Últimas 10 mensagens
            ],
            "agent_config": self.config.dict(),
            "context": context or {}
        }
    
    def _get_timestamp(self) -> str:
        """Retorna timestamp atual"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_conversation_history(self) -> List[AgentMessage]:
        """Retorna histórico da conversa"""
        return self._conversation_history.copy()
    
    def clear_history(self):
        """Limpa histórico da conversa"""
        self._conversation_history.clear()
    
    def get_metrics(self) -> SessionMetrics:
        """Retorna métricas da sessão"""
        return self.session_metrics
