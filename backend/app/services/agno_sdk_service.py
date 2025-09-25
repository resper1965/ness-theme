"""
Serviço de integração real com Agno SDK
Implementação baseada no documento oficial do Agno
"""

import logging
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime
from app.config.settings import get_settings
from app.schemas.agent import AgentCreate, AgentResponse, AgentDetails, MessageRequest, MessageResponse
from app.schemas.session import SessionCreate, SessionResponse, SessionEntry, Sessions

logger = logging.getLogger(__name__)

class AgnoSDKService:
    """Serviço real de integração com Agno SDK"""
    
    def __init__(self):
        self.settings = get_settings()
        self.active_sessions: Dict[str, Any] = {}
        self.active_agents: Dict[str, Any] = {}
        self._agno_client = None
        self._initialize_agno_sdk()
    
    def _initialize_agno_sdk(self):
        """Inicializa o Agno SDK real"""
        try:
            # Importar Agno SDK
            from agno import Agno
            from agno.models import OpenAIChat
            from agno.knowledge import KnowledgeBase
            from agno.agent import Agent as AgnoAgent
            
            # Configurar modelo OpenAI
            model = OpenAIChat(
                model="gpt-4",
                api_key=self.settings.OPENAI_API_KEY
            )
            
            # Inicializar Agno
            self._agno_client = Agno(
                model=model,
                api_key=self.settings.AGNO_API_KEY
            )
            
            logger.info("✅ Agno SDK inicializado com sucesso")
            
        except ImportError as e:
            logger.error(f"❌ Erro ao importar Agno SDK: {e}")
            logger.info("💡 Instale o Agno SDK: pip install agno")
            self._agno_client = None
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Agno SDK: {e}")
            self._agno_client = None
    
    async def create_agent(self, agent_data: AgentCreate) -> AgentResponse:
        """Cria um agente usando Agno SDK real"""
        try:
            if not self._agno_client:
                raise Exception("Agno SDK não inicializado")
            
            # Criar agente com Agno SDK
            agno_agent = self._agno_client.create_agent(
                name=agent_data.name,
                description=agent_data.description,
                model=agent_data.model,
                knowledge_sources=agent_data.knowledge_sources or []
            )
            
            # Armazenar agente
            agent_id = str(agno_agent.id)
            self.active_agents[agent_id] = agno_agent
            
            return AgentResponse(
                id=agent_id,
                name=agno_agent.name,
                description=agno_agent.description,
                model=agno_agent.model,
                status="active",
                created_at=datetime.now(),
                knowledge_sources=agno_agent.knowledge_sources
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar agente: {e}")
            raise Exception(f"Erro ao criar agente: {str(e)}")
    
    async def send_message(self, message_data: MessageRequest) -> MessageResponse:
        """Envia mensagem usando Agno SDK real"""
        try:
            if not self._agno_client:
                raise Exception("Agno SDK não inicializado")
            
            # Enviar mensagem com Agno SDK
            response = await self._agno_client.send_message(
                agent_id=message_data.agent_id,
                message=message_data.message,
                session_id=message_data.session_id
            )
            
            return MessageResponse(
                id=str(uuid.uuid4()),
                content=response.content,
                agent_id=message_data.agent_id,
                session_id=message_data.session_id,
                timestamp=datetime.now(),
                metadata=response.metadata or {}
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar mensagem: {e}")
            raise Exception(f"Erro ao enviar mensagem: {str(e)}")
    
    async def create_session(self, session_data: SessionCreate) -> SessionResponse:
        """Cria uma sessão usando Agno SDK real"""
        try:
            if not self._agno_client:
                raise Exception("Agno SDK não inicializado")
            
            # Criar sessão com Agno SDK
            agno_session = await self._agno_client.create_session(
                name=session_data.name,
                description=session_data.description,
                max_agents=session_data.max_agents
            )
            
            # Armazenar sessão
            session_id = str(agno_session.id)
            self.active_sessions[session_id] = agno_session
            
            return SessionResponse(
                id=session_id,
                name=agno_session.name,
                description=agno_session.description,
                status="active",
                agents_count=len(agno_session.agents),
                orchestrator_count=1 if agno_session.orchestrator else 0
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar sessão: {e}")
            raise Exception(f"Erro ao criar sessão: {str(e)}")
    
    def get_agents(self) -> List[AgentResponse]:
        """Retorna lista de agentes ativos"""
        agents = []
        for agent_id, agno_agent in self.active_agents.items():
            agents.append(AgentResponse(
                id=agent_id,
                name=agno_agent.name,
                description=agno_agent.description,
                model=agno_agent.model,
                status="active",
                created_at=datetime.now(),
                knowledge_sources=agno_agent.knowledge_sources
            ))
        return agents
    
    def get_sessions(self) -> Sessions:
        """Retorna lista de sessões ativas"""
        sessions = []
        for session_id, agno_session in self.active_sessions.items():
            sessions.append(SessionEntry(
                id=session_id,
                name=agno_session.name,
                description=agno_session.description,
                status="active",
                agents_count=len(agno_session.agents),
                orchestrator_count=1 if agno_session.orchestrator else 0,
                created_at=datetime.now()
            ))
        
        return Sessions(
            data=sessions,
            total=len(sessions),
            page=1,
            per_page=len(sessions)
        )
    
    def is_agno_available(self) -> bool:
        """Verifica se Agno SDK está disponível"""
        return self._agno_client is not None
    
    def get_agno_status(self) -> Dict[str, Any]:
        """Retorna status do Agno SDK"""
        return {
            "available": self.is_agno_available(),
            "agents_count": len(self.active_agents),
            "sessions_count": len(self.active_sessions),
            "sdk_version": "agno>=0.1.0" if self.is_agno_available() else "not_installed"
        }
