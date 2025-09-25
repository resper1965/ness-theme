"""
API para analytics e métricas do sistema
Dashboard de performance, uso e monitoramento
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)
router = APIRouter()

# Store de métricas (em produção seria um banco de dados)
analytics_store = {
    "system_metrics": [],
    "agent_usage": {},
    "performance_data": [],
    "error_logs": []
}

class SystemMetrics(BaseModel):
    timestamp: str
    cpu_usage: float
    memory_usage: float
    active_connections: int
    response_time_avg: float
    requests_per_minute: int

class AgentUsageMetrics(BaseModel):
    agent_id: str
    agent_name: str
    usage_count: int
    avg_response_time: float
    success_rate: float
    last_used: str

class PerformanceData(BaseModel):
    timestamp: str
    endpoint: str
    response_time: float
    status_code: int
    user_agent: Optional[str] = None

class ErrorLog(BaseModel):
    timestamp: str
    level: str
    message: str
    component: str
    stack_trace: Optional[str] = None

@router.get("/system/health")
async def get_system_health():
    """Retorna status de saúde do sistema"""
    try:
        # Simular métricas do sistema
        current_time = datetime.now().isoformat()
        
        health_data = {
            "status": "healthy",
            "timestamp": current_time,
            "components": {
                "database": {
                    "status": "connected",
                    "response_time": "45ms"
                },
                "sql_server": {
                    "status": "connected", 
                    "response_time": "120ms"
                },
                "vector_store": {
                    "status": "active",
                    "vectorized_tables": 1
                },
                "agents": {
                    "status": "active",
                    "specialized_agents": 3,
                    "orchestrator": "active"
                }
            },
            "metrics": {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "active_sessions": 12,
                "requests_per_minute": 45
            }
        }
        
        return health_data
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter saúde do sistema: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/usage")
async def get_agent_usage_metrics():
    """Retorna métricas de uso dos agentes"""
    try:
        # Simular dados de uso dos agentes
        agent_metrics = [
            {
                "agent_id": "correlation-agent",
                "agent_name": "Analista de Correlação",
                "usage_count": 45,
                "avg_response_time": 1.2,
                "success_rate": 98.5,
                "last_used": datetime.now().isoformat()
            },
            {
                "agent_id": "portfolio-agent",
                "agent_name": "Gestor de Carteira Imobiliária",
                "usage_count": 32,
                "avg_response_time": 1.8,
                "success_rate": 96.2,
                "last_used": (datetime.now() - timedelta(minutes=15)).isoformat()
            },
            {
                "agent_id": "financial-agent",
                "agent_name": "Especialista Financeiro",
                "usage_count": 28,
                "avg_response_time": 2.1,
                "success_rate": 94.8,
                "last_used": (datetime.now() - timedelta(minutes=30)).isoformat()
            }
        ]
        
        return {
            "total_agents": len(agent_metrics),
            "total_usage": sum(agent["usage_count"] for agent in agent_metrics),
            "agents": agent_metrics
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter métricas de agentes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance/overview")
async def get_performance_overview():
    """Retorna visão geral de performance"""
    try:
        # Simular dados de performance
        performance_data = {
            "time_range": "last_24_hours",
            "summary": {
                "total_requests": 1250,
                "avg_response_time": 1.4,
                "success_rate": 97.2,
                "error_rate": 2.8
            },
            "trends": {
                "requests_trend": "increasing",
                "response_time_trend": "stable",
                "error_rate_trend": "decreasing"
            },
            "top_endpoints": [
                {"endpoint": "/chat/send-message", "requests": 450, "avg_time": 1.2},
                {"endpoint": "/sql/test-connection", "requests": 120, "avg_time": 0.8},
                {"endpoint": "/agents/", "requests": 85, "avg_time": 0.5}
            ]
        }
        
        return performance_data
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/errors/recent")
async def get_recent_errors(limit: int = 10):
    """Retorna erros recentes do sistema"""
    try:
        # Simular logs de erro
        error_logs = [
            {
                "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
                "level": "WARNING",
                "message": "SQL connection timeout",
                "component": "sql_service",
                "stack_trace": None
            },
            {
                "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
                "level": "ERROR",
                "message": "Agent selection failed",
                "component": "agno_service",
                "stack_trace": "Traceback (most recent call last)..."
            },
            {
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                "level": "INFO",
                "message": "Vector store initialized",
                "component": "vectorized_sql_service",
                "stack_trace": None
            }
        ]
        
        return {
            "total_errors": len(error_logs),
            "errors": error_logs[:limit]
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter logs de erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sql/vectorization-status")
async def get_vectorization_status():
    """Retorna status da vetorização SQL"""
    try:
        # Simular status da vetorização
        vectorization_status = {
            "status": "active",
            "vectorized_tables": [
                {
                    "table_name": "REBr_AgingDiario",
                    "vector_count": 150,
                    "dimension": 384,
                    "model": "paraphrase-multilingual-MiniLM-L12-v2",
                    "last_updated": datetime.now().isoformat()
                }
            ],
            "search_performance": {
                "avg_search_time": 0.8,
                "total_searches": 45,
                "success_rate": 98.5
            }
        }
        
        return vectorization_status
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter status de vetorização: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/summary")
async def get_dashboard_summary():
    """Retorna resumo completo para dashboard"""
    try:
        summary = {
            "timestamp": datetime.now().isoformat(),
            "system_health": {
                "status": "healthy",
                "uptime": "99.8%",
                "active_components": 4
            },
            "usage_stats": {
                "total_sessions": 25,
                "active_agents": 3,
                "sql_queries": 150,
                "vector_searches": 45
            },
            "performance": {
                "avg_response_time": 1.4,
                "success_rate": 97.2,
                "throughput": "45 req/min"
            },
            "alerts": [
                {
                    "level": "info",
                    "message": "Sistema funcionando normalmente",
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }
        
        return summary
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter resumo do dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/metrics/record")
async def record_metric(metric_data: Dict[str, Any]):
    """Registra uma nova métrica"""
    try:
        metric_data["timestamp"] = datetime.now().isoformat()
        analytics_store["system_metrics"].append(metric_data)
        
        logger.info(f"✅ Métrica registrada: {metric_data}")
        
        return {"status": "success", "message": "Métrica registrada com sucesso"}
        
    except Exception as e:
        logger.error(f"❌ Erro ao registrar métrica: {e}")
        raise HTTPException(status_code=500, detail=str(e))
