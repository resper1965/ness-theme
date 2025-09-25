"""
Rotas para integração com SQL Server
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.services.sql_service import SQLService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/test-connection")
async def test_sql_connection():
    """Testa conexão com SQL Server"""
    try:
        with SQLService() as sql:
            if sql.connect():
                return {
                    "status": "success",
                    "message": "Conexão com SQL Server estabelecida com sucesso",
                    "database": "REB_BI_IA"
                }
            else:
                raise HTTPException(status_code=500, detail="Falha ao conectar com SQL Server")
    except Exception as e:
        logger.error(f"❌ Erro ao testar conexão SQL: {e}")
        raise HTTPException(status_code=500, detail=f"Erro de conexão: {str(e)}")

@router.get("/tables")
async def get_tables():
    """Lista tabelas disponíveis no banco"""
    try:
        with SQLService() as sql:
            if not sql.connect():
                raise HTTPException(status_code=500, detail="Falha ao conectar com SQL Server")
            
            # Buscar tabelas
            cursor = sql.connection.cursor()
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
            """)
            
            tables = [row[0] for row in cursor.fetchall()]
            
            return {
                "tables": tables,
                "count": len(tables)
            }
    except Exception as e:
        logger.error(f"❌ Erro ao listar tabelas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar tabelas: {str(e)}")

@router.get("/table/{table_name}/info")
async def get_table_info(table_name: str):
    """Retorna informações sobre uma tabela específica"""
    try:
        with SQLService() as sql:
            info = sql.get_table_info(table_name)
            return info
    except Exception as e:
        logger.error(f"❌ Erro ao obter informações da tabela {table_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter informações: {str(e)}")

@router.get("/search")
async def search_data(query: str, table_name: str = "REBr_AgingDiario", limit: int = 10):
    """Busca dados na tabela baseado em uma query"""
    try:
        with SQLService() as sql:
            results = sql.search_data(query, table_name, limit)
            return {
                "query": query,
                "table": table_name,
                "results": results,
                "count": len(results)
            }
    except Exception as e:
        logger.error(f"❌ Erro ao buscar dados: {e}")
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")

@router.get("/context")
async def generate_context(query: str, table_name: str = "REBr_AgingDiario"):
    """Gera contexto baseado em uma query"""
    try:
        with SQLService() as sql:
            context = sql.generate_context(query, table_name)
            return {
                "query": query,
                "table": table_name,
                "context": context,
                "length": len(context)
            }
    except Exception as e:
        logger.error(f"❌ Erro ao gerar contexto: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar contexto: {str(e)}")
