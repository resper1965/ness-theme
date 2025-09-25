"""
Rotas para chat funcional
Integração com Agno SDK para processamento de mensagens
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from app.schemas.agent import MessageRequest, MessageResponse
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, ChatSessionStatus, ChatSessionStart
from app.services.agno_service import AgnoService
import uuid
from datetime import datetime

router = APIRouter()

# Instância global do serviço Agno
_agno_service = None

def get_agno_service() -> AgnoService:
    global _agno_service
    if _agno_service is None:
        _agno_service = AgnoService()
    return _agno_service

@router.post("/send-message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Envia mensagem para processamento pelos agentes"""
    try:
        message = request.message
        session_id = request.session_id
        agent_id = request.agent_id
        
        # Se não especificado, usar orquestrador da sessão ou primeiro agente disponível
        if not agent_id:
            if session_id in agno_service.active_sessions:
                session = agno_service.active_sessions[session_id]
                # Buscar orquestrador na sessão
                for aid in session.agent_ids:
                    if aid in agno_service.active_agents:
                        agent = agno_service.active_agents[aid]
                        if str(agent.type) == "AgentType.ORCHESTRATOR":
                            agent_id = aid
                            break
                
                # Se não encontrou orquestrador, usar primeiro agente disponível
                if not agent_id and session.agent_ids:
                    agent_id = session.agent_ids[0]
            else:
                # Se sessão não existe, usar agente padrão
                agent_id = "default-agent"
        
        # Processar mensagem
        response = await agno_service.process_message(session_id, message)
        
        # Criar resposta estruturada
        message_response = ChatMessageResponse(
            id=str(uuid.uuid4()),
            content=response.get("message", "Mensagem processada com sucesso"),
            agent_id=agent_id or "orchestrator",
            session_id=session_id,
            timestamp=datetime.now(),
            metadata=response.get("metadata", {})
        )
        
        return message_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar mensagem: {str(e)}")

@router.get("/sessions/{session_id}/messages")
async def get_session_messages(
    session_id: str,
    limit: int = 50,
    offset: int = 0,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna mensagens de uma sessão"""
    try:
        # Implementação futura: buscar mensagens do banco de dados
        # Por enquanto, retorna mensagens mockup
        messages = [
            {
                "id": "msg-1",
                "content": "Olá! Como posso ajudar?",
                "agent_id": "orchestrator",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "metadata": {}
            }
        ]
        
        return {
            "messages": messages,
            "total": len(messages),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar mensagens: {str(e)}")

@router.post("/sessions/{session_id}/start-chat")
async def start_chat_session(
    session_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Inicia uma sessão de chat"""
    try:
        # Verificar se sessão existe
        if session_id not in agno_service.active_sessions:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")
        
        session = agno_service.active_sessions[session_id]
        
        # Verificar se tem agentes
        if not session.agent_ids:
            raise HTTPException(status_code=400, detail="Sessão não possui agentes")
        
        return {
            "session_id": session_id,
            "status": "ready",
            "agents_count": len(session.agent_ids),
            "message": "Sessão de chat iniciada com sucesso"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar chat: {str(e)}")

@router.get("/sessions/{session_id}/status")
async def get_chat_status(
    session_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Retorna status da sessão de chat"""
    try:
        if session_id not in agno_service.active_sessions:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")
        
        session = agno_service.active_sessions[session_id]
        
        return {
            "session_id": session_id,
            "status": "active",
            "agents_count": len(session.agent_ids),
            "orchestrator_available": any(
                str(agno_service.active_agents.get(aid, {}).type) == "AgentType.ORCHESTRATOR"
                for aid in session.agent_ids
            ),
            "agno_sdk_available": agno_service.agno_sdk_service.is_agno_available()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar status: {str(e)}")

@router.post("/sessions/{session_id}/clear")
async def clear_chat_session(
    session_id: str,
    agno_service: AgnoService = Depends(get_agno_service)
):
    """Limpa mensagens de uma sessão"""
    try:
        # Implementação futura: limpar mensagens do banco de dados
        return {
            "session_id": session_id,
            "status": "cleared",
            "message": "Mensagens da sessão foram limpas"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar sessão: {str(e)}")
