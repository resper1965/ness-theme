"""
Serviço para upload e processamento de documentos como fonte de conhecimento
Suporte a PDF, DOCX, TXT, MD e outros formatos
"""

import logging
import os
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
import mimetypes
from pathlib import Path

# Dependências para processamento de documentos
try:
    import PyPDF2
    import docx
    import markdown
    from bs4 import BeautifulSoup
except ImportError:
    # Instalar dependências se não estiverem disponíveis
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2", "python-docx", "markdown", "beautifulsoup4"])
    import PyPDF2
    import docx
    import markdown
    from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class DocumentService:
    """Serviço para processamento de documentos como fonte de conhecimento"""
    
    def __init__(self):
        self.upload_dir = Path("/app/data/documents")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Tipos de arquivo suportados
        self.supported_types = {
            'application/pdf': self._extract_pdf,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': self._extract_docx,
            'text/plain': self._extract_txt,
            'text/markdown': self._extract_markdown,
            'text/html': self._extract_html
        }
    
    def upload_document(self, file_content: bytes, filename: str, description: str = "") -> Dict[str, Any]:
        """Upload e processamento de documento"""
        try:
            # Gerar ID único para o documento
            doc_id = str(uuid.uuid4())
            
            # Determinar tipo MIME
            mime_type, _ = mimetypes.guess_type(filename)
            if not mime_type:
                mime_type = 'application/octet-stream'
            
            # Verificar se o tipo é suportado
            if mime_type not in self.supported_types:
                raise ValueError(f"Tipo de arquivo não suportado: {mime_type}")
            
            # Salvar arquivo
            file_path = self.upload_dir / f"{doc_id}_{filename}"
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Extrair texto do documento
            extractor = self.supported_types[mime_type]
            extracted_text = extractor(file_path)
            
            # Criar metadados do documento
            document_metadata = {
                "id": doc_id,
                "filename": filename,
                "mime_type": mime_type,
                "file_path": str(file_path),
                "description": description,
                "uploaded_at": datetime.now().isoformat(),
                "text_length": len(extracted_text),
                "status": "processed"
            }
            
            # Salvar metadados
            metadata_path = self.upload_dir / f"{doc_id}_metadata.json"
            import json
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(document_metadata, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Documento processado: {filename} ({len(extracted_text)} caracteres)")
            
            return {
                "status": "success",
                "document_id": doc_id,
                "filename": filename,
                "text_length": len(extracted_text),
                "metadata": document_metadata
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar documento: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _extract_pdf(self, file_path: Path) -> str:
        """Extrai texto de arquivo PDF"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Erro ao extrair PDF: {e}")
            return ""
    
    def _extract_docx(self, file_path: Path) -> str:
        """Extrai texto de arquivo DOCX"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Erro ao extrair DOCX: {e}")
            return ""
    
    def _extract_txt(self, file_path: Path) -> str:
        """Extrai texto de arquivo TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            logger.error(f"Erro ao extrair TXT: {e}")
            return ""
    
    def _extract_markdown(self, file_path: Path) -> str:
        """Extrai texto de arquivo Markdown"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                md_content = file.read()
                # Converter markdown para HTML e depois extrair texto
                html = markdown.markdown(md_content)
                soup = BeautifulSoup(html, 'html.parser')
                return soup.get_text().strip()
        except Exception as e:
            logger.error(f"Erro ao extrair Markdown: {e}")
            return ""
    
    def _extract_html(self, file_path: Path) -> str:
        """Extrai texto de arquivo HTML"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                return soup.get_text().strip()
        except Exception as e:
            logger.error(f"Erro ao extrair HTML: {e}")
            return ""
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Recupera documento por ID"""
        try:
            metadata_path = self.upload_dir / f"{document_id}_metadata.json"
            if not metadata_path.exists():
                return None
            
            import json
            with open(metadata_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao recuperar documento: {e}")
            return None
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """Lista todos os documentos processados"""
        try:
            documents = []
            for metadata_file in self.upload_dir.glob("*_metadata.json"):
                import json
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    doc_data = json.load(f)
                    documents.append(doc_data)
            
            return sorted(documents, key=lambda x: x['uploaded_at'], reverse=True)
        except Exception as e:
            logger.error(f"Erro ao listar documentos: {e}")
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """Remove documento e seus metadados"""
        try:
            metadata_path = self.upload_dir / f"{document_id}_metadata.json"
            if not metadata_path.exists():
                return False
            
            # Carregar metadados para obter caminho do arquivo
            import json
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Remover arquivo original
            file_path = Path(metadata['file_path'])
            if file_path.exists():
                file_path.unlink()
            
            # Remover metadados
            metadata_path.unlink()
            
            logger.info(f"✅ Documento removido: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover documento: {e}")
            return False
    
    def search_documents(self, query: str) -> List[Dict[str, Any]]:
        """Busca documentos por conteúdo"""
        try:
            documents = self.list_documents()
            results = []
            
            for doc in documents:
                # Buscar no texto extraído (implementação simples)
                if query.lower() in doc.get('description', '').lower():
                    results.append(doc)
                    continue
                
                # Buscar no arquivo de texto se disponível
                file_path = Path(doc['file_path'])
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if query.lower() in content.lower():
                                results.append(doc)
                    except:
                        pass  # Ignorar erros de leitura
            
            return results
            
        except Exception as e:
            logger.error(f"Erro na busca de documentos: {e}")
            return []
