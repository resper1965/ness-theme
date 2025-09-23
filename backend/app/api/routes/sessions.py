"""
Rotas para gerenciamento de sessões - Implementação baseada no documento oficial do Agno
Compatível com Agno UI seguindo padrão BMAD
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.schemas.session import SessionCreate, SessionResponse, Sessions
from app.services.agno_service import AgnoService

router = APIRouter()

# Instância global do serviço Agno
_agno_service = None

def get_agno_service() -> AgnoService:
    global _agno_service
    if _agno_service is None:
        _agno_service = AgnoService()
    return _agno_service

@router.get("/", response_model=Sessions)
async def get_sessions(
    type: str = Query("agent", description="Tipo de sessão"),
    component_id: str = Query("", description="ID do componente"),
    db_id: str = Query("", description="ID do banco de dados"),
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna todas as sessões ativas - compatível com Agno UI"""
    try:
        return agno_service.get_sessions(type, component_id, db_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/", response_model=SessionResponse)
async def create_session(
    session_data: SessionCreate,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Cria uma nova sessão de chat"""
    try:
        session = await agno_service.create_session(session_data)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{session_id}/runs")
async def get_session_runs(
    session_id: str,
    type: str = Query("agent", description="Tipo de sessão"),
    db_id: Optional[str] = Query(None, description="ID do banco de dados"),
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna runs de uma sessão - compatível com Agno UI"""
    try:
        runs = agno_service.get_session_runs(session_id)
        return {"data": runs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna uma sessão específica"""
    try:
        if session_id not in agno_service.active_sessions:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")
        
        session = agno_service.active_sessions[session_id]
        return SessionResponse(
            id=session.id,
            name=session.name,
            description=session.description,
            status="active",
            agents_count=len(session.agent_ids),
            orchestrator_count=1 if any(agent_id in agno_service.active_agents and 
                                      agno_service.active_agents[agent_id].type.value == "orchestrator" 
                                      for agent_id in session.agent_ids) else 0
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    db_id: Optional[str] = Query(None, description="ID do banco de dados"),
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Remove uma sessão - compatível com Agno UI"""
    try:
        success = await agno_service.end_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")
        
        return {"message": "Sessão removida com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")