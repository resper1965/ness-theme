"""
Wrapper para AgnoService com persistência transparente
Mantém o AgnoService original intacto - apenas adiciona persistência
"""

import logging
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session as DBSession
from app.services.agno_service import AgnoService
from app.services.agent_persistence_service import AgentPersistenceService
from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate, AgentHealth, AgentClone, AgentTemplate

logger = logging.getLogger(__name__)

class AgnoServiceWrapper:
    """
    Wrapper que adiciona persistência ao AgnoService sem modificá-lo
    Mantém 100% de compatibilidade com a interface original
    """
    
    def __init__(self, db_session: DBSession):
        # Manter o AgnoService original intacto
        self.agno_service = AgnoService()
        
        # Adicionar persistência como camada adicional
        self.persistence_service = AgentPersistenceService(db_session)
        
        # Flag para controlar persistência
        self.persistence_enabled = True
        
        logger.info("✅ AgnoServiceWrapper inicializado com persistência transparente")
    
    # ===== DELEGAÇÃO TRANSPARENTE PARA AGNOSERVICE =====
    
    async def create_session(self, *args, **kwargs):
        """Delega para AgnoService original"""
        return await self.agno_service.create_session(*args, **kwargs)
    
    async def get_sessions(self, *args, **kwargs):
        """Delega para AgnoService original"""
        return await self.agno_service.get_sessions(*args, **kwargs)
    
    async def get_agent_details(self, *args, **kwargs):
        """Delega para AgnoService original"""
        return await self.agno_service.get_agent_details(*args, **kwargs)
    
    async def send_message(self, *args, **kwargs):
        """Delega para AgnoService original"""
        return await self.agno_service.send_message(*args, **kwargs)
    
    # ===== MÉTODOS COM PERSISTÊNCIA TRANSPARENTE =====
    
    async def create_agent(self, agent_data: AgentCreate, session_id: str = None) -> AgentResponse:
        """Cria agente com persistência transparente"""
        try:
            # Executar no AgnoService original
            result = await self.agno_service.create_agent(agent_data, session_id)
            
            # Persistir no banco se habilitado
            if self.persistence_enabled:
                try:
                    await self.persistence_service.create_agent(agent_data, session_id)
                    logger.info(f"✅ Agente {result.id} persistido automaticamente")
                except Exception as e:
                    logger.warning(f"⚠️ Falha na persistência: {e}")
                    # Não falhar o método original
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar agente: {e}")
            raise
    
    async def get_agents(self, session_id: str = None) -> List[AgentResponse]:
        """Lista agentes com fallback para banco se necessário"""
        try:
            # Tentar buscar da memória primeiro (AgnoService original)
            result = await self.agno_service.get_agents(session_id)
            
            # Se não há agentes na memória, buscar do banco
            if not result and self.persistence_enabled:
                try:
                    result = await self.persistence_service.get_all_agents(session_id=session_id)
                    logger.info(f"✅ {len(result)} agentes carregados do banco")
                except Exception as e:
                    logger.warning(f"⚠️ Falha ao carregar do banco: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar agentes: {e}")
            raise
    
    async def update_agent(self, agent_id: str, updates: AgentUpdate) -> AgentResponse:
        """Atualiza agente com persistência transparente"""
        try:
            # Executar no AgnoService original
            result = await self.agno_service.update_agent(agent_id, updates)
            
            # Persistir no banco se habilitado
            if self.persistence_enabled:
                try:
                    await self.persistence_service.update_agent(agent_id, updates)
                    logger.info(f"✅ Agente {agent_id} atualizado no banco")
                except Exception as e:
                    logger.warning(f"⚠️ Falha na persistência: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar agente: {e}")
            raise
    
    async def delete_agent(self, agent_id: str) -> bool:
        """Remove agente com persistência transparente"""
        try:
            # Executar no AgnoService original
            result = await self.agno_service.delete_agent(agent_id)
            
            # Persistir no banco se habilitado
            if self.persistence_enabled and result:
                try:
                    await self.persistence_service.delete_agent(agent_id, soft_delete=True)
                    logger.info(f"✅ Agente {agent_id} removido do banco")
                except Exception as e:
                    logger.warning(f"⚠️ Falha na persistência: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao remover agente: {e}")
            raise
    
    # ===== MÉTODOS CRUD ADICIONAIS (sem tocar no AgnoService) =====
    
    async def clone_agent(self, source_agent_id: str, clone_data: AgentClone) -> AgentResponse:
        """Clona agente usando AgnoService + persistência"""
        try:
            # Buscar agente fonte do AgnoService
            source_agent = self.agno_service.active_agents.get(source_agent_id)
            if not source_agent:
                raise ValueError("Agente fonte não encontrado")
            
            # Criar dados para clonagem
            agent_data = AgentCreate(
                id=f"agent-{self.agno_service._generate_id()}",
                name=clone_data.new_name,
                description=clone_data.new_description or source_agent.description,
                type=source_agent.type,
                model=source_agent.model,
                knowledge_sources=source_agent.knowledge_sources.copy()
            )
            
            # Criar agente clonado
            cloned_agent = await self.create_agent(agent_data, clone_data.session_id)
            
            logger.info(f"✅ Agente {source_agent_id} clonado como {cloned_agent.id}")
            return cloned_agent
            
        except Exception as e:
            logger.error(f"❌ Erro ao clonar agente: {e}")
            raise
    
    async def get_agent_health(self, agent_id: str) -> AgentHealth:
        """Verifica saúde do agente"""
        try:
            # Usar AgnoService original se disponível
            if hasattr(self.agno_service, 'get_agent_health'):
                return await self.agno_service.get_agent_health(agent_id)
            
            # Fallback para persistência
            if self.persistence_enabled:
                return await self.persistence_service.get_agent_health(agent_id)
            
            # Fallback básico
            agent = self.agno_service.active_agents.get(agent_id)
            if not agent:
                raise ValueError("Agente não encontrado")
            
            return AgentHealth(
                agent_id=agent_id,
                status="healthy" if agent.status == "active" else "warning",
                last_check=agent.created_at.isoformat(),
                metrics={"status": agent.status},
                issues=[]
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao verificar saúde: {e}")
            raise
    
    async def restart_agent(self, agent_id: str) -> bool:
        """Reinicia agente"""
        try:
            # Usar AgnoService original se disponível
            if hasattr(self.agno_service, 'restart_agent'):
                return await self.agno_service.restart_agent(agent_id)
            
            # Implementação básica
            agent = self.agno_service.active_agents.get(agent_id)
            if not agent:
                return False
            
            agent.status = "active"
            logger.info(f"✅ Agente {agent_id} reiniciado")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao reiniciar agente: {e}")
            raise
    
    # ===== MÉTODOS DE PERSISTÊNCIA ADICIONAIS =====
    
    async def sync_from_database(self):
        """Sincroniza agentes do banco para memória"""
        try:
            if not self.persistence_enabled:
                return
            
            # Buscar agentes do banco
            agents_from_db = await self.persistence_service.get_all_agents(status="active")
            
            # Adicionar à memória se não existirem
            for agent_response in agents_from_db:
                if agent_response.id not in self.agno_service.active_agents:
                    # Converter para modelo de memória
                    from app.models.agent import Agent, AgentType
                    agent = Agent(
                        id=agent_response.id,
                        name=agent_response.name,
                        description=agent_response.description,
                        type=agent_response.type,
                        model=agent_response.model,
                        knowledge_sources=[],
                        session_id=agent_response.session_id,
                        status=agent_response.status
                    )
                    
                    self.agno_service.active_agents[agent.id] = agent
                    
                    # Adicionar à sessão se necessário
                    if agent.session_id and agent.session_id in self.agno_service.active_sessions:
                        if agent.id not in self.agno_service.active_sessions[agent.session_id].agent_ids:
                            self.agno_service.active_sessions[agent.session_id].agent_ids.append(agent.id)
            
            logger.info(f"✅ {len(agents_from_db)} agentes sincronizados do banco")
            
        except Exception as e:
            logger.error(f"❌ Erro na sincronização: {e}")
    
    def toggle_persistence(self, enabled: bool):
        """Habilita/desabilita persistência"""
        self.persistence_enabled = enabled
        logger.info(f"✅ Persistência {'habilitada' if enabled else 'desabilitada'}")
    
    # ===== PROPRIEDADES PARA COMPATIBILIDADE =====
    
    @property
    def active_agents(self):
        """Acesso direto aos agentes ativos"""
        return self.agno_service.active_agents
    
    @property
    def active_sessions(self):
        """Acesso direto às sessões ativas"""
        return self.agno_service.active_sessions
