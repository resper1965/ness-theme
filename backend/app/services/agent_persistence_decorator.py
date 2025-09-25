"""
Decorator para persistência transparente de agentes
NÃO modifica o AgnoService original - apenas adiciona persistência
"""

import logging
from functools import wraps
from typing import Any, Callable
from sqlalchemy.orm import Session as DBSession
from app.services.agent_persistence_service import AgentPersistenceService
from app.schemas.agent import AgentCreate, AgentUpdate

logger = logging.getLogger(__name__)

class AgentPersistenceDecorator:
    """Decorator para adicionar persistência ao AgnoService sem modificá-lo"""
    
    def __init__(self, db_session: DBSession):
        self.db_session = db_session
        self.persistence_service = AgentPersistenceService(db_session)
    
    def persist_agent_creation(self, func: Callable) -> Callable:
        """Decorator para persistir criação de agentes"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Executar método original
            result = await func(*args, **kwargs)
            
            try:
                # Persistir no banco se for criação de agente
                if hasattr(result, 'id') and hasattr(result, 'name'):
                    # Converter para AgentCreate se necessário
                    agent_data = AgentCreate(
                        id=result.id,
                        name=result.name,
                        description=result.description,
                        type=result.type,
                        model=result.model,
                        knowledge_sources=[]
                    )
                    
                    await self.persistence_service.create_agent(agent_data, result.session_id)
                    logger.info(f"✅ Agente {result.id} persistido automaticamente")
                    
            except Exception as e:
                logger.warning(f"⚠️ Falha na persistência automática: {e}")
                # Não falhar o método original por causa da persistência
            
            return result
        return wrapper
    
    def persist_agent_update(self, func: Callable) -> Callable:
        """Decorator para persistir atualizações de agentes"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Executar método original
            result = await func(*args, **kwargs)
            
            try:
                # Persistir atualização se for update de agente
                if len(args) >= 2:  # agent_id, updates
                    agent_id = args[1] if len(args) > 1 else None
                    if agent_id and hasattr(result, 'id'):
                        updates = AgentUpdate(
                            name=result.name if hasattr(result, 'name') else None,
                            description=result.description if hasattr(result, 'description') else None,
                            model=result.model if hasattr(result, 'model') else None,
                            status=result.status if hasattr(result, 'status') else None
                        )
                        
                        await self.persistence_service.update_agent(agent_id, updates)
                        logger.info(f"✅ Agente {agent_id} atualizado no banco")
                        
            except Exception as e:
                logger.warning(f"⚠️ Falha na persistência de atualização: {e}")
            
            return result
        return wrapper
    
    def persist_agent_deletion(self, func: Callable) -> Callable:
        """Decorator para persistir remoção de agentes"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Executar método original
            result = await func(*args, **kwargs)
            
            try:
                # Persistir remoção se for delete de agente
                if len(args) >= 1:  # agent_id
                    agent_id = args[0]
                    if agent_id and result:  # Se o método original retornou True
                        await self.persistence_service.delete_agent(agent_id, soft_delete=True)
                        logger.info(f"✅ Agente {agent_id} removido do banco")
                        
            except Exception as e:
                logger.warning(f"⚠️ Falha na persistência de remoção: {e}")
            
            return result
        return wrapper

# Função helper para aplicar decorators
def add_persistence_to_agno_service(agno_service_instance, db_session: DBSession):
    """
    Adiciona persistência ao AgnoService existente sem modificá-lo
    """
    decorator = AgentPersistenceDecorator(db_session)
    
    # Aplicar decorators aos métodos relevantes
    if hasattr(agno_service_instance, 'create_agent'):
        agno_service_instance.create_agent = decorator.persist_agent_creation(
            agno_service_instance.create_agent
        )
    
    if hasattr(agno_service_instance, 'update_agent'):
        agno_service_instance.update_agent = decorator.persist_agent_update(
            agno_service_instance.update_agent
        )
    
    if hasattr(agno_service_instance, 'delete_agent'):
        agno_service_instance.delete_agent = decorator.persist_agent_deletion(
            agno_service_instance.delete_agent
        )
    
    logger.info("✅ Persistência adicionada ao AgnoService via decorators")
    return agno_service_instance
