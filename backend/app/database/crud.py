"""
Operações CRUD para banco de dados
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.models import SessionDB, AgentDB, KnowledgeSourceDB, MessageDB, UserDB
from app.schemas.session import SessionCreate, SessionUpdate
from app.schemas.agent import AgentCreate, AgentUpdate
from datetime import datetime
import uuid

class SessionCRUD:
    """CRUD para sessões"""
    
    @staticmethod
    def create(db: Session, session_data: SessionCreate) -> SessionDB:
        """Cria uma nova sessão"""
        db_session = SessionDB(
            id=session_data.id,
            name=session_data.name,
            description=session_data.description
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def get_by_id(db: Session, session_id: str) -> Optional[SessionDB]:
        """Busca sessão por ID"""
        return db.query(SessionDB).filter(SessionDB.id == session_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[SessionDB]:
        """Lista todas as sessões"""
        return db.query(SessionDB).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, session_id: str, session_data: SessionUpdate) -> Optional[SessionDB]:
        """Atualiza uma sessão"""
        db_session = db.query(SessionDB).filter(SessionDB.id == session_id).first()
        if not db_session:
            return None
        
        if session_data.name is not None:
            db_session.name = session_data.name
        if session_data.description is not None:
            db_session.description = session_data.description
        
        db_session.updated_at = datetime.now()
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def delete(db: Session, session_id: str) -> bool:
        """Remove uma sessão"""
        db_session = db.query(SessionDB).filter(SessionDB.id == session_id).first()
        if not db_session:
            return False
        
        db.delete(db_session)
        db.commit()
        return True

class AgentCRUD:
    """CRUD para agentes"""
    
    @staticmethod
    def create(db: Session, agent_data: AgentCreate, session_id: str) -> AgentDB:
        """Cria um novo agente"""
        db_agent = AgentDB(
            id=agent_data.id,
            name=agent_data.name,
            description=agent_data.description,
            type=agent_data.type,
            model=agent_data.model,
            session_id=session_id
        )
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return db_agent
    
    @staticmethod
    def get_by_id(db: Session, agent_id: str) -> Optional[AgentDB]:
        """Busca agente por ID"""
        return db.query(AgentDB).filter(AgentDB.id == agent_id).first()
    
    @staticmethod
    def get_by_session(db: Session, session_id: str) -> List[AgentDB]:
        """Busca agentes de uma sessão"""
        return db.query(AgentDB).filter(AgentDB.session_id == session_id).all()
    
    @staticmethod
    def get_orchestrators_by_session(db: Session, session_id: str) -> List[AgentDB]:
        """Busca orquestradores de uma sessão"""
        return db.query(AgentDB).filter(
            and_(AgentDB.session_id == session_id, AgentDB.type == "orchestrator")
        ).all()
    
    @staticmethod
    def update(db: Session, agent_id: str, agent_data: AgentUpdate) -> Optional[AgentDB]:
        """Atualiza um agente"""
        db_agent = db.query(AgentDB).filter(AgentDB.id == agent_id).first()
        if not db_agent:
            return None
        
        if agent_data.name is not None:
            db_agent.name = agent_data.name
        if agent_data.description is not None:
            db_agent.description = agent_data.description
        if agent_data.model is not None:
            db_agent.model = agent_data.model
        
        db_agent.updated_at = datetime.now()
        db.commit()
        db.refresh(db_agent)
        return db_agent
    
    @staticmethod
    def delete(db: Session, agent_id: str) -> bool:
        """Remove um agente"""
        db_agent = db.query(AgentDB).filter(AgentDB.id == agent_id).first()
        if not db_agent:
            return False
        
        db.delete(db_agent)
        db.commit()
        return True

class MessageCRUD:
    """CRUD para mensagens"""
    
    @staticmethod
    def create(db: Session, content: str, role: str, session_id: str, agent_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> MessageDB:
        """Cria uma nova mensagem"""
        db_message = MessageDB(
            id=str(uuid.uuid4()),
            content=content,
            role=role,
            session_id=session_id,
            agent_id=agent_id,
            metadata=metadata or {}
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    
    @staticmethod
    def get_by_session(db: Session, session_id: str, skip: int = 0, limit: int = 100) -> List[MessageDB]:
        """Busca mensagens de uma sessão"""
        return db.query(MessageDB).filter(
            MessageDB.session_id == session_id
        ).order_by(MessageDB.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_agent(db: Session, agent_id: str, skip: int = 0, limit: int = 100) -> List[MessageDB]:
        """Busca mensagens de um agente"""
        return db.query(MessageDB).filter(
            MessageDB.agent_id == agent_id
        ).order_by(MessageDB.created_at.desc()).offset(skip).limit(limit).all()

class KnowledgeSourceCRUD:
    """CRUD para fontes de conhecimento"""
    
    @staticmethod
    def create(db: Session, name: str, type: str, config: Dict[str, Any], agent_id: str) -> KnowledgeSourceDB:
        """Cria uma nova fonte de conhecimento"""
        db_source = KnowledgeSourceDB(
            id=str(uuid.uuid4()),
            name=name,
            type=type,
            config=config,
            agent_id=agent_id
        )
        db.add(db_source)
        db.commit()
        db.refresh(db_source)
        return db_source
    
    @staticmethod
    def get_by_agent(db: Session, agent_id: str) -> List[KnowledgeSourceDB]:
        """Busca fontes de conhecimento de um agente"""
        return db.query(KnowledgeSourceDB).filter(KnowledgeSourceDB.agent_id == agent_id).all()
    
    @staticmethod
    def get_by_type(db: Session, type: str) -> List[KnowledgeSourceDB]:
        """Busca fontes de conhecimento por tipo"""
        return db.query(KnowledgeSourceDB).filter(KnowledgeSourceDB.type == type).all()
    
    @staticmethod
    def delete(db: Session, source_id: str) -> bool:
        """Remove uma fonte de conhecimento"""
        db_source = db.query(KnowledgeSourceDB).filter(KnowledgeSourceDB.id == source_id).first()
        if not db_source:
            return False
        
        db.delete(db_source)
        db.commit()
        return True
