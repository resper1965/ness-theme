"""
Rotas para gerenciamento de sessões
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.session import SessionCreate, SessionResponse, SessionUpdate
from app.services.agno_service import AgnoService

router = APIRouter()

# Dependency para obter o serviço Agno
def get_agno_service() -> AgnoService:
    return AgnoService()

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

@router.get("/", response_model=List[SessionResponse])
async def get_sessions(
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna todas as sessões ativas"""
    try:
        # Implementar listagem de sessões
        sessions = []
        for session in agno_service.active_sessions.values():
            sessions.append(SessionResponse(
                id=session.id,
                name=session.name,
                description=session.description,
                status=session.status,
                agents_count=session.agents_count,
                orchestrator_count=session.orchestrator_count
            ))
        return sessions
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
            status=session.status,
            agents_count=session.agents_count,
            orchestrator_count=session.orchestrator_count
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    session_data: SessionUpdate,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Atualiza uma sessão"""
    try:
        if session_id not in agno_service.active_sessions:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")
        
        session = agno_service.active_sessions[session_id]
        
        if session_data.name is not None:
            session.name = session_data.name
        if session_data.description is not None:
            session.description = session_data.description
        
        return SessionResponse(
            id=session.id,
            name=session.name,
            description=session.description,
            status=session.status,
            agents_count=session.agents_count,
            orchestrator_count=session.orchestrator_count
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Remove uma sessão"""
    try:
        success = await agno_service.end_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")
        
        return {"message": "Sessão removida com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
