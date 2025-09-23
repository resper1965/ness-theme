"""
Classe base para modelos
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ModelResponse(BaseModel):
    """Resposta do modelo"""
    content: str
    metadata: Dict[str, Any] = {}
    usage: Dict[str, int] = {}
    model: str


class Model(BaseModel, ABC):
    """Classe base para modelos de IA"""
    
    name: str
    provider: str
    config: Dict[str, Any] = {}
    
    @abstractmethod
    async def generate_response(
        self, 
        context: Dict[str, Any],
        **kwargs
    ) -> str:
        """Gera resposta baseada no contexto"""
        pass
    
    @abstractmethod
    async def generate_response_with_metadata(
        self, 
        context: Dict[str, Any],
        **kwargs
    ) -> ModelResponse:
        """Gera resposta com metadados"""
        pass
    
    def validate_config(self) -> bool:
        """Valida configuração do modelo"""
        return True
    
    def get_model_info(self) -> Dict[str, Any]:
        """Retorna informações do modelo"""
        return {
            "name": self.name,
            "provider": self.provider,
            "config": self.config
        }
