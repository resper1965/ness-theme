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
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/gabi"
    
    # Supabase
    SUPABASE_URL: str = "http://localhost:8000"
    SUPABASE_ANON_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
    SUPABASE_SERVICE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"
    JWT_SECRET: str = "super-secret-jwt-token-with-at-least-32-characters-long"
    
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
