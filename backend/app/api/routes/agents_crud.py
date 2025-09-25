"""
Rotas CRUD para administração de agentes - Implementação baseada no documento oficial do Agno
Compatível com Agno UI seguindo padrão BMAD
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict, Any
from app.schemas.agent import (
    AgentCreate, AgentResponse, AgentDetails, MessageRequest, MessageResponse,
    AgentUpdate, AgentTemplate, AgentHealth, AgentClone
)
from app.services.agno_service import AgnoService

router = APIRouter()

# Instância global do serviço Agno
_agno_service = None

def get_agno_service() -> AgnoService:
    global _agno_service
    if _agno_service is None:
        _agno_service = AgnoService()
    return _agno_service

# ===== ROTAS CRUD PARA ADMINISTRAÇÃO =====

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    updates: AgentUpdate,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Atualiza um agente existente mantendo operacionalidade"""
    try:
        agent = await agno_service.update_agent(agent_id, updates)
        return agent
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Remove um agente (soft delete)"""
    try:
        success = await agno_service.delete_agent(agent_id)
        if success:
            return {"message": "Agente removido com sucesso", "agent_id": agent_id}
        else:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/{agent_id}/clone", response_model=AgentResponse)
async def clone_agent(
    agent_id: str,
    clone_data: AgentClone,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Clona um agente existente"""
    try:
        new_agent = await agno_service.clone_agent(agent_id, clone_data)
        return new_agent
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{agent_id}/health", response_model=AgentHealth)
async def get_agent_health(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Verifica saúde do agente"""
    try:
        health = await agno_service.get_agent_health(agent_id)
        return health
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/{agent_id}/restart")
async def restart_agent(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Reinicia um agente"""
    try:
        success = await agno_service.restart_agent(agent_id)
        if success:
            return {"message": "Agente reiniciado com sucesso", "agent_id": agent_id}
        else:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/templates", response_model=List[AgentTemplate])
async def get_agent_templates(
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna templates de agentes disponíveis"""
    try:
        templates = await agno_service.get_agent_templates()
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/from-template", response_model=AgentResponse)
async def create_agent_from_template(
    template_id: str,
    session_id: str,
    custom_name: str = None,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Cria agente a partir de template"""
    try:
        agent = await agno_service.create_agent_from_template(template_id, session_id, custom_name)
        return agent
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{agent_id}/metrics")
async def get_agent_metrics(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna métricas de performance do agente"""
    try:
        metrics = await agno_service.get_agent_metrics(agent_id)
        return metrics
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/{agent_id}/archive")
async def archive_agent(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Arquiva um agente (preserva para uso futuro)"""
    try:
        success = await agno_service.archive_agent(agent_id)
        if success:
            return {"message": "Agente arquivado com sucesso", "agent_id": agent_id}
        else:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/archived", response_model=List[AgentResponse])
async def get_archived_agents(
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna agentes arquivados"""
    try:
        agents = await agno_service.get_archived_agents()
        return agents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/{agent_id}/restore")
async def restore_agent(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Restaura um agente arquivado"""
    try:
        success = await agno_service.restore_agent(agent_id)
        if success:
            return {"message": "Agente restaurado com sucesso", "agent_id": agent_id}
        else:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
