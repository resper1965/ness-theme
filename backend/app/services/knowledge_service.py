"""
Serviço de gerenciamento de bases de conhecimento
Implementa múltiplas fontes: RAG, sites, documentos, MCP
"""

import logging
from typing import List, Dict, Optional, Any, Union
from app.models.agent import KnowledgeSource
from app.config.settings import get_settings
import uuid
import json

logger = logging.getLogger(__name__)

class KnowledgeService:
    """Serviço de gerenciamento de bases de conhecimento"""
    
    def __init__(self):
        self.settings = get_settings()
        self.knowledge_sources: Dict[str, KnowledgeSource] = {}
        self.rag_embeddings = {}  # Cache de embeddings
        self.document_store = {}  # Store de documentos
    
    async def create_rag_source(self, name: str, documents: List[Dict[str, Any]], config: Optional[Dict[str, Any]] = None) -> KnowledgeSource:
        """Cria fonte de conhecimento RAG"""
        try:
            source_id = str(uuid.uuid4())
            config = config or {}
            
            # Configurações padrão para RAG
            rag_config = {
                "type": "rag",
                "embedding_model": config.get("embedding_model", "text-embedding-ada-002"),
                "chunk_size": config.get("chunk_size", 1000),
                "chunk_overlap": config.get("chunk_overlap", 200),
                "similarity_threshold": config.get("similarity_threshold", 0.7),
                "max_results": config.get("max_results", 5),
                "documents_count": len(documents)
            }
            
            # Processar documentos
            processed_docs = await self._process_documents(documents, rag_config)
            
            source = KnowledgeSource(
                id=source_id,
                name=name,
                type="rag",
                config=rag_config,
                status="active"
            )
            
            self.knowledge_sources[source_id] = source
            self.document_store[source_id] = processed_docs
            
            logger.info(f"✅ Fonte RAG criada: {name} com {len(documents)} documentos")
            return source
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar fonte RAG: {e}")
            raise
    
    async def create_website_source(self, name: str, urls: List[str], config: Optional[Dict[str, Any]] = None) -> KnowledgeSource:
        """Cria fonte de conhecimento de website"""
        try:
            source_id = str(uuid.uuid4())
            config = config or {}
            
            # Configurações para website
            website_config = {
                "type": "website",
                "urls": urls,
                "crawl_depth": config.get("crawl_depth", 2),
                "respect_robots": config.get("respect_robots", True),
                "extract_text": config.get("extract_text", True),
                "follow_links": config.get("follow_links", True),
                "max_pages": config.get("max_pages", 100)
            }
            
            source = KnowledgeSource(
                id=source_id,
                name=name,
                type="website",
                config=website_config,
                status="active"
            )
            
            self.knowledge_sources[source_id] = source
            
            logger.info(f"✅ Fonte Website criada: {name} com {len(urls)} URLs")
            return source
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar fonte Website: {e}")
            raise
    
    async def create_document_source(self, name: str, file_paths: List[str], config: Optional[Dict[str, Any]] = None) -> KnowledgeSource:
        """Cria fonte de conhecimento de documentos"""
        try:
            source_id = str(uuid.uuid4())
            config = config or {}
            
            # Configurações para documentos
            doc_config = {
                "type": "document",
                "file_paths": file_paths,
                "supported_formats": config.get("supported_formats", ["pdf", "txt", "docx", "md"]),
                "extract_images": config.get("extract_images", False),
                "ocr_enabled": config.get("ocr_enabled", False),
                "chunk_size": config.get("chunk_size", 1000)
            }
            
            source = KnowledgeSource(
                id=source_id,
                name=name,
                type="document",
                config=doc_config,
                status="active"
            )
            
            self.knowledge_sources[source_id] = source
            
            logger.info(f"✅ Fonte Document criada: {name} com {len(file_paths)} arquivos")
            return source
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar fonte Document: {e}")
            raise
    
    async def create_mcp_source(self, name: str, mcp_config: Dict[str, Any]) -> KnowledgeSource:
        """Cria fonte de conhecimento MCP (Model Context Protocol)"""
        try:
            source_id = str(uuid.uuid4())
            
            # Configurações para MCP
            mcp_source_config = {
                "type": "mcp",
                "server_url": mcp_config.get("server_url"),
                "api_key": mcp_config.get("api_key"),
                "capabilities": mcp_config.get("capabilities", []),
                "tools": mcp_config.get("tools", []),
                "context_window": mcp_config.get("context_window", 4000)
            }
            
            source = KnowledgeSource(
                id=source_id,
                name=name,
                type="mcp",
                config=mcp_source_config,
                status="active"
            )
            
            self.knowledge_sources[source_id] = source
            
            logger.info(f"✅ Fonte MCP criada: {name}")
            return source
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar fonte MCP: {e}")
            raise
    
    async def search_knowledge(self, query: str, source_ids: Optional[List[str]] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Busca em bases de conhecimento"""
        try:
            results = []
            
            # Se não especificadas, buscar em todas as fontes ativas
            if not source_ids:
                source_ids = [sid for sid, source in self.knowledge_sources.items() if source.status == "active"]
            
            for source_id in source_ids:
                if source_id not in self.knowledge_sources:
                    continue
                
                source = self.knowledge_sources[source_id]
                
                # Buscar baseado no tipo de fonte
                if source.type == "rag":
                    source_results = await self._search_rag(query, source, limit)
                elif source.type == "website":
                    source_results = await self._search_website(query, source, limit)
                elif source.type == "document":
                    source_results = await self._search_documents(query, source, limit)
                elif source.type == "mcp":
                    source_results = await self._search_mcp(query, source, limit)
                else:
                    continue
                
                results.extend(source_results)
            
            # Ordenar por relevância e limitar resultados
            results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)[:limit]
            
            logger.info(f"✅ Busca realizada: {len(results)} resultados para '{query}'")
            return results
            
        except Exception as e:
            logger.error(f"❌ Erro na busca de conhecimento: {e}")
            raise
    
    async def _process_documents(self, documents: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Processa documentos para RAG"""
        processed = []
        
        for doc in documents:
            # Simular processamento de documentos
            processed_doc = {
                "id": str(uuid.uuid4()),
                "content": doc.get("content", ""),
                "metadata": doc.get("metadata", {}),
                "chunks": self._chunk_text(doc.get("content", ""), config["chunk_size"], config["chunk_overlap"])
            }
            processed.append(processed_doc)
        
        return processed
    
    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Divide texto em chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
            
            if start >= len(text):
                break
        
        return chunks
    
    async def _search_rag(self, query: str, source: KnowledgeSource, limit: int) -> List[Dict[str, Any]]:
        """Busca em fonte RAG"""
        # Simular busca RAG
        results = []
        if source.id in self.document_store:
            docs = self.document_store[source.id]
            for doc in docs[:limit]:
                results.append({
                    "content": doc["content"][:500] + "...",
                    "source": source.name,
                    "type": "rag",
                    "score": 0.8,  # Simular score de relevância
                    "metadata": doc["metadata"]
                })
        
        return results
    
    async def _search_website(self, query: str, source: KnowledgeSource, limit: int) -> List[Dict[str, Any]]:
        """Busca em fonte Website"""
        # Simular busca em website
        results = []
        urls = source.config.get("urls", [])
        
        for url in urls[:limit]:
            results.append({
                "content": f"Conteúdo encontrado em {url} para '{query}'",
                "source": source.name,
                "type": "website",
                "score": 0.7,
                "metadata": {"url": url}
            })
        
        return results
    
    async def _search_documents(self, query: str, source: KnowledgeSource, limit: int) -> List[Dict[str, Any]]:
        """Busca em fonte Document"""
        # Simular busca em documentos
        results = []
        file_paths = source.config.get("file_paths", [])
        
        for file_path in file_paths[:limit]:
            results.append({
                "content": f"Conteúdo encontrado em {file_path} para '{query}'",
                "source": source.name,
                "type": "document",
                "score": 0.6,
                "metadata": {"file_path": file_path}
            })
        
        return results
    
    async def _search_mcp(self, query: str, source: KnowledgeSource, limit: int) -> List[Dict[str, Any]]:
        """Busca em fonte MCP"""
        # Simular busca MCP
        results = []
        
        # Simular resposta do MCP server
        results.append({
            "content": f"Resposta MCP para '{query}'",
            "source": source.name,
            "type": "mcp",
            "score": 0.9,
            "metadata": {"mcp_server": source.config.get("server_url")}
        })
        
        return results
    
    async def sync_knowledge_source(self, source_id: str) -> bool:
        """Sincroniza uma fonte de conhecimento"""
        try:
            if source_id not in self.knowledge_sources:
                return False
            
            source = self.knowledge_sources[source_id]
            
            # Implementar sincronização baseada no tipo
            if source.type == "website":
                # Sincronizar website
                pass
            elif source.type == "document":
                # Sincronizar documentos
                pass
            elif source.type == "mcp":
                # Sincronizar MCP
                pass
            
            logger.info(f"✅ Fonte sincronizada: {source.name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao sincronizar fonte: {e}")
            return False
    
    def get_knowledge_sources(self) -> List[KnowledgeSource]:
        """Retorna todas as fontes de conhecimento"""
        return list(self.knowledge_sources.values())
    
    def get_source_by_id(self, source_id: str) -> Optional[KnowledgeSource]:
        """Retorna fonte por ID"""
        return self.knowledge_sources.get(source_id)
    
    async def delete_knowledge_source(self, source_id: str) -> bool:
        """Remove fonte de conhecimento"""
        try:
            if source_id in self.knowledge_sources:
                del self.knowledge_sources[source_id]
                if source_id in self.document_store:
                    del self.document_store[source_id]
                logger.info(f"✅ Fonte removida: {source_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Erro ao remover fonte: {e}")
            return False
