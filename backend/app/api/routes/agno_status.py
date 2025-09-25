"""
Rotas para verificar status do Agno SDK
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.services.agno_service import AgnoService

router = APIRouter()

# Instância global do serviço Agno
_agno_service = None

def get_agno_service() -> AgnoService:
    global _agno_service
    if _agno_service is None:
        _agno_service = AgnoService()
    return _agno_service

@router.get("/status")
async def get_agno_status(agno_service: AgnoService = Depends(get_agno_service)):
    """Retorna status do Agno SDK"""
    try:
        status = agno_service.agno_sdk_service.get_agno_status()
        return {
            "agno_sdk": status,
            "backend": {
                "status": "healthy",
                "agents_count": len(agno_service.active_agents),
                "sessions_count": len(agno_service.active_sessions)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar status: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check simples"""
    return {"status": "healthy", "service": "agno-status"}
