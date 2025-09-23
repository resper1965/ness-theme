"""
Configurações do Gabi Backend
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Ambiente
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database - Neon (produção)
    DATABASE_URL: str = "postgresql://neon_connection_string_here"
    
    # Neon Database (substitui Supabase local)
    # Use banco Neon para todos os ambientes conforme especificado
    
    # Agno SDK
    AGNO_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # Security
    SECRET_KEY: str = "gabi-secret-key-change-in-production"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Retorna lista de origens CORS"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        """Retorna lista de hosts permitidos"""
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",")]
    
    # Agentes
    MAX_AGENTS_PER_SESSION: int = 3
    MAX_ORCHESTRATOR_PER_SESSION: int = 1
    
    # Knowledge Base
    MAX_KB_SOURCES: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True

def get_settings() -> Settings:
    """Retorna as configurações da aplicação"""
    return Settings()
