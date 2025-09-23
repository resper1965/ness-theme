"""
Módulo de Ingestão de Dados
"""

import asyncio
import aiohttp
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel

from .knowledge import KnowledgeBase, KnowledgeItem


class IngestSource(BaseModel):
    """Fonte de ingestão"""
    type: str  # "file", "url", "text", "api"
    path: Optional[str] = None
    url: Optional[str] = None
    content: Optional[str] = None
    metadata: Dict[str, Any] = {}
    filters: Dict[str, Any] = {}


class IngestResult(BaseModel):
    """Resultado da ingestão"""
    source: IngestSource
    documents_processed: int
    documents_failed: int
    errors: List[str] = []
    metadata: Dict[str, Any] = {}


class IngestEngine:
    """Motor de ingestão de dados"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.supported_types = ["text", "file", "url", "api"]
    
    async def ingest_source(self, source: IngestSource) -> IngestResult:
        """Ingere dados de uma fonte"""
        result = IngestResult(
            source=source,
            documents_processed=0,
            documents_failed=0
        )
        
        try:
            if source.type == "text":
                await self._ingest_text(source, result)
            elif source.type == "file":
                await self._ingest_file(source, result)
            elif source.type == "url":
                await self._ingest_url(source, result)
            elif source.type == "api":
                await self._ingest_api(source, result)
            else:
                result.errors.append(f"Tipo de fonte não suportado: {source.type}")
                
        except Exception as e:
            result.errors.append(f"Erro na ingestão: {str(e)}")
            result.documents_failed += 1
        
        return result
    
    async def _ingest_text(self, source: IngestSource, result: IngestResult):
        """Ingere texto direto"""
        if not source.content:
            result.errors.append("Conteúdo não fornecido para ingestão de texto")
            return
        
        try:
            doc_id = await self.knowledge_base.add_document(
                content=source.content,
                metadata={
                    **source.metadata,
                    "ingest_type": "text",
                    "ingest_timestamp": datetime.now().isoformat()
                },
                source="text_input"
            )
            result.documents_processed += 1
        except Exception as e:
            result.errors.append(f"Erro ao processar texto: {str(e)}")
            result.documents_failed += 1
    
    async def _ingest_file(self, source: IngestSource, result: IngestResult):
        """Ingere arquivo"""
        if not source.path:
            result.errors.append("Caminho do arquivo não fornecido")
            return
        
        file_path = Path(source.path)
        if not file_path.exists():
            result.errors.append(f"Arquivo não encontrado: {source.path}")
            return
        
        try:
            # Ler conteúdo do arquivo
            if file_path.suffix.lower() in ['.txt', '.md', '.rst']:
                content = file_path.read_text(encoding='utf-8')
            elif file_path.suffix.lower() in ['.json']:
                import json
                data = json.loads(file_path.read_text(encoding='utf-8'))
                content = str(data)
            else:
                result.errors.append(f"Tipo de arquivo não suportado: {file_path.suffix}")
                return
            
            # Adicionar à base de conhecimento
            doc_id = await self.knowledge_base.add_document(
                content=content,
                metadata={
                    **source.metadata,
                    "ingest_type": "file",
                    "file_path": str(file_path),
                    "file_size": file_path.stat().st_size,
                    "ingest_timestamp": datetime.now().isoformat()
                },
                source=str(file_path)
            )
            result.documents_processed += 1
            
        except Exception as e:
            result.errors.append(f"Erro ao processar arquivo {source.path}: {str(e)}")
            result.documents_failed += 1
    
    async def _ingest_url(self, source: IngestSource, result: IngestResult):
        """Ingere conteúdo de URL"""
        if not source.url:
            result.errors.append("URL não fornecida")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(source.url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        doc_id = await self.knowledge_base.add_document(
                            content=content,
                            metadata={
                                **source.metadata,
                                "ingest_type": "url",
                                "url": source.url,
                                "status_code": response.status,
                                "ingest_timestamp": datetime.now().isoformat()
                            },
                            source=source.url
                        )
                        result.documents_processed += 1
                    else:
                        result.errors.append(f"Erro HTTP {response.status} ao acessar {source.url}")
                        result.documents_failed += 1
                        
        except Exception as e:
            result.errors.append(f"Erro ao processar URL {source.url}: {str(e)}")
            result.documents_failed += 1
    
    async def _ingest_api(self, source: IngestSource, result: IngestResult):
        """Ingere dados de API"""
        if not source.url:
            result.errors.append("URL da API não fornecida")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = source.metadata.get("headers", {})
                params = source.metadata.get("params", {})
                
                async with session.get(source.url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = str(data)
                        
                        doc_id = await self.knowledge_base.add_document(
                            content=content,
                            metadata={
                                **source.metadata,
                                "ingest_type": "api",
                                "api_url": source.url,
                                "status_code": response.status,
                                "ingest_timestamp": datetime.now().isoformat()
                            },
                            source=source.url
                        )
                        result.documents_processed += 1
                    else:
                        result.errors.append(f"Erro HTTP {response.status} ao acessar API {source.url}")
                        result.documents_failed += 1
                        
        except Exception as e:
            result.errors.append(f"Erro ao processar API {source.url}: {str(e)}")
            result.documents_failed += 1
    
    async def batch_ingest(self, sources: List[IngestSource]) -> List[IngestResult]:
        """Ingere múltiplas fontes em lote"""
        tasks = [self.ingest_source(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Processar exceções
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_result = IngestResult(
                    source=sources[i],
                    documents_processed=0,
                    documents_failed=1,
                    errors=[str(result)]
                )
                processed_results.append(error_result)
            else:
                processed_results.append(result)
        
        return processed_results
