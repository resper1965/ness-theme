"""
Rotas para criação dinâmica de agentes
Implementação baseada no padrão BMAD
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from app.schemas.agent import AgentCreate, AgentResponse, AgentDetails
from app.schemas.session import SessionCreate, SessionResponse
from app.services.agno_service import AgnoService
from app.models.agent import AgentType

router = APIRouter()

# Instância global do serviço Agno
_agno_service = None

def get_agno_service() -> AgnoService:
    global _agno_service
    if _agno_service is None:
        _agno_service = AgnoService()
    return _agno_service

@router.post("/create-agent", response_model=AgentResponse)
async def create_dynamic_agent(
    name: str,
    description: str,
    model: str = "gpt-4",
    agent_type: str = "agent",
    session_id: Optional[str] = None,
    knowledge_sources: Optional[List[str]] = None,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Cria um agente dinamicamente via interface"""
    try:
        # Validar tipo de agente
        if agent_type not in ["agent", "orchestrator"]:
            raise HTTPException(status_code=400, detail="Tipo de agente deve ser 'agent' ou 'orchestrator'")
        
        # Criar dados do agente
        agent_data = AgentCreate(
            id=f"agent-{name.lower().replace(' ', '-')}",
            name=name,
            description=description,
            type=AgentType.AGENT if agent_type == "agent" else AgentType.ORCHESTRATOR,
            model=model,
            knowledge_sources=knowledge_sources or []
        )
        
        # Usar sessão padrão se não especificada
        if not session_id:
            session_id = "default-session"
        
        # Criar agente
        agent = await agno_service.create_agent(session_id, agent_data)
        
        return agent
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar agente: {str(e)}")

@router.post("/create-session", response_model=SessionResponse)
async def create_dynamic_session(
    name: str,
    description: str,
    max_agents: int = 3,
    max_orchestrator: int = 1,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Cria uma sessão dinamicamente"""
    try:
        session_data = SessionCreate(
            id=f"session-{name.lower().replace(' ', '-')}",
            name=name,
            description=description,
            max_agents=max_agents,
            max_orchestrator=max_orchestrator
        )
        
        session = await agno_service.create_session(session_data)
        
        return session
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar sessão: {str(e)}")

@router.get("/available-models")
async def get_available_models():
    """Retorna modelos disponíveis para agentes"""
    return {
        "models": [
            {"id": "gpt-4", "name": "GPT-4", "description": "Modelo mais avançado da OpenAI"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Modelo rápido e eficiente"},
            {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet", "description": "Modelo da Anthropic"},
            {"id": "claude-3-haiku", "name": "Claude 3 Haiku", "description": "Modelo rápido da Anthropic"}
        ]
    }

@router.get("/agent-templates")
async def get_agent_templates():
    """Retorna templates de agentes pré-definidos"""
    return {
        "templates": [
            {
                "id": "assistant",
                "name": "Assistente Geral",
                "description": "Agente assistente para tarefas gerais",
                "model": "gpt-4",
                "type": "agent",
                "knowledge_sources": []
            },
            {
                "id": "researcher",
                "name": "Pesquisador",
                "description": "Agente especializado em pesquisa e análise",
                "model": "gpt-4",
                "type": "agent",
                "knowledge_sources": ["web", "documents"]
            },
            {
                "id": "writer",
                "name": "Escritor",
                "description": "Agente especializado em escrita e redação",
                "model": "gpt-4",
                "type": "agent",
                "knowledge_sources": ["documents", "templates"]
            },
            {
                "id": "orchestrator",
                "name": "Orquestrador",
                "description": "Agente orquestrador para coordenar outros agentes",
                "model": "gpt-4",
                "type": "orchestrator",
                "knowledge_sources": []
            }
        ]
    }

@router.post("/create-from-template")
async def create_agent_from_template(
    template_id: str,
    custom_name: Optional[str] = None,
    session_id: Optional[str] = None,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Cria agente a partir de template"""
    try:
        # Buscar template
        templates_response = await get_agent_templates()
        template = None
        for t in templates_response["templates"]:
            if t["id"] == template_id:
                template = t
                break
        
        if not template:
            raise HTTPException(status_code=404, detail="Template não encontrado")
        
        # Criar agente do template
        agent_data = AgentCreate(
            id=f"agent-{template_id}-{custom_name or template['name'].lower().replace(' ', '-')}",
            name=custom_name or template["name"],
            description=template["description"],
            type=AgentType.AGENT if template["type"] == "agent" else AgentType.ORCHESTRATOR,
            model=template["model"],
            knowledge_sources=template["knowledge_sources"]
        )
        
        # Usar sessão padrão se não especificada
        if not session_id:
            session_id = "default-session"
        
        # Criar agente
        agent = await agno_service.create_agent(session_id, agent_data)
        
        return agent
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar agente do template: {str(e)}")

@router.get("/session/{session_id}/agents")
async def get_session_agents(
    session_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna agentes de uma sessão específica"""
    try:
        agents = await agno_service.get_session_agents(session_id)
        return {"agents": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agentes: {str(e)}")

@router.delete("/agent/{agent_id}")
async def delete_agent(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Remove um agente"""
    try:
        success = await agno_service.delete_agent(agent_id)
        if not success:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        return {"message": "Agente removido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover agente: {str(e)}")
