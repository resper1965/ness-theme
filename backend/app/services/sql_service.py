"""
Serviço de integração com SQL Server para RAG (Retrieval Augmented Generation)
Permite consultar o banco REB_BI_IA e usar os dados como contexto para respostas
"""

import logging
import pyodbc
import json
from typing import List, Dict, Any, Optional
from app.config.settings import get_settings

logger = logging.getLogger(__name__)

class SQLService:
    """Serviço para integração com SQL Server"""
    
    def __init__(self):
        self.settings = get_settings()
        self.connection_string = "DRIVER={FreeTDS};SERVER=gabi-sqlserver;PORT=1433;DATABASE=REB_BI_IA;UID=sa;PWD=Gabi123!;TDS_Version=8.0;"
        self.connection = None
    
    def connect(self) -> bool:
        """Estabelece conexão com o SQL Server"""
        try:
            self.connection = pyodbc.connect(self.connection_string)
            logger.info("✅ Conectado ao SQL Server REB_BI_IA")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao conectar com SQL Server: {e}")
            return False
    
    def disconnect(self):
        """Fecha conexão com o SQL Server"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("🔌 Conexão com SQL Server fechada")
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Retorna schema de uma tabela"""
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
            """
            cursor.execute(query, table_name)
            
            columns = []
            for row in cursor.fetchall():
                columns.append({
                    "name": row[0],
                    "type": row[1],
                    "nullable": row[2] == "YES",
                    "max_length": row[3]
                })
            
            return columns
        except Exception as e:
            logger.error(f"❌ Erro ao obter schema da tabela {table_name}: {e}")
            return []
    
    def search_data(self, query: str, table_name: str = "REBr_AgingDiario", limit: int = 10) -> List[Dict[str, Any]]:
        """Busca dados na tabela baseado em uma query de texto"""
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            
            # Query genérica para buscar em todas as colunas de texto
            search_query = f"""
            SELECT TOP {limit} *
            FROM {table_name}
            WHERE 
                CONCAT(CAST(ISNULL([coluna1], '') AS NVARCHAR(MAX)), 
                       CAST(ISNULL([coluna2], '') AS NVARCHAR(MAX)),
                       CAST(ISNULL([coluna3], '') AS NVARCHAR(MAX))) 
                LIKE ?
            """
            
            # Para simplificar, vamos buscar em todas as colunas
            # Primeiro, vamos ver quais colunas existem
            schema = self.get_table_schema(table_name)
            if not schema:
                return []
            
            # Construir query dinâmica baseada nas colunas disponíveis
            text_columns = [col["name"] for col in schema if col["type"] in ["varchar", "nvarchar", "text", "char", "nchar"]]
            
            if not text_columns:
                # Se não há colunas de texto, retornar primeiras linhas
                cursor.execute(f"SELECT TOP {limit} * FROM {table_name}")
            else:
                # Construir WHERE clause dinâmica
                where_conditions = []
                for col in text_columns:
                    where_conditions.append(f"CAST(ISNULL([{col}], '') AS NVARCHAR(MAX)) LIKE ?")
                
                search_query = f"""
                SELECT TOP {limit} *
                FROM {table_name}
                WHERE {' OR '.join(where_conditions)}
                """
                
                # Executar com parâmetros
                search_params = [f"%{query}%" for _ in text_columns]
                cursor.execute(search_query, search_params)
            
            # Converter resultados para dicionários
            columns = [column[0] for column in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                row_dict = {}
                for i, value in enumerate(row):
                    # Converter valores para JSON serializable
                    if hasattr(value, 'isoformat'):  # datetime
                        row_dict[columns[i]] = value.isoformat()
                    else:
                        row_dict[columns[i]] = str(value) if value is not None else None
                results.append(row_dict)
            
            logger.info(f"🔍 Encontrados {len(results)} registros para query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar dados: {e}")
            return []
    
    def get_table_info(self, table_name: str = "REBr_AgingDiario") -> Dict[str, Any]:
        """Retorna informações sobre a tabela"""
        if not self.connection:
            if not self.connect():
                return {}
        
        try:
            cursor = self.connection.cursor()
            
            # Contar total de registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            total_records = cursor.fetchone()[0]
            
            # Obter schema
            schema = self.get_table_schema(table_name)
            
            # Obter amostra de dados
            cursor.execute(f"SELECT TOP 3 * FROM {table_name}")
            sample_data = []
            columns = [column[0] for column in cursor.description]
            
            for row in cursor.fetchall():
                row_dict = {}
                for i, value in enumerate(row):
                    if hasattr(value, 'isoformat'):
                        row_dict[columns[i]] = value.isoformat()
                    else:
                        row_dict[columns[i]] = str(value) if value is not None else None
                sample_data.append(row_dict)
            
            return {
                "table_name": table_name,
                "total_records": total_records,
                "columns": schema,
                "sample_data": sample_data
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter informações da tabela: {e}")
            return {}
    
    def generate_context(self, user_query: str, table_name: str = "REBr_AgingDiario") -> str:
        """Gera contexto baseado na query do usuário e dados da tabela"""
        try:
            # Buscar dados relevantes
            search_results = self.search_data(user_query, table_name, limit=5)
            
            if not search_results:
                return "Não encontrei dados relevantes no banco para sua pergunta."
            
            # Gerar contexto estruturado
            context = f"Baseado nos dados do banco REB_BI_IA (tabela {table_name}):\n\n"
            
            for i, record in enumerate(search_results, 1):
                context += f"Registro {i}:\n"
                for key, value in record.items():
                    if value is not None:
                        context += f"  {key}: {value}\n"
                context += "\n"
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar contexto: {e}")
            return "Erro ao acessar dados do banco."
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
