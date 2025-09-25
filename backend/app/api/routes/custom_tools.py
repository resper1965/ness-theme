"""
API para ferramentas personalizadas
Permite criar, gerenciar e executar ferramentas customizadas
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

# Store de ferramentas personalizadas (em produção seria um banco)
custom_tools_store = {}

class CustomToolCreate(BaseModel):
    name: str
    description: str
    category: str
    endpoint: str
    parameters: Dict[str, Any]
    code: str
    tags: List[str] = []

class CustomToolResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    endpoint: str
    parameters: Dict[str, Any]
    code: str
    tags: List[str]
    status: str
    created_at: str
    updated_at: str
    usage_count: int = 0

class ToolExecutionRequest(BaseModel):
    tool_id: str
    parameters: Dict[str, Any]

class ToolExecutionResponse(BaseModel):
    tool_id: str
    status: str
    result: Any
    execution_time: float
    error: Optional[str] = None

@router.post("/", response_model=CustomToolResponse)
async def create_custom_tool(tool_data: CustomToolCreate):
    """Cria uma nova ferramenta personalizada"""
    try:
        tool_id = str(uuid.uuid4())
        
        custom_tool = {
            "id": tool_id,
            "name": tool_data.name,
            "description": tool_data.description,
            "category": tool_data.category,
            "endpoint": tool_data.endpoint,
            "parameters": tool_data.parameters,
            "code": tool_data.code,
            "tags": tool_data.tags,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        custom_tools_store[tool_id] = custom_tool
        
        logger.info(f"✅ Ferramenta personalizada criada: {tool_data.name}")
        
        return CustomToolResponse(**custom_tool)
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar ferramenta: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[CustomToolResponse])
async def list_custom_tools(category: Optional[str] = None, status: Optional[str] = None):
    """Lista ferramentas personalizadas"""
    try:
        tools = list(custom_tools_store.values())
        
        # Filtrar por categoria
        if category:
            tools = [tool for tool in tools if tool["category"] == category]
        
        # Filtrar por status
        if status:
            tools = [tool for tool in tools if tool["status"] == status]
        
        return [CustomToolResponse(**tool) for tool in tools]
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar ferramentas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{tool_id}", response_model=CustomToolResponse)
async def get_custom_tool(tool_id: str):
    """Obtém uma ferramenta personalizada específica"""
    try:
        if tool_id not in custom_tools_store:
            raise HTTPException(status_code=404, detail="Ferramenta não encontrada")
        
        return CustomToolResponse(**custom_tools_store[tool_id])
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao obter ferramenta: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{tool_id}", response_model=CustomToolResponse)
async def update_custom_tool(tool_id: str, tool_data: CustomToolCreate):
    """Atualiza uma ferramenta personalizada"""
    try:
        if tool_id not in custom_tools_store:
            raise HTTPException(status_code=404, detail="Ferramenta não encontrada")
        
        # Manter dados existentes
        existing_tool = custom_tools_store[tool_id]
        
        # Atualizar dados
        updated_tool = {
            **existing_tool,
            "name": tool_data.name,
            "description": tool_data.description,
            "category": tool_data.category,
            "endpoint": tool_data.endpoint,
            "parameters": tool_data.parameters,
            "code": tool_data.code,
            "tags": tool_data.tags,
            "updated_at": datetime.now().isoformat()
        }
        
        custom_tools_store[tool_id] = updated_tool
        
        logger.info(f"✅ Ferramenta atualizada: {tool_data.name}")
        
        return CustomToolResponse(**updated_tool)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar ferramenta: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{tool_id}")
async def delete_custom_tool(tool_id: str):
    """Remove uma ferramenta personalizada"""
    try:
        if tool_id not in custom_tools_store:
            raise HTTPException(status_code=404, detail="Ferramenta não encontrada")
        
        del custom_tools_store[tool_id]
        
        logger.info(f"✅ Ferramenta removida: {tool_id}")
        
        return {"message": "Ferramenta removida com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao remover ferramenta: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute", response_model=ToolExecutionResponse)
async def execute_custom_tool(execution_request: ToolExecutionRequest):
    """Executa uma ferramenta personalizada"""
    try:
        tool_id = execution_request.tool_id
        
        if tool_id not in custom_tools_store:
            raise HTTPException(status_code=404, detail="Ferramenta não encontrada")
        
        tool = custom_tools_store[tool_id]
        
        if tool["status"] != "active":
            raise HTTPException(status_code=400, detail="Ferramenta não está ativa")
        
        # Simular execução (em produção seria executar o código real)
        start_time = datetime.now()
        
        # Aqui seria executado o código da ferramenta
        # Por enquanto, simulamos uma execução
        result = {
            "tool_name": tool["name"],
            "parameters_received": execution_request.parameters,
            "execution_status": "success",
            "message": f"Ferramenta {tool['name']} executada com sucesso"
        }
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Incrementar contador de uso
        custom_tools_store[tool_id]["usage_count"] += 1
        custom_tools_store[tool_id]["updated_at"] = datetime.now().isoformat()
        
        logger.info(f"✅ Ferramenta executada: {tool['name']} em {execution_time:.2f}s")
        
        return ToolExecutionResponse(
            tool_id=tool_id,
            status="success",
            result=result,
            execution_time=execution_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao executar ferramenta: {e}")
        return ToolExecutionResponse(
            tool_id=execution_request.tool_id,
            status="error",
            result=None,
            execution_time=0.0,
            error=str(e)
        )

@router.get("/categories/list")
async def list_categories():
    """Lista todas as categorias de ferramentas disponíveis"""
    try:
        categories = set(tool["category"] for tool in custom_tools_store.values())
        return {"categories": list(categories)}
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar categorias: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/overview")
async def get_tools_stats():
    """Retorna estatísticas das ferramentas personalizadas"""
    try:
        total_tools = len(custom_tools_store)
        active_tools = len([t for t in custom_tools_store.values() if t["status"] == "active"])
        total_usage = sum(tool["usage_count"] for tool in custom_tools_store.values())
        
        categories = {}
        for tool in custom_tools_store.values():
            category = tool["category"]
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
        
        return {
            "total_tools": total_tools,
            "active_tools": active_tools,
            "inactive_tools": total_tools - active_tools,
            "total_usage": total_usage,
            "categories": categories
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))
