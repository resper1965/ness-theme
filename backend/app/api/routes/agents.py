"""
Rotas para gerenciamento de agentes
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate
from app.schemas.session import MessageRequest, MessageResponse
from app.services.agno_service import AgnoService

router = APIRouter()

# Dependency para obter o serviço Agno
def get_agno_service() -> AgnoService:
    return AgnoService()

@router.post("/", response_model=AgentResponse)
async def create_agent(
    session_id: str,
    agent_data: AgentCreate,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Cria um novo agente na sessão"""
    try:
        agent = await agno_service.create_agent(session_id, agent_data)
        return agent
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/session/{session_id}", response_model=List[AgentResponse])
async def get_session_agents(
    session_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna todos os agentes de uma sessão"""
    try:
        agents = await agno_service.get_session_agents(session_id)
        return agents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna um agente específico"""
    try:
        # Implementar busca de agente específico
        raise HTTPException(status_code=501, detail="Funcionalidade em desenvolvimento")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Atualiza um agente"""
    try:
        # Implementar atualização de agente
        raise HTTPException(status_code=501, detail="Funcionalidade em desenvolvimento")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Remove um agente"""
    try:
        # Implementar remoção de agente
        raise HTTPException(status_code=501, detail="Funcionalidade em desenvolvimento")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/message", response_model=MessageResponse)
async def send_message(
    message_data: MessageRequest,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Envia mensagem para os agentes da sessão"""
    try:
        response = await agno_service.process_message(
            message_data.session_id, 
            message_data.message
        )
        return MessageResponse(**response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
