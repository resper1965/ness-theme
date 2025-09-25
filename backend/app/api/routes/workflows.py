"""
Endpoints para gerenciamento de workflows baseados na documentação do Agno
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.services.workflow_service import WorkflowService
from app.services.agno_service import get_agno_service

router = APIRouter(prefix="/workflows", tags=["workflows"])

# Schemas
class WorkflowTemplateResponse(BaseModel):
    id: str
    name: str
    description: str
    type: str
    agents: List[Dict[str, Any]]
    sequence: List[Dict[str, Any]]

class WorkflowCreateRequest(BaseModel):
    template_id: str
    session_id: str
    custom_config: Optional[Dict[str, Any]] = None

class WorkflowResponse(BaseModel):
    id: str
    template_id: str
    session_id: str
    name: str
    description: str
    type: str
    agents: List[Dict[str, Any]]
    sequence: List[Dict[str, Any]]
    status: str
    created_at: str
    custom_config: Dict[str, Any]

class WorkflowStatusUpdate(BaseModel):
    status: str

# Dependency
def get_workflow_service() -> WorkflowService:
    return WorkflowService()

@router.get("/templates", response_model=List[WorkflowTemplateResponse])
async def get_workflow_templates():
    """Retorna todos os templates de workflow disponíveis"""
    workflow_service = get_workflow_service()
    templates = workflow_service.get_workflow_templates()
    
    result = []
    for template_id, template in templates.items():
        result.append(WorkflowTemplateResponse(
            id=template_id,
            name=template["name"],
            description=template["description"],
            type=template["type"],
            agents=template["agents"],
            sequence=template["sequence"]
        ))
    
    return result

@router.get("/templates/{template_id}", response_model=WorkflowTemplateResponse)
async def get_workflow_template(template_id: str):
    """Retorna um template específico de workflow"""
    workflow_service = get_workflow_service()
    template = workflow_service.get_workflow_template(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    return WorkflowTemplateResponse(
        id=template_id,
        name=template["name"],
        description=template["description"],
        type=template["type"],
        agents=template["agents"],
        sequence=template["sequence"]
    )

@router.post("/create", response_model=WorkflowResponse)
async def create_workflow(request: WorkflowCreateRequest):
    """Cria um novo workflow a partir de um template"""
    workflow_service = get_workflow_service()
    
    try:
        workflow = workflow_service.create_workflow_from_template(
            template_id=request.template_id,
            session_id=request.session_id,
            custom_config=request.custom_config
        )
        
        return WorkflowResponse(**workflow)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[WorkflowResponse])
async def get_workflows(session_id: Optional[str] = None):
    """Retorna workflows ativos, opcionalmente filtrados por sessão"""
    workflow_service = get_workflow_service()
    workflows = workflow_service.get_active_workflows(session_id)
    
    return [WorkflowResponse(**workflow) for workflow in workflows]

@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: str):
    """Retorna um workflow específico"""
    workflow_service = get_workflow_service()
    workflow = workflow_service.get_workflow(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")
    
    return WorkflowResponse(**workflow)

@router.put("/{workflow_id}/status")
async def update_workflow_status(workflow_id: str, status_update: WorkflowStatusUpdate):
    """Atualiza o status de um workflow"""
    workflow_service = get_workflow_service()
    
    success = workflow_service.update_workflow_status(workflow_id, status_update.status)
    if not success:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")
    
    return {"message": f"Status do workflow {workflow_id} atualizado para {status_update.status}"}

@router.get("/{workflow_id}/agents")
async def get_workflow_agents(workflow_id: str):
    """Retorna os agentes de um workflow"""
    workflow_service = get_workflow_service()
    agents = workflow_service.get_workflow_agents(workflow_id)
    
    if not agents:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")
    
    return {"agents": agents}

@router.get("/{workflow_id}/sequence")
async def get_workflow_sequence(workflow_id: str):
    """Retorna a sequência de execução de um workflow"""
    workflow_service = get_workflow_service()
    sequence = workflow_service.get_workflow_sequence(workflow_id)
    
    if not sequence:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")
    
    return {"sequence": sequence}

@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Remove um workflow"""
    workflow_service = get_workflow_service()
    
    success = workflow_service.delete_workflow(workflow_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")
    
    return {"message": f"Workflow {workflow_id} removido com sucesso"}