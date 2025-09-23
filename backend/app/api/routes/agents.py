"""
Rotas para gerenciamento de agentes - Implementação baseada no documento oficial do Agno
Compatível com Agno UI seguindo padrão BMAD
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict, Any
from app.schemas.agent import AgentCreate, AgentResponse, AgentDetails, MessageRequest, MessageResponse
from app.services.agno_service import AgnoService

router = APIRouter()

# Instância global do serviço Agno
_agno_service = None

def get_agno_service() -> AgnoService:
    global _agno_service
    if _agno_service is None:
        _agno_service = AgnoService()
    return _agno_service

@router.get("/", response_model=List[AgentDetails])
async def get_agents(
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna todos os agentes disponíveis - compatível com Agno UI"""
    try:
        return agno_service.get_agents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/", response_model=AgentResponse)
async def create_agent(
    agent_data: AgentCreate,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Cria um novo agente"""
    try:
        agent = await agno_service.create_agent(agent_data.session_id, agent_data)
        return agent
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna um agente específico"""
    try:
        if agent_id not in agno_service.active_agents:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        agent = agno_service.active_agents[agent_id]
        return AgentResponse(
            id=agent.id,
            name=agent.name,
            description=agent.description,
            type=agent.type,
            model=agent.model,
            status="active",
            session_id=agent.session_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/{agent_id}/runs")
async def run_agent(
    agent_id: str,
    request: Request,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Executa agente - compatível com Agno UI"""
    try:
        # Parse form data como no Agno original
        form_data = await request.form()
        session_id = form_data.get("session_id", "")
        message = form_data.get("message", "")
        stream = form_data.get("stream", "true").lower() == "true"
        
        response = await agno_service.run_agent(agent_id, session_id, message, stream)
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Remove um agente"""
    try:
        if agent_id in agno_service.active_agents:
            del agno_service.active_agents[agent_id]
            return {"message": "Agente removido com sucesso"}
        else:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
    except HTTPException:
        raise
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