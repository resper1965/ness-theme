"""
Gabi Backend - Chat Multi-Agentes com Agno SDK
Baseado no padrão BMAD para estruturação dinâmica de agentes
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from typing import List, Optional
import logging

from app.config.settings import get_settings
from app.api.routes import agents, sessions, knowledge, workflows, agents_crud, ingestion, templates, agno_status, agent_creation, chat, sql, custom_tools, analytics, mcp
from app.database.connection import get_database

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialização do FastAPI
app = FastAPI(
    title="Gabi API",
    description="Chat Multi-Agentes com tecnologia Agno SDK",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurações
settings = get_settings()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização do sistema Agno será feita no startup

@app.on_event("startup")
async def startup_event():
    """Inicialização do backend"""
    logger.info("🚀 Iniciando Gabi Backend...")
    
    # Conectar ao banco de dados
    await get_database()
    
    # Inicializar sistema Agno
    from app.services.agno_service import AgnoService
    global agno_service
    agno_service = AgnoService()
    await agno_service.initialize()
    
    logger.info("✅ Gabi Backend iniciado com sucesso!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup do backend"""
    logger.info("🛑 Finalizando Gabi Backend...")
    if 'agno_service' in globals():
        await agno_service.cleanup()
    logger.info("✅ Gabi Backend finalizado!")

# Health check
@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "service": "gabi-backend",
        "version": "1.0.0"
    }

# Rotas compatíveis com Agno UI (sem prefixo /api/v1)
logger.info("🔗 Registrando rotas...")
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(agents_crud.router, prefix="/agents", tags=["agents-crud"])
app.include_router(templates.router, prefix="/agents", tags=["templates"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
app.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
app.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
app.include_router(agno_status.router, prefix="/agno", tags=["agno-status"])
app.include_router(agent_creation.router, prefix="/dynamic", tags=["agent-creation"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(sql.router, prefix="/sql", tags=["sql"])
app.include_router(custom_tools.router, prefix="/tools", tags=["custom-tools"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(mcp.router, prefix="/mcp", tags=["mcp"])
logger.info("✅ Rotas registradas com sucesso!")

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Erro não tratado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Erro interno do servidor", "status_code": 500}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False
    )
