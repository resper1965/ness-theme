"""
Rotas para gerenciamento de teams/workflows - Implementação baseada no documento oficial do Agno
Compatível com Agno UI seguindo padrão BMAD
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict, Any
from app.services.agno_service import AgnoService

router = APIRouter()

# Instância global do serviço Agno
_agno_service = None

def get_agno_service() -> AgnoService:
    global _agno_service
    if _agno_service is None:
        _agno_service = AgnoService()
    return _agno_service

@router.get("/", response_model=List[Dict[str, Any]])
async def get_teams(
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna todos os teams disponíveis - compatível com Agno UI"""
    try:
        return agno_service.get_teams()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/{team_id}/runs")
async def run_team(
    team_id: str,
    request: Request,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Executa team - compatível com Agno UI"""
    try:
        # Parse form data como no Agno original
        form_data = await request.form()
        session_id = form_data.get("session_id", "")
        message = form_data.get("message", "")
        stream = form_data.get("stream", "true").lower() == "true"
        
        # Por enquanto, simular execução de team
        response = {
            "run_id": f"team-run-{team_id}",
            "team_id": team_id,
            "session_id": session_id,
            "status": "RUNNING",
            "message": f"Team {team_id} processando: {message}",
        }
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{team_id}/sessions/{session_id}")
async def delete_team_session(
    team_id: str,
    session_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Remove uma sessão de team - compatível com Agno UI"""
    try:
        # Por enquanto, simular remoção
        return {"message": f"Sessão {session_id} do team {team_id} removida com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")