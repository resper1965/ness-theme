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
from app.schemas.agent import AgentCreate, AgentResponse, AgentDetails, MessageRequest, MessageResponse, AgentUpdate, AgentClone, AgentHealth, AgentTemplate
from app.schemas.session import SessionCreate, SessionResponse, SessionEntry, Sessions, Pagination
from app.services.agent_manager import AgentManager
from app.services.workflow_service import WorkflowService
from app.services.agno_sdk_service import AgnoSDKService
from app.services.sql_service import SQLService
from app.services.vectorized_sql_service import VectorizedSQLService

logger = logging.getLogger(__name__)

class AgnoService:
    """Serviço principal para integração com Agno SDK - Implementação baseada no documento oficial"""
    
    def __init__(self):
        self.settings = get_settings()
        self.active_sessions: Dict[str, Session] = {}
        self.active_agents: Dict[str, Agent] = {}
        self.agent_manager = AgentManager()
        self.workflow_service = WorkflowService()
        self.agno_sdk_service = AgnoSDKService()
        self.sql_service = SQLService()
        self.vectorized_sql_service = VectorizedSQLService()
        self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Inicializa dados padrão como no Agno original"""
        # Criar agentes especializados para imobiliário e financeiro
        agents_data = [
            {
                "id": "correlation-agent",
                "name": "Analista de Correlação",
                "description": "Especialista em correlação de dados, análise estatística avançada e identificação de padrões em grandes volumes de dados imobiliários e financeiros",
                "type": AgentType.AGENT,
                "model": "gpt-4",
                "capabilities": [
                    "correlation_analysis", 
                    "statistical_modeling", 
                    "pattern_recognition",
                    "data_correlation",
                    "trend_analysis",
                    "statistical_significance",
                    "regression_analysis",
                    "time_series_analysis"
                ],
                "specialization": "Correlação de Dados",
                "expertise_areas": [
                    "Análise de correlação entre variáveis imobiliárias",
                    "Identificação de padrões em dados de vendas",
                    "Análise estatística de performance de carteiras",
                    "Correlação entre indicadores econômicos e imobiliários",
                    "Análise de sazonalidade e tendências"
                ]
            },
            {
                "id": "portfolio-agent",
                "name": "Gestor de Carteira Imobiliária",
                "description": "Especialista em gestão de carteiras imobiliárias, análise de risco, diversificação de portfólio e estratégias de investimento imobiliário",
                "type": AgentType.AGENT,
                "model": "gpt-4",
                "capabilities": [
                    "portfolio_management",
                    "real_estate_analysis", 
                    "risk_assessment",
                    "portfolio_optimization",
                    "investment_strategy",
                    "asset_allocation",
                    "performance_analysis",
                    "market_analysis"
                ],
                "specialization": "Gestão de Carteira Imobiliária",
                "expertise_areas": [
                    "Análise de carteiras imobiliárias",
                    "Gestão de risco em investimentos imobiliários",
                    "Otimização de portfólio imobiliário",
                    "Análise de performance de ativos",
                    "Estratégias de diversificação imobiliária",
                    "Análise de liquidez em carteiras imobiliárias"
                ]
            },
            {
                "id": "financial-agent",
                "name": "Especialista Financeiro",
                "description": "Especialista em matemática financeira, análise de investimentos, cálculos de rentabilidade, avaliação de projetos e gestão financeira avançada",
                "type": AgentType.AGENT,
                "model": "gpt-4",
                "capabilities": [
                    "financial_mathematics",
                    "investment_analysis",
                    "profitability_calculations",
                    "financial_modeling",
                    "risk_analysis",
                    "valuation_methods",
                    "cash_flow_analysis",
                    "financial_planning"
                ],
                "specialization": "Matemática Financeira",
                "expertise_areas": [
                    "Cálculos de rentabilidade (TIR, VPL, Payback)",
                    "Análise de viabilidade financeira",
                    "Avaliação de ativos e investimentos",
                    "Matemática financeira aplicada",
                    "Análise de fluxo de caixa",
                    "Cálculos de juros compostos e inflação",
                    "Análise de sensibilidade financeira",
                    "Modelagem financeira avançada"
                ]
            },
            {
                "id": "orchestrator-agent",
                "name": "Orquestrador",
                "description": "Agente coordenador que gerencia outros agentes especializados e integra análises",
                "type": AgentType.ORCHESTRATOR,
                "model": "gpt-4",
                "capabilities": ["coordination", "management", "synthesis", "integration"],
                "specialization": "Coordenação de Especialistas"
            }
        ]
        
        # Criar agentes
        for agent_data in agents_data:
            agent = Agent(
                id=agent_data["id"],
                name=agent_data["name"],
                description=agent_data["description"],
                type=agent_data["type"],
                model=agent_data["model"],
                knowledge_sources=[],
                session_id="default-session",
                specialization=agent_data.get("specialization"),
                expertise_areas=agent_data.get("expertise_areas", []),
                capabilities=agent_data.get("capabilities", [])
            )
            
            self.active_agents[agent_data["id"]] = agent
        
        # Criar sessão padrão
        default_session = Session(
            id="default-session",
            name="Sessão Padrão",
            description="Sessão padrão do Gabi com todos os agentes",
            max_agents=self.settings.MAX_AGENTS_PER_SESSION,
            max_orchestrator=self.settings.MAX_ORCHESTRATOR_PER_SESSION
        )
        
        # Adicionar agentes especializados como padrão
        default_session.add_agent(self.active_agents["correlation-agent"])
        default_session.add_agent(self.active_agents["portfolio-agent"])
        default_session.add_agent(self.active_agents["financial-agent"])
        default_session.add_agent(self.active_agents["orchestrator-agent"])
        self.active_sessions["default-session"] = default_session
        
        logger.info(f"✅ {len(agents_data)} agentes especializados inicializados")
    
    def _select_specialized_agent(self, message: str, session) -> Optional[Agent]:
        """Seleciona o agente especializado mais adequado baseado no contexto da mensagem"""
        message_lower = message.lower()
        
        # Palavras-chave para cada especialização
        correlation_keywords = [
            "correlação", "correlacionar", "correlacionado", "padrão", "padrões",
            "tendência", "tendências", "análise estatística", "estatística",
            "regressão", "correlação", "significância", "sazonalidade",
            "dados", "análise de dados", "performance", "indicadores"
        ]
        
        portfolio_keywords = [
            "carteira", "portfólio", "portfólio imobiliário", "gestão de carteira",
            "diversificação", "risco", "análise de risco", "otimização",
            "alocação", "alocação de ativos", "performance de carteira",
            "liquidez", "investimento imobiliário", "ativo", "ativos"
        ]
        
        financial_keywords = [
            "matemática financeira", "rentabilidade", "tir", "vpl", "payback",
            "viabilidade", "viabilidade financeira", "avaliação", "projeto",
            "fluxo de caixa", "juros", "inflação", "modelagem financeira",
            "cálculo", "cálculos", "investimento", "retorno", "roi"
        ]
        
        # Contar matches para cada especialização
        correlation_score = sum(1 for keyword in correlation_keywords if keyword in message_lower)
        portfolio_score = sum(1 for keyword in portfolio_keywords if keyword in message_lower)
        financial_score = sum(1 for keyword in financial_keywords if keyword in message_lower)
        
        # Selecionar agente com maior score
        if correlation_score > portfolio_score and correlation_score > financial_score:
            agent_id = "correlation-agent"
            logger.info(f"🎯 Selecionado: Analista de Correlação (score: {correlation_score})")
        elif portfolio_score > financial_score:
            agent_id = "portfolio-agent"
            logger.info(f"🎯 Selecionado: Gestor de Carteira (score: {portfolio_score})")
        elif financial_score > 0:
            agent_id = "financial-agent"
            logger.info(f"🎯 Selecionado: Especialista Financeiro (score: {financial_score})")
        else:
            # Se não há palavras-chave específicas, usar orquestrador
            agent_id = "orchestrator-agent"
            logger.info("🎯 Selecionado: Orquestrador (contexto geral)")
        
        # Retornar agente se estiver na sessão
        if agent_id in self.active_agents:
            return self.active_agents[agent_id]
        
        return None
    
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
            # Tentar usar Agno SDK real primeiro
            if self.agno_sdk_service.is_agno_available():
                logger.info("🚀 Usando Agno SDK real para criar agente")
                # Adicionar session_id ao agent_data
                agent_data.session_id = session_id
                return await self.agno_sdk_service.create_agent(agent_data)
            
            # Fallback para implementação mockup
            logger.info("⚠️ Usando implementação mockup (Agno SDK não disponível)")
            
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
            # Tentar usar Agno SDK real primeiro
            if self.agno_sdk_service.is_agno_available():
                logger.info("🚀 Usando Agno SDK real para processar mensagem")
                from app.schemas.agent import MessageRequest
                message_request = MessageRequest(
                    message=message,
                    session_id=session_id,
                    agent_id="orchestrator"  # Usar orquestrador por padrão
                )
                response = await self.agno_sdk_service.send_message(message_request)
                return {
                    "message": response.content,
                    "session_id": session_id,
                    "agent_id": response.agent_id,
                    "metadata": response.metadata
                }
            
            # Fallback para implementação mockup
            logger.info("⚠️ Usando implementação mockup (Agno SDK não disponível)")
            
            if session_id not in self.active_sessions:
                # Criar sessão automaticamente se não existir
                logger.info(f"📝 Criando sessão automática: {session_id}")
                session = Session(
                    id=session_id,
                    name=f"Sessão {session_id}",
                    description="Sessão criada automaticamente",
                    max_agents=self.settings.MAX_AGENTS_PER_SESSION,
                    max_orchestrator=self.settings.MAX_ORCHESTRATOR_PER_SESSION
                )
                # Adicionar agentes especializados à sessão
                session.add_agent(self.active_agents["correlation-agent"])
                session.add_agent(self.active_agents["portfolio-agent"])
                session.add_agent(self.active_agents["financial-agent"])
                session.add_agent(self.active_agents["orchestrator-agent"])
                self.active_sessions[session_id] = session
            else:
                session = self.active_sessions[session_id]
            
            # Selecionar agente especializado baseado no contexto da mensagem
            selected_agent = self._select_specialized_agent(message, session)
            
            if not selected_agent:
                # Fallback para orquestrador
                for agent_id in session.agent_ids:
                    if agent_id in self.active_agents:
                        agent = self.active_agents[agent_id]
                        if agent.type == AgentType.ORCHESTRATOR:
                            selected_agent = agent
                            break
                
                # Se não encontrou orquestrador, usar primeiro agente disponível
                if not selected_agent and session.agent_ids:
                    for agent_id in session.agent_ids:
                        if agent_id in self.active_agents:
                            selected_agent = self.active_agents[agent_id]
                            break
            
            if not selected_agent:
                raise ValueError("Nenhum agente encontrado na sessão")
            
            # Processar mensagem com integração SQL (RAG)
            logger.info("🔍 Processando mensagem com integração SQL...")
            
            # Tentar buscar dados relevantes usando vetorização semântica
            sql_context = ""
            try:
                # Usar busca semântica vetorizada
                sql_context = self.vectorized_sql_service.generate_semantic_context(message)
                logger.info(f"🧠 Contexto semântico gerado: {len(sql_context)} caracteres")
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca semântica, tentando SQL tradicional: {e}")
                try:
                    # Fallback para SQL tradicional
                    with self.sql_service as sql:
                        sql_context = sql.generate_context(message)
                        logger.info(f"📊 Contexto SQL tradicional: {len(sql_context)} caracteres")
                except Exception as e2:
                    logger.warning(f"⚠️ Erro no SQL tradicional: {e2}")
                    sql_context = ""
            
            # Gerar resposta baseada no conteúdo da mensagem e contexto SQL
            if "oi" in message.lower() or "olá" in message.lower() or "hello" in message.lower():
                response_message = "Olá! Eu sou o Gabi, seu assistente de IA. Como posso ajudar você hoje?"
            elif "como" in message.lower() and "funciona" in message.lower():
                response_message = "Eu sou um sistema de chat multi-agentes baseado no padrão BMAD. Posso processar suas mensagens, responder perguntas e ajudar com diversas tarefas. Estou aqui para auxiliar você!"
            elif "capital" in message.lower() and "brasil" in message.lower():
                response_message = "A capital do Brasil é Brasília. Foi inaugurada em 21 de abril de 1960 e está localizada no Distrito Federal."
            elif "cor" in message.lower() and "céu" in message.lower():
                response_message = "O céu é azul durante o dia devido à dispersão da luz solar na atmosfera (dispersão de Rayleigh). À noite, aparece escuro com estrelas."
            elif "dados" in message.lower() or "banco" in message.lower() or "sql" in message.lower():
                # Resposta específica para consultas de dados
                if sql_context and "Não encontrei dados" not in sql_context:
                    response_message = f"Baseado nos dados do banco REB_BI_IA:\n\n{sql_context}\n\nPosso ajudar com mais consultas sobre esses dados!"
                else:
                    response_message = "Conectei ao banco REB_BI_IA, mas não encontrei dados específicos para sua pergunta. Pode reformular ou ser mais específico?"
            elif "qual" in message.lower() and "?" in message:
                # Resposta direta para perguntas diretas com contexto SQL
                if sql_context and "Não encontrei dados" not in sql_context:
                    response_message = f"Baseado nos dados disponíveis:\n\n{sql_context}\n\nEsta é a informação que encontrei para sua pergunta: {message.replace('?', '')}"
                else:
                    response_message = f"Vou responder sua pergunta: {message.replace('?', '')}. Preciso de mais informações específicas para dar uma resposta mais precisa. Pode reformular a pergunta?"
            elif "?" in message:
                # Perguntas gerais com contexto SQL
                if sql_context and "Não encontrei dados" not in sql_context:
                    response_message = f"Baseado nos dados do banco:\n\n{sql_context}\n\nEsta é a informação que encontrei para sua pergunta: {message}"
                else:
                    response_message = f"Entendi sua pergunta: {message}. Vou tentar ajudar da melhor forma possível. Pode me dar mais detalhes sobre o que você precisa?"
            else:
                # Mensagens gerais com contexto SQL se disponível
                if sql_context and "Não encontrei dados" not in sql_context:
                    response_message = f"Entendi sua mensagem: '{message}'. Encontrei algumas informações relevantes no banco:\n\n{sql_context}\n\nComo posso auxiliar você com isso?"
                else:
                    response_message = f"Entendi sua mensagem: '{message}'. Como posso auxiliar você com isso?"
            
            response = {
                "message": response_message,
                "session_id": session_id,
                "agent_id": selected_agent.id,
                "agent_name": selected_agent.name,
                "agent_specialization": getattr(selected_agent, 'specialization', 'Geral'),
                "agents_involved": session.agent_ids,
                "metadata": {
                    "processing_time": "instant",
                    "agent_type": str(selected_agent.type),
                    "model": selected_agent.model,
                    "sql_context_used": bool(sql_context and "Não encontrei dados" not in sql_context),
                    "sql_context_length": len(sql_context) if sql_context else 0,
                    "specialization": getattr(selected_agent, 'specialization', 'Geral')
                }
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

    # ===== MÉTODOS CRUD PARA ADMINISTRAÇÃO =====
    
    async def update_agent(self, agent_id: str, updates: AgentUpdate) -> AgentResponse:
        """Atualiza um agente existente mantendo operacionalidade"""
        try:
            if agent_id not in self.active_agents:
                raise ValueError("Agente não encontrado")
            
            agent = self.active_agents[agent_id]
            
            # Aplicar updates gradualmente para manter operacionalidade
            if updates.name is not None:
                agent.name = updates.name
            if updates.description is not None:
                agent.description = updates.description
            if updates.model is not None:
                agent.model = updates.model
            if updates.knowledge_sources is not None:
                agent.knowledge_sources = updates.knowledge_sources
            if updates.status is not None:
                agent.status = updates.status
            
            logger.info(f"✅ Agente {agent_id} atualizado com sucesso")
            
            return AgentResponse(
                id=agent.id,
                name=agent.name,
                description=agent.description,
                type=agent.type,
                model=agent.model,
                status=agent.status,
                session_id=agent.session_id
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar agente: {e}")
            raise
    
    async def delete_agent(self, agent_id: str) -> bool:
        """Remove um agente (soft delete)"""
        try:
            if agent_id not in self.active_agents:
                return False
            
            # Soft delete - marcar como inativo
            agent = self.active_agents[agent_id]
            agent.status = "deleted"
            
            # Remover de sessões ativas
            for session in self.active_sessions.values():
                if agent_id in session.agent_ids:
                    session.agent_ids.remove(agent_id)
            
            logger.info(f"✅ Agente {agent_id} removido (soft delete)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao remover agente: {e}")
            raise
    
    async def clone_agent(self, source_agent_id: str, clone_data: AgentClone) -> AgentResponse:
        """Clona um agente existente"""
        try:
            if source_agent_id not in self.active_agents:
                raise ValueError("Agente fonte não encontrado")
            
            source_agent = self.active_agents[source_agent_id]
            
            # Criar novo agente baseado no fonte
            new_agent_id = f"agent-{uuid.uuid4().hex[:8]}"
            new_agent = Agent(
                id=new_agent_id,
                name=clone_data.new_name,
                description=clone_data.new_description or source_agent.description,
                type=source_agent.type,
                model=source_agent.model,
                knowledge_sources=source_agent.knowledge_sources.copy(),
                session_id=clone_data.session_id or source_agent.session_id
            )
            
            self.active_agents[new_agent_id] = new_agent
            
            # Adicionar à sessão se especificada
            if clone_data.session_id and clone_data.session_id in self.active_sessions:
                self.active_sessions[clone_data.session_id].agent_ids.append(new_agent_id)
            
            logger.info(f"✅ Agente {source_agent_id} clonado como {new_agent_id}")
            
            return AgentResponse(
                id=new_agent.id,
                name=new_agent.name,
                description=new_agent.description,
                type=new_agent.type,
                model=new_agent.model,
                status="active",
                session_id=new_agent.session_id
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao clonar agente: {e}")
            raise
    
    async def get_agent_health(self, agent_id: str) -> AgentHealth:
        """Verifica saúde do agente"""
        try:
            if agent_id not in self.active_agents:
                raise ValueError("Agente não encontrado")
            
            agent = self.active_agents[agent_id]
            
            # Verificações básicas de saúde
            health_status = "healthy"
            issues = []
            
            # Verificar se agente está ativo
            if agent.status != "active":
                health_status = "warning"
                issues.append("Agente não está ativo")
            
            # Verificar se tem sessão válida
            if agent.session_id and agent.session_id not in self.active_sessions:
                health_status = "error"
                issues.append("Sessão associada não encontrada")
            
            # Verificar knowledge sources
            if not agent.knowledge_sources:
                health_status = "warning"
                issues.append("Nenhuma fonte de conhecimento configurada")
            
            return AgentHealth(
                agent_id=agent_id,
                status=health_status,
                last_check=datetime.now().isoformat(),
                metrics={
                    "status": agent.status,
                    "session_id": agent.session_id,
                    "knowledge_sources_count": len(agent.knowledge_sources),
                    "created_at": agent.created_at.isoformat()
                },
                issues=issues
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao verificar saúde do agente: {e}")
            raise
    
    async def restart_agent(self, agent_id: str) -> bool:
        """Reinicia um agente"""
        try:
            if agent_id not in self.active_agents:
                return False
            
            agent = self.active_agents[agent_id]
            
            # Simular reinicialização (manter estado mas resetar métricas)
            agent.status = "active"
            agent.created_at = datetime.now()
            
            logger.info(f"✅ Agente {agent_id} reiniciado")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao reiniciar agente: {e}")
            raise
    
    async def get_agent_templates(self) -> List[AgentTemplate]:
        """Retorna templates de agentes disponíveis"""
        try:
            templates = [
                AgentTemplate(
                    id="research-agent",
                    name="Research Agent",
                    description="Agente especializado em pesquisa e análise",
                    type=AgentType.AGENT,
                    model="gpt-4",
                    knowledge_sources=["rag", "website"],
                    capabilities=["web_search", "data_analysis"],
                    is_system=False
                ),
                AgentTemplate(
                    id="writing-agent",
                    name="Writing Agent",
                    description="Agente para criação de conteúdo",
                    type=AgentType.AGENT,
                    model="gpt-4",
                    knowledge_sources=["documents"],
                    capabilities=["content_generation", "editing"],
                    is_system=False
                ),
                AgentTemplate(
                    id="orchestrator-agent",
                    name="Orchestrator Agent",
                    description="Agente orquestrador para coordenação",
                    type=AgentType.ORCHESTRATOR,
                    model="gpt-4",
                    knowledge_sources=["rag"],
                    capabilities=["coordination", "task_management"],
                    is_system=False
                )
            ]
            
            return templates
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar templates: {e}")
            raise
    
    async def create_agent_from_template(self, template_id: str, session_id: str, custom_name: str = None) -> AgentResponse:
        """Cria agente a partir de template"""
        try:
            templates = await self.get_agent_templates()
            template = next((t for t in templates if t.id == template_id), None)
            
            if not template:
                raise ValueError("Template não encontrado")
            
            if session_id not in self.active_sessions:
                raise ValueError("Sessão não encontrada")
            
            # Criar agente do template
            new_agent_id = f"agent-{uuid.uuid4().hex[:8]}"
            new_agent = Agent(
                id=new_agent_id,
                name=custom_name or template.name,
                description=template.description,
                type=template.type,
                model=template.model,
                knowledge_sources=template.knowledge_sources.copy(),
                session_id=session_id
            )
            
            self.active_agents[new_agent_id] = new_agent
            self.active_sessions[session_id].agent_ids.append(new_agent_id)
            
            logger.info(f"✅ Agente criado do template {template_id}")
            
            return AgentResponse(
                id=new_agent.id,
                name=new_agent.name,
                description=new_agent.description,
                type=new_agent.type,
                model=new_agent.model,
                status="active",
                session_id=new_agent.session_id
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar agente do template: {e}")
            raise
    
    async def get_agent_metrics(self, agent_id: str) -> Dict[str, Any]:
        """Retorna métricas de performance do agente"""
        try:
            if agent_id not in self.active_agents:
                raise ValueError("Agente não encontrado")
            
            agent = self.active_agents[agent_id]
            
            # Métricas básicas (expandir conforme necessário)
            metrics = {
                "agent_id": agent_id,
                "status": agent.status,
                "created_at": agent.created_at.isoformat(),
                "session_id": agent.session_id,
                "knowledge_sources_count": len(agent.knowledge_sources),
                "uptime": (datetime.now() - agent.created_at).total_seconds(),
                "last_activity": datetime.now().isoformat()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar métricas: {e}")
            raise
    
    async def archive_agent(self, agent_id: str) -> bool:
        """Arquiva um agente"""
        try:
            if agent_id not in self.active_agents:
                return False
            
            agent = self.active_agents[agent_id]
            agent.status = "archived"
            
            logger.info(f"✅ Agente {agent_id} arquivado")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao arquivar agente: {e}")
            raise
    
    async def get_archived_agents(self) -> List[AgentResponse]:
        """Retorna agentes arquivados"""
        try:
            archived_agents = []
            
            for agent in self.active_agents.values():
                if agent.status == "archived":
                    archived_agents.append(AgentResponse(
                        id=agent.id,
                        name=agent.name,
                        description=agent.description,
                        type=agent.type,
                        model=agent.model,
                        status=agent.status,
                        session_id=agent.session_id
                    ))
            
            return archived_agents
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar agentes arquivados: {e}")
            raise
    
    async def restore_agent(self, agent_id: str) -> bool:
        """Restaura um agente arquivado"""
        try:
            if agent_id not in self.active_agents:
                return False
            
            agent = self.active_agents[agent_id]
            
            if agent.status == "archived":
                agent.status = "active"
                logger.info(f"✅ Agente {agent_id} restaurado")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao restaurar agente: {e}")
            raise

# Instância global do serviço
_agno_service_instance = None

def get_agno_service() -> AgnoService:
    """Retorna a instância global do AgnoService"""
    global _agno_service_instance
    if _agno_service_instance is None:
        _agno_service_instance = AgnoService()
    return _agno_service_instance
