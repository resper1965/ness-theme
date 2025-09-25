'use client'

import { useState, useCallback } from 'react'
import { toast } from 'sonner'

interface ChatMessage {
  id: string
  content: string
  agent_id: string
  session_id: string
  timestamp: string
  metadata: Record<string, any>
}

interface ChatSession {
  session_id: string
  status: string
  agents_count: number
  orchestrator_available: boolean
  agno_sdk_available: boolean
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null)
  const [initialized, setInitialized] = useState(false)

  const sendMessage = useCallback(async (message: string, sessionId: string = 'default-session') => {
    if (!message.trim()) {
      toast.error('Mensagem não pode estar vazia')
      return
    }

    setIsLoading(true)
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 10000) // 10 segundos timeout
      
      const response = await fetch('http://localhost:7777/chat/send-message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.trim(),
          session_id: sessionId
        }),
        signal: controller.signal
      })
      
      clearTimeout(timeoutId)

      if (response.ok) {
        const messageResponse = await response.json()
        
        // Adicionar mensagem do usuário
        const userMessage: ChatMessage = {
          id: `user-${Date.now()}`,
          content: message,
          agent_id: 'user',
          session_id: sessionId,
          timestamp: new Date().toISOString(),
          metadata: {}
        }
        
        // Adicionar resposta do agente
        const agentMessage: ChatMessage = {
          id: messageResponse.id,
          content: messageResponse.content,
          agent_id: messageResponse.agent_id,
          session_id: messageResponse.session_id,
          timestamp: messageResponse.timestamp,
          metadata: messageResponse.metadata
        }
        
        setMessages(prev => [...prev, userMessage, agentMessage])
        
        toast.success('Mensagem enviada com sucesso!')
      } else {
        const error = await response.json()
        toast.error(`Erro ao enviar mensagem: ${error.detail}`)
      }
    } catch (error: any) {
      console.error('Erro ao enviar mensagem:', error)
      if (error.name === 'AbortError') {
        toast.error('Timeout: A mensagem demorou muito para ser processada')
      } else {
        toast.error('Erro ao enviar mensagem')
      }
    } finally {
      setIsLoading(false)
    }
  }, [])

  const startChatSession = useCallback(async (sessionId: string = 'default-session') => {
    if (initialized) return currentSession
    
    try {
      const response = await fetch(`http://localhost:7777/chat/sessions/${sessionId}/start-chat`, {
        method: 'POST'
      })

      if (response.ok) {
        const sessionData = await response.json()
        setCurrentSession(sessionData)
        setInitialized(true)
        return sessionData
      } else {
        const error = await response.json()
        console.error(`Erro ao iniciar chat: ${error.detail}`)
        return null
      }
    } catch (error) {
      console.error('Erro ao iniciar sessão:', error)
      return null
    }
  }, [initialized, currentSession])

  const getChatStatus = useCallback(async (sessionId: string = 'default-session') => {
    if (initialized) return currentSession
    
    try {
      const response = await fetch(`http://localhost:7777/chat/sessions/${sessionId}/status`)
      
      if (response.ok) {
        const status = await response.json()
        setCurrentSession(status)
        setInitialized(true)
        return status
      } else {
        const error = await response.json()
        console.error(`Erro ao verificar status: ${error.detail}`)
        return null
      }
    } catch (error) {
      console.error('Erro ao verificar status:', error)
      return null
    }
  }, [initialized, currentSession])

  const clearChat = useCallback(async (sessionId: string = 'default-session') => {
    try {
      const response = await fetch(`http://localhost:7777/chat/sessions/${sessionId}/clear`, {
        method: 'POST'
      })

      if (response.ok) {
        setMessages([])
        toast.success('Chat limpo com sucesso!')
      } else {
        const error = await response.json()
        toast.error(`Erro ao limpar chat: ${error.detail}`)
      }
    } catch (error) {
      console.error('Erro ao limpar chat:', error)
      toast.error('Erro ao limpar chat')
    }
  }, [])

  const loadMessages = useCallback(async (sessionId: string = 'default-session', limit: number = 50) => {
    try {
      const response = await fetch(`http://localhost:7777/chat/sessions/${sessionId}/messages?limit=${limit}`)
      
      if (response.ok) {
        const data = await response.json()
        setMessages(data.messages || [])
        return data.messages || []
      } else {
        const error = await response.json()
        toast.error(`Erro ao carregar mensagens: ${error.detail}`)
        return []
      }
    } catch (error) {
      console.error('Erro ao carregar mensagens:', error)
      return []
    }
  }, [])

  return {
    messages,
    isLoading,
    currentSession,
    sendMessage,
    startChatSession,
    getChatStatus,
    clearChat,
    loadMessages
  }
}
