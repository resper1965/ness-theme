"""
Serviço de migração de dados em memória para banco de dados
"""

import logging
from typing import Dict, List
from app.services.agent_persistence_service import AgentPersistenceService
from app.models.agent import Agent
from app.schemas.agent import AgentCreate

logger = logging.getLogger(__name__)

class MigrationService:
    """Serviço para migração de dados"""
    
    def __init__(self, persistence_service: AgentPersistenceService):
        self.persistence = persistence_service
    
    async def migrate_agents_to_database(self, agents_in_memory: Dict[str, Agent]) -> Dict[str, str]:
        """
        Migra agentes da memória para o banco de dados
        Retorna mapeamento de IDs antigos para novos
        """
        try:
            migration_map = {}
            
            for agent_id, agent in agents_in_memory.items():
                # Criar dados para migração
                agent_data = AgentCreate(
                    id=agent.id,
                    name=agent.name,
                    description=agent.description,
                    type=agent.type,
                    model=agent.model,
                    knowledge_sources=agent.knowledge_sources
                )
                
                # Persistir no banco
                persisted_agent = await self.persistence.create_agent(
                    agent_data, 
                    session_id=agent.session_id
                )
                
                migration_map[agent_id] = persisted_agent.id
                
                logger.info(f"✅ Agente {agent_id} migrado para {persisted_agent.id}")
            
            logger.info(f"✅ Migração concluída: {len(migration_map)} agentes migrados")
            return migration_map
            
        except Exception as e:
            logger.error(f"❌ Erro na migração: {e}")
            raise
    
    async def sync_agents_from_database(self) -> Dict[str, Agent]:
        """
        Sincroniza agentes do banco de dados para memória
        Retorna dicionário de agentes para carregar na memória
        """
        try:
            # Buscar todos os agentes ativos do banco
            agents_from_db = await self.persistence.get_all_agents(status="active")
            
            agents_in_memory = {}
            
            for agent_response in agents_from_db:
                # Converter para modelo de memória
                agent = Agent(
                    id=agent_response.id,
                    name=agent_response.name,
                    description=agent_response.description,
                    type=agent_response.type,
                    model=agent_response.model,
                    knowledge_sources=[],  # Será carregado separadamente se necessário
                    session_id=agent_response.session_id,
                    status=agent_response.status
                )
                
                agents_in_memory[agent.id] = agent
            
            logger.info(f"✅ Sincronização concluída: {len(agents_in_memory)} agentes carregados")
            return agents_in_memory
            
        except Exception as e:
            logger.error(f"❌ Erro na sincronização: {e}")
            raise
