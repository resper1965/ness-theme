"""
Configuração de conexão com banco de dados
"""

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import get_settings

logger = logging.getLogger(__name__)

# Configurações
settings = get_settings()

# Engine do SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

async def get_database():
    """Inicializa conexão com banco de dados"""
    try:
        # Testar conexão
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        
        logger.info("✅ Conexão com banco de dados estabelecida")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao conectar com banco de dados: {e}")
        raise

def get_db():
    """Dependency para obter sessão do banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
