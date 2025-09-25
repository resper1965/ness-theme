"""
Serviço de persistência de agentes no banco de dados
"""

import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, or_
from app.models.database.agent_db import AgentDB, KnowledgeSourceDB, SessionDB, AgentMetricsDB, AgentTemplateDB
from app.models.agent import Agent, AgentType, KnowledgeSource
from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate, AgentTemplate, AgentHealth

logger = logging.getLogger(__name__)

class AgentPersistenceService:
    """Serviço para persistência de agentes no banco de dados"""
    
    def __init__(self, db_session: DBSession):
        self.db = db_session
    
    # ===== OPERAÇÕES CRUD BÁSICAS =====
    
    async def create_agent(self, agent_data: AgentCreate, session_id: str = None) -> AgentResponse:
        """Cria um novo agente no banco"""
        try:
            # Criar agente
            agent_db = AgentDB(
                id=agent_data.id,
                name=agent_data.name,
                description=agent_data.description,
                type=agent_data.type.value,
                model=agent_data.model,
                session_id=session_id,
                status="active"
            )
            
            self.db.add(agent_db)
            
            # Criar fontes de conhecimento
            for kb_source in agent_data.knowledge_sources:
                kb_db = KnowledgeSourceDB(
                    agent_id=agent_db.id,
                    name=kb_source.name,
                    type=kb_source.type,
                    config=kb_source.config,
                    status=kb_source.status
                )
                self.db.add(kb_db)
            
            self.db.commit()
            self.db.refresh(agent_db)
            
            logger.info(f"✅ Agente {agent_db.id} criado no banco")
            
            return AgentResponse(
                id=agent_db.id,
                name=agent_db.name,
                description=agent_db.description,
                type=AgentType(agent_db.type),
                model=agent_db.model,
                status=agent_db.status,
                session_id=agent_db.session_id or ""
            )
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Erro ao criar agente: {e}")
            raise
    
    async def get_agent(self, agent_id: str) -> Optional[AgentResponse]:
        """Busca um agente por ID"""
        try:
            agent_db = self.db.query(AgentDB).filter(AgentDB.id == agent_id).first()
            
            if not agent_db:
                return None
            
            return AgentResponse(
                id=agent_db.id,
                name=agent_db.name,
                description=agent_db.description,
                type=AgentType(agent_db.type),
                model=agent_db.model,
                status=agent_db.status,
                session_id=agent_db.session_id or ""
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar agente: {e}")
            raise
    
    async def get_all_agents(self, session_id: str = None, status: str = None) -> List[AgentResponse]:
        """Lista todos os agentes com filtros opcionais"""
        try:
            query = self.db.query(AgentDB)
            
            if session_id:
                query = query.filter(AgentDB.session_id == session_id)
            
            if status:
                query = query.filter(AgentDB.status == status)
            
            agents_db = query.all()
            
            return [
                AgentResponse(
                    id=agent.id,
                    name=agent.name,
                    description=agent.description,
                    type=AgentType(agent.type),
                    model=agent.model,
                    status=agent.status,
                    session_id=agent.session_id or ""
                )
                for agent in agents_db
            ]
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar agentes: {e}")
            raise
    
    async def update_agent(self, agent_id: str, updates: AgentUpdate) -> Optional[AgentResponse]:
        """Atualiza um agente existente"""
        try:
            agent_db = self.db.query(AgentDB).filter(AgentDB.id == agent_id).first()
            
            if not agent_db:
                return None
            
            # Aplicar updates
            if updates.name is not None:
                agent_db.name = updates.name
            if updates.description is not None:
                agent_db.description = updates.description
            if updates.model is not None:
                agent_db.model = updates.model
            if updates.status is not None:
                agent_db.status = updates.status
            
            agent_db.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(agent_db)
            
            logger.info(f"✅ Agente {agent_id} atualizado no banco")
            
            return AgentResponse(
                id=agent_db.id,
                name=agent_db.name,
                description=agent_db.description,
                type=AgentType(agent_db.type),
                model=agent_db.model,
                status=agent_db.status,
                session_id=agent_db.session_id or ""
            )
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Erro ao atualizar agente: {e}")
            raise
    
    async def delete_agent(self, agent_id: str, soft_delete: bool = True) -> bool:
        """Remove um agente (soft delete por padrão)"""
        try:
            agent_db = self.db.query(AgentDB).filter(AgentDB.id == agent_id).first()
            
            if not agent_db:
                return False
            
            if soft_delete:
                agent_db.status = "deleted"
                agent_db.updated_at = datetime.utcnow()
            else:
                # Hard delete - remover fontes de conhecimento primeiro
                self.db.query(KnowledgeSourceDB).filter(KnowledgeSourceDB.agent_id == agent_id).delete()
                self.db.query(AgentMetricsDB).filter(AgentMetricsDB.agent_id == agent_id).delete()
                self.db.delete(agent_db)
            
            self.db.commit()
            
            logger.info(f"✅ Agente {agent_id} removido (soft_delete={soft_delete})")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Erro ao remover agente: {e}")
            raise
    
    # ===== OPERAÇÕES AVANÇADAS =====
    
    async def clone_agent(self, source_agent_id: str, clone_data: Dict[str, Any]) -> AgentResponse:
        """Clona um agente existente"""
        try:
            source_agent = self.db.query(AgentDB).filter(AgentDB.id == source_agent_id).first()
            
            if not source_agent:
                raise ValueError("Agente fonte não encontrado")
            
            # Criar novo agente baseado no fonte
            new_agent = AgentDB(
                name=clone_data.get("new_name", f"{source_agent.name} (Cópia)"),
                description=clone_data.get("new_description", source_agent.description),
                type=source_agent.type,
                model=source_agent.model,
                session_id=clone_data.get("session_id", source_agent.session_id),
                status="active"
            )
            
            self.db.add(new_agent)
            self.db.flush()  # Para obter o ID
            
            # Clonar fontes de conhecimento
            source_kb_sources = self.db.query(KnowledgeSourceDB).filter(
                KnowledgeSourceDB.agent_id == source_agent_id
            ).all()
            
            for kb_source in source_kb_sources:
                new_kb = KnowledgeSourceDB(
                    agent_id=new_agent.id,
                    name=kb_source.name,
                    type=kb_source.type,
                    config=kb_source.config,
                    status=kb_source.status
                )
                self.db.add(new_kb)
            
            self.db.commit()
            self.db.refresh(new_agent)
            
            logger.info(f"✅ Agente {source_agent_id} clonado como {new_agent.id}")
            
            return AgentResponse(
                id=new_agent.id,
                name=new_agent.name,
                description=new_agent.description,
                type=AgentType(new_agent.type),
                model=new_agent.model,
                status=new_agent.status,
                session_id=new_agent.session_id or ""
            )
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Erro ao clonar agente: {e}")
            raise
    
    async def get_agent_health(self, agent_id: str) -> AgentHealth:
        """Verifica saúde do agente baseado em dados do banco"""
        try:
            agent_db = self.db.query(AgentDB).filter(AgentDB.id == agent_id).first()
            
            if not agent_db:
                raise ValueError("Agente não encontrado")
            
            # Verificações básicas de saúde
            health_status = "healthy"
            issues = []
            
            # Verificar status
            if agent_db.status not in ["active"]:
                health_status = "warning"
                issues.append(f"Agente com status: {agent_db.status}")
            
            # Verificar fontes de conhecimento
            kb_count = self.db.query(KnowledgeSourceDB).filter(
                KnowledgeSourceDB.agent_id == agent_id
            ).count()
            
            if kb_count == 0:
                health_status = "warning"
                issues.append("Nenhuma fonte de conhecimento configurada")
            
            # Verificar sessão
            if agent_db.session_id:
                session = self.db.query(SessionDB).filter(SessionDB.id == agent_db.session_id).first()
                if not session:
                    health_status = "error"
                    issues.append("Sessão associada não encontrada")
            
            return AgentHealth(
                agent_id=agent_id,
                status=health_status,
                last_check=datetime.utcnow().isoformat(),
                metrics={
                    "status": agent_db.status,
                    "session_id": agent_db.session_id,
                    "knowledge_sources_count": kb_count,
                    "created_at": agent_db.created_at.isoformat(),
                    "updated_at": agent_db.updated_at.isoformat()
                },
                issues=issues
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao verificar saúde do agente: {e}")
            raise
    
    async def archive_agent(self, agent_id: str) -> bool:
        """Arquiva um agente"""
        try:
            agent_db = self.db.query(AgentDB).filter(AgentDB.id == agent_id).first()
            
            if not agent_db:
                return False
            
            agent_db.status = "archived"
            agent_db.updated_at = datetime.utcnow()
            
            self.db.commit()
            
            logger.info(f"✅ Agente {agent_id} arquivado")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Erro ao arquivar agente: {e}")
            raise
    
    async def get_archived_agents(self) -> List[AgentResponse]:
        """Retorna agentes arquivados"""
        try:
            archived_agents = self.db.query(AgentDB).filter(AgentDB.status == "archived").all()
            
            return [
                AgentResponse(
                    id=agent.id,
                    name=agent.name,
                    description=agent.description,
                    type=AgentType(agent.type),
                    model=agent.model,
                    status=agent.status,
                    session_id=agent.session_id or ""
                )
                for agent in archived_agents
            ]
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar agentes arquivados: {e}")
            raise
    
    async def restore_agent(self, agent_id: str) -> bool:
        """Restaura um agente arquivado"""
        try:
            agent_db = self.db.query(AgentDB).filter(AgentDB.id == agent_id).first()
            
            if not agent_db or agent_db.status != "archived":
                return False
            
            agent_db.status = "active"
            agent_db.updated_at = datetime.utcnow()
            
            self.db.commit()
            
            logger.info(f"✅ Agente {agent_id} restaurado")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Erro ao restaurar agente: {e}")
            raise
