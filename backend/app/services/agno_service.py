"""
Serviço de integração com Agno SDK
Gerencia criação dinâmica de agentes e orquestração
"""

import logging
from typing import List, Dict, Optional, Any
from app.config.settings import get_settings
from app.models.agent import Agent, AgentType
from app.models.session import Session
from app.schemas.agent import AgentCreate, AgentResponse
from app.schemas.session import SessionCreate, SessionResponse
from app.services.agent_manager import AgentManager

logger = logging.getLogger(__name__)

class AgnoService:
    """Serviço principal para integração com Agno SDK"""
    
    def __init__(self):
        self.settings = get_settings()
        self.agno_client = None
        self.active_sessions: Dict[str, Session] = {}
        self.active_agents: Dict[str, Agent] = {}
        self.agent_manager = AgentManager()
    
    async def initialize(self):
        """Inicializa o serviço Agno"""
        try:
            # Importar Agno SDK quando disponível
            # from agno import AgnoClient
            
            # self.agno_client = AgnoClient(
            #     api_key=self.settings.AGNO_API_KEY,
            #     openai_api_key=self.settings.OPENAI_API_KEY
            # )
            
            # Por enquanto, simular inicialização
            logger.info("✅ Agno Service inicializado (modo simulação)")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Agno Service: {e}")
            raise
    
    async def cleanup(self):
        """Limpa recursos do serviço"""
        try:
            # Cleanup de sessões ativas
            for session_id in list(self.active_sessions.keys()):
                await self.end_session(session_id)
            
            logger.info("✅ Agno Service finalizado")
            
        except Exception as e:
            logger.error(f"❌ Erro ao finalizar Agno Service: {e}")
    
    async def create_session(self, session_data: SessionCreate) -> SessionResponse:
        """Cria uma nova sessão de chat"""
        try:
            session = Session(
                id=session_data.id,
                name=session_data.name,
                description=session_data.description,
                max_agents=self.settings.MAX_AGENTS_PER_SESSION,
                max_orchestrator=self.settings.MAX_ORCHESTRATOR_PER_SESSION
            )
            
            self.active_sessions[session.id] = session
            
            logger.info(f"✅ Sessão criada: {session.id}")
            
            return SessionResponse(
                id=session.id,
                name=session.name,
                description=session.description,
                status="active",
                agents_count=0,
                orchestrator_count=0
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar sessão: {e}")
            raise
    
    async def create_agent(self, session_id: str, agent_data: AgentCreate) -> AgentResponse:
        """Cria um novo agente na sessão"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError("Sessão não encontrada")
            
            session = self.active_sessions[session_id]
            
            # Verificar limites usando AgentManager
            if not self.agent_manager.validate_session_limits(session, agent_data.type):
                if agent_data.type == AgentType.ORCHESTRATOR:
                    raise ValueError("Limite de orquestradores atingido")
                else:
                    raise ValueError("Limite de agentes atingido")
            
            # Criar agente
            agent = Agent(
                id=agent_data.id,
                name=agent_data.name,
                description=agent_data.description,
                type=agent_data.type,
                model=agent_data.model,
                knowledge_sources=agent_data.knowledge_sources,
                session_id=session_id
            )
            
            self.active_agents[agent.id] = agent
            session.add_agent(agent)
            
            logger.info(f"✅ Agente criado: {agent.id} na sessão {session_id}")
            
            return AgentResponse(
                id=agent.id,
                name=agent.name,
                description=agent.description,
                type=agent.type,
                model=agent.model,
                status="active",
                session_id=session_id
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar agente: {e}")
            raise
    
    async def create_agent_from_template(self, session_id: str, template_name: str, custom_config: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Cria agente a partir de template"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError("Sessão não encontrada")
            
            # Criar agente usando AgentManager
            agent_data = self.agent_manager.create_agent_from_template(template_name, session_id, custom_config)
            
            # Criar agente normalmente
            return await self.create_agent(session_id, agent_data)
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar agente do template: {e}")
            raise
    
    async def create_agent_workflow(self, session_id: str, task_description: str) -> List[AgentResponse]:
        """Cria workflow de agentes baseado na tarefa"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError("Sessão não encontrada")
            
            # Criar workflow usando AgentManager
            agents_data = self.agent_manager.create_agent_workflow(session_id, task_description)
            agents = []
            
            for agent_data in agents_data:
                try:
                    agent = await self.create_agent(session_id, agent_data)
                    agents.append(agent)
                except Exception as e:
                    logger.warning(f"Erro ao criar agente {agent_data.name}: {e}")
                    continue
            
            logger.info(f"✅ Workflow criado com {len(agents)} agentes para tarefa: {task_description}")
            return agents
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar workflow: {e}")
            raise
    
    async def get_session_agents(self, session_id: str) -> List[AgentResponse]:
        """Retorna agentes de uma sessão"""
        try:
            if session_id not in self.active_sessions:
                return []
            
            session = self.active_sessions[session_id]
            agents = []
            
            for agent_id in session.agent_ids:
                if agent_id in self.active_agents:
                    agent = self.active_agents[agent_id]
                    agents.append(AgentResponse(
                        id=agent.id,
                        name=agent.name,
                        description=agent.description,
                        type=agent.type,
                        model=agent.model,
                        status="active",
                        session_id=session_id
                    ))
            
            return agents
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar agentes: {e}")
            raise
    
    async def process_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """Processa mensagem através dos agentes da sessão"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError("Sessão não encontrada")
            
            session = self.active_sessions[session_id]
            
            # Buscar orquestrador
            orchestrator = None
            for agent_id in session.agent_ids:
                if agent_id in self.active_agents:
                    agent = self.active_agents[agent_id]
                    if agent.type == AgentType.ORCHESTRATOR:
                        orchestrator = agent
                        break
            
            if not orchestrator:
                raise ValueError("Nenhum orquestrador encontrado na sessão")
            
            # Processar mensagem (implementação futura com Agno SDK)
            response = {
                "message": f"Processando mensagem: {message}",
                "session_id": session_id,
                "orchestrator_id": orchestrator.id,
                "agents_involved": session.agent_ids
            }
            
            logger.info(f"✅ Mensagem processada na sessão {session_id}")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar mensagem: {e}")
            raise
    
    async def end_session(self, session_id: str) -> bool:
        """Finaliza uma sessão"""
        try:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                
                # Remover agentes da sessão
                for agent_id in session.agent_ids:
                    if agent_id in self.active_agents:
                        del self.active_agents[agent_id]
                
                # Remover sessão
                del self.active_sessions[session_id]
                
                logger.info(f"✅ Sessão finalizada: {session_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao finalizar sessão: {e}")
            raise
