"""
Serviço de integração com Agno SDK - Implementação baseada no documento oficial
Gerencia criação dinâmica de agentes e orquestração seguindo padrão BMAD
"""

import logging
import uuid
from typing import List, Dict, Optional, Any
from datetime import datetime
from app.config.settings import get_settings
from app.models.agent import Agent, AgentType
from app.models.session import Session
from app.schemas.agent import AgentCreate, AgentResponse, AgentDetails, MessageRequest, MessageResponse
from app.schemas.session import SessionCreate, SessionResponse, SessionEntry, Sessions, Pagination
from app.services.agent_manager import AgentManager
from app.services.workflow_service import WorkflowService

logger = logging.getLogger(__name__)

class AgnoService:
    """Serviço principal para integração com Agno SDK - Implementação baseada no documento oficial"""
    
    def __init__(self):
        self.settings = get_settings()
        self.active_sessions: Dict[str, Session] = {}
        self.active_agents: Dict[str, Agent] = {}
        self.agent_manager = AgentManager()
        self.workflow_service = WorkflowService()
        self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Inicializa dados padrão como no Agno original"""
        # Criar agente padrão
        default_agent = Agent(
            id="default-agent",
            name="Assistente Padrão",
            description="Agente assistente padrão do Gabi",
            type=AgentType.AGENT,
            model="gpt-4",
            knowledge_sources=[],
            session_id=None
        )
        self.active_agents["default-agent"] = default_agent
        
        # Criar sessão padrão
        default_session = Session(
            id="default-session",
            name="Sessão Padrão",
            description="Sessão padrão do Gabi",
            max_agents=self.settings.MAX_AGENTS_PER_SESSION,
            max_orchestrator=self.settings.MAX_ORCHESTRATOR_PER_SESSION
        )
        default_session.add_agent(default_agent)
        self.active_sessions["default-session"] = default_session
        
        logger.info("✅ Dados padrão inicializados")
    
    async def initialize(self):
        """Inicializa o serviço Agno"""
        try:
            logger.info("✅ Agno Service inicializado (clone do Agno original)")
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
            
            # Criar workflow usando WorkflowService
            workflow = await self.workflow_service.create_custom_workflow(session_id, task_description, [])
            
            # Criar agentes do workflow
            agents = []
            for agent_config in workflow["agents"]:
                try:
                    agent_data = AgentCreate(
                        id=f"agent-{uuid.uuid4().hex[:8]}",
                        name=agent_config["name"],
                        description=agent_config["description"],
                        type=AgentType(agent_config["type"]),
                        model=agent_config["model"],
                        knowledge_sources=[],
                        session_id=session_id
                    )
                    agent = await self.create_agent(session_id, agent_data)
                    agents.append(agent)
                except Exception as e:
                    logger.warning(f"Erro ao criar agente {agent_config['name']}: {e}")
                    continue
            
            logger.info(f"✅ Workflow criado com {len(agents)} agentes para tarefa: {task_description}")
            return agents
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar workflow: {e}")
            raise
    
    async def create_workflow_from_template(self, session_id: str, template_name: str, custom_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Cria workflow a partir de template"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError("Sessão não encontrada")
            
            workflow = await self.workflow_service.create_workflow_from_template(
                template_name, session_id, custom_config
            )
            
            logger.info(f"✅ Workflow criado do template {template_name}")
            return workflow
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar workflow do template: {e}")
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
    
    # Métodos específicos para compatibilidade com Agno UI
    
    def get_agents(self) -> List[AgentDetails]:
        """Retorna lista de agentes no formato esperado pelo frontend"""
        agents = []
        for agent_id, agent in self.active_agents.items():
            agents.append(AgentDetails(
                id=agent.id,
                name=agent.name,
                db_id=agent.session_id,
                model={"name": agent.model, "provider": "openai"} if agent.model else None
            ))
        return agents
    
    def get_sessions(self, type: str = "agent", component_id: str = "", db_id: str = "") -> Sessions:
        """Retorna lista de sessões no formato esperado pelo frontend"""
        sessions = []
        for session_id, session in self.active_sessions.items():
            sessions.append(SessionEntry(
                session_id=session.id,
                session_name=session.name,
                created_at=int(datetime.now().timestamp()),
                updated_at=int(datetime.now().timestamp())
            ))
        
        return Sessions(
            data=sessions,
            meta=Pagination(
                page=1,
                limit=10,
                total_pages=1,
                total_count=len(sessions)
            )
        )
    
    def get_teams(self) -> List[Dict[str, Any]]:
        """Retorna lista de times (workflows) - compatível com Agno UI"""
        return self.workflow_service.get_teams()
    
    def get_session_runs(self, session_id: str) -> List[Dict[str, Any]]:
        """Retorna runs de uma sessão"""
        if session_id not in self.active_sessions:
            return []
        
        # Simular dados de runs
        return [
            {
                "run_id": "run-1",
                "session_id": session_id,
                "status": "completed",
                "created_at": int(datetime.now().timestamp()),
                "messages": []
            }
        ]
    
    async def run_agent(self, agent_id: str, session_id: str, message: str, stream: bool = True) -> Dict[str, Any]:
        """Executa agente - compatível com Agno UI"""
        try:
            if agent_id not in self.active_agents:
                raise ValueError("Agente não encontrado")
            
            agent = self.active_agents[agent_id]
            
            # Simular execução do agente
            response = {
                "run_id": f"run-{uuid.uuid4().hex[:8]}",
                "agent_id": agent_id,
                "session_id": session_id,
                "status": "RUNNING",
                "message": f"Agente {agent.name} processando: {message}",
                "created_at": int(datetime.now().timestamp())
            }
            
            logger.info(f"✅ Agente {agent_id} executado")
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar agente: {e}")
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
