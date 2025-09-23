"""
Serviço de integração com Supabase Local (Simplificado)
Gerencia apenas banco de dados sem autenticação
"""

import logging
from typing import Dict, Any, Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config.settings import get_settings

logger = logging.getLogger(__name__)

class SupabaseService:
    """Serviço de integração com Supabase Local (Simplificado)"""
    
    def __init__(self):
        self.settings = get_settings()
        self.connection = None
        self.is_connected = False
    
    async def initialize(self):
        """Inicializa conexão com Supabase"""
        try:
            # Conectar diretamente ao PostgreSQL
            self.connection = psycopg2.connect(
                host="localhost",
                port=5432,
                database="gabi",
                user="postgres",
                password="postgres"
            )
            
            # Testar conexão
            await self._test_connection()
            
            self.is_connected = True
            logger.info("✅ Supabase Service inicializado (modo simplificado)")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Supabase Service: {e}")
            raise
    
    async def _test_connection(self):
        """Testa conexão com Supabase"""
        try:
            # Testar conexão básica
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            logger.info("✅ Conexão com Supabase estabelecida")
            
        except Exception as e:
            logger.warning(f"⚠️ Aviso na conexão Supabase: {e}")
            # Não falhar se tabelas não existem ainda
    
    async def create_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria sessão via Supabase"""
        try:
            if not self.is_connected:
                raise ValueError("Supabase não conectado")
            
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                INSERT INTO sessions (id, name, description, max_agents, max_orchestrator, status)
                VALUES (%(id)s, %(name)s, %(description)s, %(max_agents)s, %(max_orchestrator)s, %(status)s)
                RETURNING *
            """, session_data)
            
            result = cursor.fetchone()
            self.connection.commit()
            cursor.close()
            
            logger.info(f"✅ Sessão criada via Supabase: {result['id']}")
            return dict(result)
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar sessão: {e}")
            raise
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Busca sessão via Supabase"""
        try:
            if not self.is_connected:
                raise ValueError("Supabase não conectado")
            
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return dict(result) if result else None
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar sessão: {e}")
            raise
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza sessão via Supabase"""
        try:
            if not self.is_connected:
                raise ValueError("Supabase não conectado")
            
            # Construir query de update dinamicamente
            set_clause = ", ".join([f"{key} = %({key})s" for key in updates.keys()])
            updates['id'] = session_id
            
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(f"""
                UPDATE sessions 
                SET {set_clause}, updated_at = NOW()
                WHERE id = %(id)s
                RETURNING *
            """, updates)
            
            result = cursor.fetchone()
            self.connection.commit()
            cursor.close()
            
            if result:
                logger.info(f"✅ Sessão atualizada via Supabase: {session_id}")
                return dict(result)
            else:
                raise ValueError("Sessão não encontrada")
                
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar sessão: {e}")
            raise
    
    async def delete_session(self, session_id: str) -> bool:
        """Remove sessão via Supabase"""
        try:
            if not self.is_connected:
                raise ValueError("Supabase não conectado")
            
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
            self.connection.commit()
            cursor.close()
            
            logger.info(f"✅ Sessão removida via Supabase: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao remover sessão: {e}")
            raise
    
    async def create_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria agente via Supabase"""
        try:
            if not self.is_connected:
                raise ValueError("Supabase não conectado")
            
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                INSERT INTO agents (id, name, description, type, model, status, session_id)
                VALUES (%(id)s, %(name)s, %(description)s, %(type)s, %(model)s, %(status)s, %(session_id)s)
                RETURNING *
            """, agent_data)
            
            result = cursor.fetchone()
            self.connection.commit()
            cursor.close()
            
            logger.info(f"✅ Agente criado via Supabase: {result['id']}")
            return dict(result)
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar agente: {e}")
            raise
    
    async def get_session_agents(self, session_id: str) -> List[Dict[str, Any]]:
        """Busca agentes de uma sessão via Supabase"""
        try:
            if not self.is_connected:
                raise ValueError("Supabase não conectado")
            
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM agents WHERE session_id = %s", (session_id,))
            results = cursor.fetchall()
            cursor.close()
            
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar agentes: {e}")
            raise
    
    async def create_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria mensagem via Supabase"""
        try:
            if not self.is_connected:
                raise ValueError("Supabase não conectado")
            
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                INSERT INTO messages (id, content, role, session_id, agent_id, metadata)
                VALUES (%(id)s, %(content)s, %(role)s, %(session_id)s, %(agent_id)s, %(metadata)s)
                RETURNING *
            """, message_data)
            
            result = cursor.fetchone()
            self.connection.commit()
            cursor.close()
            
            logger.info(f"✅ Mensagem criada via Supabase: {result['id']}")
            return dict(result)
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar mensagem: {e}")
            raise
    
    async def get_session_messages(self, session_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Busca mensagens de uma sessão via Supabase"""
        try:
            if not self.is_connected:
                raise ValueError("Supabase não conectado")
            
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT * FROM messages 
                WHERE session_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (session_id, limit))
            results = cursor.fetchall()
            cursor.close()
            
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar mensagens: {e}")
            raise
    
    async def cleanup(self):
        """Limpa recursos do serviço"""
        try:
            if self.connection:
                self.connection.close()
            
            self.is_connected = False
            logger.info("✅ Supabase Service finalizado")
            
        except Exception as e:
            logger.error(f"❌ Erro ao finalizar Supabase Service: {e}")
