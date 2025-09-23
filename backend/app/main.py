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
from app.api.routes import agents, sessions, knowledge, workflows
from app.database.connection import get_database
from app.agno import Agent, OpenAIModel, InMemoryStorage, InMemoryKnowledgeBase, IngestEngine, RAGEngine
from app.agno.agent import AgentConfig
from app.agno.knowledge import IngestSource

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

# Inicialização do sistema Agno
agno_memory = InMemoryStorage()
agno_knowledge = InMemoryKnowledgeBase(name="gabi_kb", description="Base de conhecimento do Gabi")
agno_rag = RAGEngine(agno_knowledge)
agno_ingest = IngestEngine(agno_knowledge)

@app.on_event("startup")
async def startup_event():
    """Inicialização do backend"""
    logger.info("🚀 Iniciando Gabi Backend...")
    
    # Conectar ao banco de dados
    await get_database()
    
    # Inicializar sistema Agno
    await agno_knowledge.add_document(
        content="Sistema Gabi inicializado com sucesso. Base de conhecimento ativa.",
        metadata={"type": "system", "status": "initialized"},
        source="system"
    )
    
    logger.info("✅ Gabi Backend iniciado com sucesso!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup do backend"""
    logger.info("🛑 Finalizando Gabi Backend...")
    logger.info("✅ Sistema Agno finalizado com sucesso!")
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

# Incluir rotas
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])
app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["knowledge"])
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["workflows"])

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
