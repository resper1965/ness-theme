"""
Módulo RAG (Retrieval-Augmented Generation)
"""

from typing import Any, Dict, List, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel

from .knowledge import KnowledgeBase, KnowledgeItem


class RAGConfig(BaseModel):
    """Configuração do RAG"""
    similarity_threshold: float = 0.1
    max_results: int = 5
    chunk_size: int = 1000
    chunk_overlap: int = 200


class RAGEngine:
    """Motor RAG para busca semântica"""
    
    def __init__(self, knowledge_base: KnowledgeBase, config: Optional[RAGConfig] = None):
        self.knowledge_base = knowledge_base
        self.config = config or RAGConfig()
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self._documents_cache: List[str] = []
        self._tfidf_matrix = None
        self._is_fitted = False
    
    async def index_documents(self):
        """Indexa documentos para busca"""
        documents = await self.knowledge_base.list_documents(limit=1000)
        
        if not documents:
            return
        
        # Extrair conteúdo dos documentos
        self._documents_cache = [doc.content for doc in documents]
        
        # Criar matriz TF-IDF
        try:
            self._tfidf_matrix = self.vectorizer.fit_transform(self._documents_cache)
            self._is_fitted = True
        except Exception as e:
            print(f"Erro ao indexar documentos: {e}")
            self._is_fitted = False
    
    async def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Busca semântica usando RAG"""
        if not self._is_fitted:
            await self.index_documents()
        
        if not self._is_fitted or not self._documents_cache:
            # Fallback para busca simples
            return await self.knowledge_base.search(query, limit=self.config.max_results)
        
        try:
            # Transformar query usando o mesmo vectorizer
            query_vector = self.vectorizer.transform([query])
            
            # Calcular similaridade
            similarities = cosine_similarity(query_vector, self._tfidf_matrix).flatten()
            
            # Obter documentos mais similares
            similar_indices = np.argsort(similarities)[::-1]
            
            results = []
            for idx in similar_indices:
                similarity = similarities[idx]
                
                if similarity < self.config.similarity_threshold:
                    break
                
                if len(results) >= self.config.max_results:
                    break
                
                # Buscar documento original
                documents = await self.knowledge_base.list_documents(limit=1000)
                if idx < len(documents):
                    doc = documents[idx]
                    
                    # Aplicar filtros se fornecidos
                    if filters:
                        match = True
                        for key, value in filters.items():
                            if doc.metadata.get(key) != value:
                                match = False
                                break
                        if not match:
                            continue
                    
                    results.append({
                        "id": doc.id,
                        "content": doc.content,
                        "source": doc.source,
                        "metadata": doc.metadata,
                        "similarity": float(similarity),
                        "timestamp": doc.timestamp.isoformat()
                    })
            
            return results
            
        except Exception as e:
            print(f"Erro na busca RAG: {e}")
            # Fallback para busca simples
            return await self.knowledge_base.search(query, limit=self.config.max_results)
    
    async def get_relevant_context(
        self,
        query: str,
        max_chars: int = 2000
    ) -> str:
        """Retorna contexto relevante formatado"""
        results = await self.search(query)
        
        if not results:
            return ""
        
        context_parts = []
        current_length = 0
        
        for result in results:
            content = result["content"]
            source = result.get("source", "Unknown")
            
            # Truncar se necessário
            if current_length + len(content) > max_chars:
                remaining = max_chars - current_length
                if remaining > 100:  # Só adicionar se sobrou espaço significativo
                    content = content[:remaining] + "..."
                else:
                    break
            
            context_parts.append(f"Fonte: {source}\n{content}\n")
            current_length += len(content)
        
        return "\n".join(context_parts)
    
    async def add_document_with_indexing(
        self,
        content: str,
        metadata: Dict[str, Any],
        source: str
    ) -> str:
        """Adiciona documento e atualiza índice"""
        doc_id = await self.knowledge_base.add_document(content, metadata, source)
        
        # Reindexar documentos
        await self.index_documents()
        
        return doc_id
