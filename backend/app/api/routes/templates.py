from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

@router.get("/")
async def get_agent_templates():
    """Retorna templates de agentes disponíveis"""
    try:
        # Retornar dados de teste primeiro
        return [
            {
                "id": "research-agent",
                "name": "Research Agent",
                "description": "Agente especializado em pesquisa e análise",
                "type": "agent",
                "model": "gpt-4",
                "knowledge_sources": ["rag", "website"],
                "capabilities": ["web_search", "data_analysis"],
                "is_system": False
            },
            {
                "id": "writing-agent",
                "name": "Writing Agent",
                "description": "Agente para criação de conteúdo",
                "type": "agent",
                "model": "gpt-4",
                "knowledge_sources": ["rag"],
                "capabilities": ["content_creation", "text_editing"],
                "is_system": False
            }
        ]
    except Exception as e:
        print(f"Erro ao buscar templates: {e}")  # Debug
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
