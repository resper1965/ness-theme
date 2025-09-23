"""
Rotas para gerenciamento de workflows de agentes
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.services.agno_service import AgnoService

router = APIRouter()

class WorkflowRequest(BaseModel):
    """Schema para criação de workflow"""
    session_id: str
    task_description: str
    custom_config: Optional[Dict[str, Any]] = None

class TemplateRequest(BaseModel):
    """Schema para criação de agente por template"""
    session_id: str
    template_name: str
    custom_config: Optional[Dict[str, Any]] = None

class AgentSuggestionRequest(BaseModel):
    """Schema para sugestão de agentes"""
    task_description: str

# Dependency para obter o serviço Agno
def get_agno_service() -> AgnoService:
    return AgnoService()

@router.post("/create-workflow")
async def create_agent_workflow(
    workflow_data: WorkflowRequest,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Cria workflow de agentes baseado na descrição da tarefa"""
    try:
        agents = await agno_service.create_agent_workflow(
            workflow_data.session_id,
            workflow_data.task_description
        )
        return {
            "message": "Workflow criado com sucesso",
            "agents": agents,
            "task_description": workflow_data.task_description
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/create-from-template")
async def create_agent_from_template(
    template_data: TemplateRequest,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Cria agente a partir de template"""
    try:
        agent = await agno_service.create_agent_from_template(
            template_data.session_id,
            template_data.template_name,
            template_data.custom_config
        )
        return {
            "message": "Agente criado com sucesso",
            "agent": agent,
            "template": template_data.template_name
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/templates")
async def get_available_templates(
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna templates de agentes disponíveis"""
    try:
        templates = agno_service.agent_manager.get_available_templates()
        return {
            "templates": templates,
            "count": len(templates)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/suggest-agents")
async def suggest_agent_combination(
    suggestion_data: AgentSuggestionRequest,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Sugere combinação de agentes baseada na tarefa"""
    try:
        suggestions = agno_service.agent_manager.suggest_agent_combination(
            suggestion_data.task_description
        )
        return {
            "suggestions": suggestions,
            "task_description": suggestion_data.task_description,
            "count": len(suggestions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/templates/{template_name}/capabilities")
async def get_template_capabilities(
    template_name: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna capacidades de um template"""
    try:
        capabilities = agno_service.agent_manager.get_agent_capabilities(template_name)
        return {
            "template": template_name,
            "capabilities": capabilities,
            "count": len(capabilities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/performance/{agent_id}")
async def get_agent_performance(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna métricas de performance de um agente"""
    try:
        metrics = agno_service.agent_manager.get_agent_performance_metrics(agent_id)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
