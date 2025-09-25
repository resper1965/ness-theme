"""
API para MCP (Model Context Protocol) - Ferramentas externas
Baseado no Agno Cookbook
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from app.services.mcp_service import MCPService

logger = logging.getLogger(__name__)
router = APIRouter()

class MCPServerConfig(BaseModel):
    name: str
    host: str
    port: int
    protocol: str = "http"
    api_key: Optional[str] = None

class MCPToolExecution(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]

class MCPCustomTool(BaseModel):
    name: str
    description: str
    capabilities: List[str]
    config: Dict[str, Any] = {}

@router.get("/tools")
async def get_mcp_tools():
    """Lista todas as ferramentas MCP disponíveis"""
    try:
        mcp_service = MCPService()
        tools = mcp_service.get_available_tools()
        
        return {
            "status": "success",
            "tools": tools,
            "total": len(tools)
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar ferramentas MCP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools/category/{category}")
async def get_tools_by_category(category: str):
    """Lista ferramentas MCP por categoria"""
    try:
        mcp_service = MCPService()
        tools = mcp_service.get_tools_by_category(category)
        
        return {
            "status": "success",
            "category": category,
            "tools": tools,
            "total": len(tools)
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar ferramentas por categoria: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_mcp_tools(query: str):
    """Busca ferramentas MCP por query"""
    try:
        mcp_service = MCPService()
        results = mcp_service.search_tools(query)
        
        return {
            "status": "success",
            "query": query,
            "results": results,
            "total": len(results)
        }
        
    except Exception as e:
        logger.error(f"❌ Erro na busca de ferramentas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/servers/connect")
async def connect_mcp_server(config: MCPServerConfig):
    """Conecta a um servidor MCP"""
    try:
        mcp_service = MCPService()
        server_config = {
            "host": config.host,
            "port": config.port,
            "protocol": config.protocol,
            "api_key": config.api_key
        }
        
        success = mcp_service.connect_mcp_server(config.name, server_config)
        
        if success:
            return {
                "status": "success",
                "message": f"Servidor MCP {config.name} conectado com sucesso"
            }
        else:
            raise HTTPException(status_code=400, detail="Falha ao conectar servidor MCP")
            
    except Exception as e:
        logger.error(f"❌ Erro ao conectar servidor MCP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/servers/{server_name}")
async def disconnect_mcp_server(server_name: str):
    """Desconecta de um servidor MCP"""
    try:
        mcp_service = MCPService()
        success = mcp_service.disconnect_mcp_server(server_name)
        
        if success:
            return {
                "status": "success",
                "message": f"Servidor MCP {server_name} desconectado"
            }
        else:
            raise HTTPException(status_code=404, detail="Servidor MCP não encontrado")
            
    except Exception as e:
        logger.error(f"❌ Erro ao desconectar servidor MCP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tools/execute")
async def execute_mcp_tool(execution: MCPToolExecution):
    """Executa uma ferramenta MCP"""
    try:
        mcp_service = MCPService()
        result = mcp_service.execute_mcp_tool(execution.tool_name, execution.parameters)
        
        return {
            "status": "success",
            "execution": result
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao executar ferramenta MCP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tools/custom")
async def create_custom_tool(tool: MCPCustomTool):
    """Cria uma ferramenta MCP personalizada"""
    try:
        mcp_service = MCPService()
        tool_config = {
            "name": tool.name,
            "description": tool.description,
            "capabilities": tool.capabilities,
            "config": tool.config
        }
        
        success = mcp_service.create_custom_tool(tool_config)
        
        if success:
            return {
                "status": "success",
                "message": f"Ferramenta personalizada {tool.name} criada com sucesso"
            }
        else:
            raise HTTPException(status_code=400, detail="Falha ao criar ferramenta personalizada")
            
    except Exception as e:
        logger.error(f"❌ Erro ao criar ferramenta personalizada: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_mcp_status():
    """Retorna status dos servidores MCP"""
    try:
        mcp_service = MCPService()
        status = mcp_service.get_mcp_status()
        
        return {
            "status": "success",
            "mcp_status": status
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter status MCP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_mcp_categories():
    """Lista categorias de ferramentas MCP disponíveis"""
    try:
        mcp_service = MCPService()
        categories = list(mcp_service.tool_categories.keys())
        
        return {
            "status": "success",
            "categories": categories,
            "total": len(categories)
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar categorias MCP: {e}")
        raise HTTPException(status_code=500, detail=str(e))
