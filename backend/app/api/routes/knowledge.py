"""
Rotas para gerenciamento de bases de conhecimento - Implementação baseada no documento oficial do Agno
Compatível com Agno UI seguindo padrão BMAD
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.services.knowledge_service import KnowledgeService

router = APIRouter()

class KnowledgeSourceCreate(BaseModel):
    """Schema para criação de fonte de conhecimento"""
    name: str
    type: str  # "rag", "website", "document", "mcp"
    config: Dict[str, Any]

class KnowledgeSourceResponse(BaseModel):
    """Schema de resposta de fonte de conhecimento"""
    id: str
    name: str
    type: str
    status: str
    config: Dict[str, Any]

class RAGSourceCreate(BaseModel):
    """Schema para criação de fonte RAG"""
    name: str
    documents: List[Dict[str, Any]]
    config: Optional[Dict[str, Any]] = None

class WebsiteSourceCreate(BaseModel):
    """Schema para criação de fonte Website"""
    name: str
    urls: List[str]
    config: Optional[Dict[str, Any]] = None

class DocumentSourceCreate(BaseModel):
    """Schema para criação de fonte Document"""
    name: str
    file_paths: List[str]
    config: Optional[Dict[str, Any]] = None

class MCPSourceCreate(BaseModel):
    """Schema para criação de fonte MCP"""
    name: str
    server_url: str
    api_key: str
    capabilities: List[str] = []
    tools: List[str] = []

class KnowledgeSearchRequest(BaseModel):
    """Schema para busca de conhecimento"""
    query: str
    source_ids: Optional[List[str]] = None
    limit: int = 5

# Dependency para obter o serviço de conhecimento
def get_knowledge_service() -> KnowledgeService:
    return KnowledgeService()

@router.post("/sources/rag", response_model=KnowledgeSourceResponse)
async def create_rag_source(
    source_data: RAGSourceCreate,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """Cria uma nova fonte de conhecimento RAG"""
    try:
        source = await knowledge_service.create_rag_source(
            source_data.name,
            source_data.documents,
            source_data.config
        )
        return KnowledgeSourceResponse(
            id=source.id,
            name=source.name,
            type=source.type,
            status=source.status,
            config=source.config
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/sources/website", response_model=KnowledgeSourceResponse)
async def create_website_source(
    source_data: WebsiteSourceCreate,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """Cria uma nova fonte de conhecimento Website"""
    try:
        source = await knowledge_service.create_website_source(
            source_data.name,
            source_data.urls,
            source_data.config
        )
        return KnowledgeSourceResponse(
            id=source.id,
            name=source.name,
            type=source.type,
            status=source.status,
            config=source.config
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/sources/document", response_model=KnowledgeSourceResponse)
async def create_document_source(
    source_data: DocumentSourceCreate,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """Cria uma nova fonte de conhecimento Document"""
    try:
        source = await knowledge_service.create_document_source(
            source_data.name,
            source_data.file_paths,
            source_data.config
        )
        return KnowledgeSourceResponse(
            id=source.id,
            name=source.name,
            type=source.type,
            status=source.status,
            config=source.config
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/sources/mcp", response_model=KnowledgeSourceResponse)
async def create_mcp_source(
    source_data: MCPSourceCreate,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """Cria uma nova fonte de conhecimento MCP"""
    try:
        mcp_config = {
            "server_url": source_data.server_url,
            "api_key": source_data.api_key,
            "capabilities": source_data.capabilities,
            "tools": source_data.tools
        }
        
        source = await knowledge_service.create_mcp_source(
            source_data.name,
            mcp_config
        )
        return KnowledgeSourceResponse(
            id=source.id,
            name=source.name,
            type=source.type,
            status=source.status,
            config=source.config
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/search")
async def search_knowledge(
    search_data: KnowledgeSearchRequest,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """Busca em bases de conhecimento"""
    try:
        results = await knowledge_service.search_knowledge(
            search_data.query,
            search_data.source_ids,
            search_data.limit
        )
        return {
            "query": search_data.query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/sources", response_model=List[KnowledgeSourceResponse])
async def get_knowledge_sources(
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """Retorna todas as fontes de conhecimento"""
    try:
        sources = knowledge_service.get_knowledge_sources()
        return [
            KnowledgeSourceResponse(
                id=source.id,
                name=source.name,
                type=source.type,
                status=source.status,
                config=source.config
            )
            for source in sources
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/sources/{source_id}", response_model=KnowledgeSourceResponse)
async def get_knowledge_source(
    source_id: str,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """Retorna uma fonte de conhecimento específica"""
    try:
        source = knowledge_service.get_source_by_id(source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Fonte não encontrada")
        
        return KnowledgeSourceResponse(
            id=source.id,
            name=source.name,
            type=source.type,
            status=source.status,
            config=source.config
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/sources/{source_id}")
async def delete_knowledge_source(
    source_id: str,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """Remove uma fonte de conhecimento"""
    try:
        success = await knowledge_service.delete_knowledge_source(source_id)
        if not success:
            raise HTTPException(status_code=404, detail="Fonte não encontrada")
        
        return {"message": "Fonte removida com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/sources/{source_id}/sync")
async def sync_knowledge_source(
    source_id: str,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """Sincroniza uma fonte de conhecimento"""
    try:
        success = await knowledge_service.sync_knowledge_source(source_id)
        if not success:
            raise HTTPException(status_code=404, detail="Fonte não encontrada")
        
        return {"message": "Fonte sincronizada com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
