"""
Serviço de vetorização SQL para RAG avançado
Converte dados SQL em embeddings vetoriais para busca semântica
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import json
from app.services.sql_service import SQLService

logger = logging.getLogger(__name__)

class VectorizedSQLService:
    """Serviço de vetorização SQL para busca semântica"""
    
    def __init__(self):
        self.sql_service = SQLService()
        # Modelo de embeddings em português
        self.embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        self.vector_store = {}  # Store local de vetores
        self.vector_dimension = 384  # Dimensão do modelo escolhido
        
    def vectorize_sql_data(self, table_name: str = "REBr_AgingDiario", limit: int = 100) -> Dict[str, Any]:
        """Vetoriza dados do SQL Server para busca semântica"""
        try:
            logger.info(f"🔍 Iniciando vetorização da tabela {table_name}")
            
            # Buscar dados do SQL
            with self.sql_service as sql:
                if not sql.connect():
                    raise Exception("Falha ao conectar com SQL Server")
                
                # Buscar dados da tabela
                query = f"SELECT TOP {limit} * FROM {table_name}"
                cursor = sql.connection.cursor()
                cursor.execute(query)
                
                columns = [column[0] for column in cursor.description]
                raw_data = []
                
                for row in cursor.fetchall():
                    row_dict = {}
                    for i, value in enumerate(row):
                        if hasattr(value, 'isoformat'):
                            row_dict[columns[i]] = value.isoformat()
                        else:
                            row_dict[columns[i]] = str(value) if value is not None else None
                    raw_data.append(row_dict)
                
                logger.info(f"📊 Dados brutos carregados: {len(raw_data)} registros")
                
                # Processar e vetorizar dados
                vectorized_data = []
                for i, record in enumerate(raw_data):
                    # Criar representação textual do registro
                    text_representation = self._create_text_representation(record)
                    
                    # Gerar embedding
                    embedding = self.embedding_model.encode(text_representation)
                    
                    vectorized_data.append({
                        "id": f"{table_name}_{i}",
                        "text": text_representation,
                        "embedding": embedding.tolist(),
                        "metadata": {
                            "table": table_name,
                            "record_id": i,
                            "original_data": record
                        }
                    })
                
                # Armazenar vetores
                self.vector_store[table_name] = vectorized_data
                
                logger.info(f"✅ Vetorização concluída: {len(vectorized_data)} registros vetorizados")
                
                return {
                    "status": "success",
                    "table_name": table_name,
                    "vectorized_count": len(vectorized_data),
                    "dimension": self.vector_dimension,
                    "model": "paraphrase-multilingual-MiniLM-L12-v2"
                }
                
        except Exception as e:
            logger.error(f"❌ Erro na vetorização: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _create_text_representation(self, record: Dict[str, Any]) -> str:
        """Cria representação textual de um registro para vetorização"""
        # Filtrar campos relevantes e criar texto descritivo
        relevant_fields = [
            'Cliente', 'Empreendimento', 'Status', 'Situacao', 
            'VendaValor', 'VendaData', 'Estado', 'Unidade'
        ]
        
        text_parts = []
        for field in relevant_fields:
            if field in record and record[field] is not None:
                text_parts.append(f"{field}: {record[field]}")
        
        # Adicionar contexto geral
        context = f"Registro imobiliário com dados de venda"
        if 'Cliente' in record:
            context += f" do cliente {record['Cliente']}"
        if 'Empreendimento' in record:
            context += f" no empreendimento {record['Empreendimento']}"
        if 'VendaValor' in record:
            context += f" com valor R$ {record['VendaValor']}"
        
        return f"{context}. {'; '.join(text_parts)}"
    
    def semantic_search(self, query: str, table_name: str = "REBr_AgingDiario", top_k: int = 5) -> List[Dict[str, Any]]:
        """Busca semântica nos dados vetorizados"""
        try:
            if table_name not in self.vector_store:
                logger.warning(f"⚠️ Tabela {table_name} não vetorizada. Vetorizando agora...")
                self.vectorize_sql_data(table_name)
            
            # Gerar embedding da query
            query_embedding = self.embedding_model.encode(query)
            
            # Calcular similaridade com todos os vetores
            similarities = []
            for item in self.vector_store[table_name]:
                similarity = self._cosine_similarity(query_embedding, item["embedding"])
                similarities.append({
                    "item": item,
                    "similarity": similarity
                })
            
            # Ordenar por similaridade
            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            
            # Retornar top_k resultados
            results = similarities[:top_k]
            
            logger.info(f"🔍 Busca semântica: {len(results)} resultados encontrados")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Erro na busca semântica: {e}")
            return []
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: List[float]) -> float:
        """Calcula similaridade de cosseno entre dois vetores"""
        vec2 = np.array(vec2)
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (norm1 * norm2)
    
    def generate_semantic_context(self, user_query: str, table_name: str = "REBr_AgingDiario") -> str:
        """Gera contexto semântico baseado na query do usuário"""
        try:
            # Busca semântica
            results = self.semantic_search(user_query, table_name, top_k=3)
            
            if not results:
                return "Não encontrei dados relevantes para sua consulta."
            
            # Gerar contexto estruturado
            context = f"Baseado na busca semântica nos dados vetorizados:\n\n"
            
            for i, result in enumerate(results, 1):
                item = result["item"]
                similarity = result["similarity"]
                
                context += f"Resultado {i} (similaridade: {similarity:.3f}):\n"
                context += f"{item['text']}\n\n"
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar contexto semântico: {e}")
            return "Erro ao processar busca semântica."
    
    def get_vector_stats(self, table_name: str = "REBr_AgingDiario") -> Dict[str, Any]:
        """Retorna estatísticas dos vetores armazenados"""
        if table_name not in self.vector_store:
            return {"status": "not_vectorized", "message": f"Tabela {table_name} não foi vetorizada"}
        
        vectors = self.vector_store[table_name]
        return {
            "status": "vectorized",
            "table_name": table_name,
            "vector_count": len(vectors),
            "dimension": self.vector_dimension,
            "model": "paraphrase-multilingual-MiniLM-L12-v2"
        }
