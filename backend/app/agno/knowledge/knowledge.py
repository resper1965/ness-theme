"""
Sistema de Base de Conhecimento
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class KnowledgeItem(BaseModel):
    """Item de conhecimento"""
    id: str
    source: str
    content: str
    metadata: Dict[str, Any] = {}
    embedding: Optional[List[float]] = None
    timestamp: datetime
    tags: List[str] = []


class KnowledgeBase(BaseModel, ABC):
    """Classe base para base de conhecimento"""
    
    name: str
    description: str = ""
    
    @abstractmethod
    async def search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Busca na base de conhecimento"""
        pass
    
    @abstractmethod
    async def add_document(
        self,
        content: str,
        metadata: Dict[str, Any],
        source: str
    ) -> str:
        """Adiciona documento à base de conhecimento"""
        pass
    
    @abstractmethod
    async def get_document(self, document_id: str) -> Optional[KnowledgeItem]:
        """Retorna documento por ID"""
        pass
    
    @abstractmethod
    async def delete_document(self, document_id: str) -> bool:
        """Remove documento da base de conhecimento"""
        pass
    
    @abstractmethod
    async def list_documents(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[KnowledgeItem]:
        """Lista documentos da base de conhecimento"""
        pass


class InMemoryKnowledgeBase(KnowledgeBase):
    """Base de conhecimento em memória (para desenvolvimento)"""
    
    def __init__(self, name: str, description: str = ""):
        super().__init__(name=name, description=description)
        self._documents: Dict[str, KnowledgeItem] = {}
        self._index: List[tuple] = []  # (query_terms, document_id)
    
    async def search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Busca simples por palavras-chave"""
        query_terms = query.lower().split()
        results = []
        
        for doc_id, doc in self._documents.items():
            score = 0
            content_lower = doc.content.lower()
            
            # Calcular score baseado em correspondências
            for term in query_terms:
                if term in content_lower:
                    score += content_lower.count(term)
            
            if score > 0:
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
                    "id": doc_id,
                    "content": doc.content,
                    "source": doc.source,
                    "metadata": doc.metadata,
                    "score": score,
                    "timestamp": doc.timestamp.isoformat()
                })
        
        # Ordenar por score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    async def add_document(
        self,
        content: str,
        metadata: Dict[str, Any],
        source: str
    ) -> str:
        """Adiciona documento à base de conhecimento"""
        from uuid import uuid4
        
        doc_id = str(uuid4())
        doc = KnowledgeItem(
            id=doc_id,
            source=source,
            content=content,
            metadata=metadata,
            timestamp=datetime.now()
        )
        
        self._documents[doc_id] = doc
        return doc_id
    
    async def get_document(self, document_id: str) -> Optional[KnowledgeItem]:
        """Retorna documento por ID"""
        return self._documents.get(document_id)
    
    async def delete_document(self, document_id: str) -> bool:
        """Remove documento da base de conhecimento"""
        if document_id in self._documents:
            del self._documents[document_id]
            return True
        return False
    
    async def list_documents(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[KnowledgeItem]:
        """Lista documentos da base de conhecimento"""
        docs = list(self._documents.values())
        docs.sort(key=lambda x: x.timestamp, reverse=True)
        return docs[offset:offset + limit]
