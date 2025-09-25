'use client'

import { useState, useEffect, useCallback } from 'react'
import { useStore } from '@/store'
import { useQueryState } from 'nuqs'
import { toast } from 'sonner'

interface SavedChat {
  id: string
  title: string
  lastMessage: string
  timestamp: Date
  agentId?: string
  teamId?: string
  messageCount: number
  mode: 'agent' | 'team'
  messages: any[]
}

const STORAGE_KEY = 'gabi-saved-chats'

export function useSavedChats() {
  const { mode, agents, teams, setMessages, setMode } = useStore()
  const [savedChats, setSavedChats] = useState<SavedChat[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [agentId, setAgentId] = useQueryState('agent')
  const [teamId, setTeamId] = useQueryState('team')
  const [, setSessionId] = useQueryState('session')

  // Carregar chats salvos
  useEffect(() => {
    loadSavedChats()
  }, [])

  const loadSavedChats = useCallback(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      if (saved) {
        const parsed = JSON.parse(saved)
        setSavedChats(parsed.map((chat: any) => ({
          ...chat,
          timestamp: new Date(chat.timestamp)
        })))
      }
    } catch (error) {
      console.error('Erro ao carregar chats salvos:', error)
    }
  }, [])

  const saveCurrentChat = useCallback(() => {
    const currentMessages = useStore.getState().messages
    if (currentMessages.length === 0) {
      toast.error('Nenhuma mensagem para salvar')
      return false
    }

    const newChat: SavedChat = {
      id: `chat-${Date.now()}`,
      title: `Chat ${new Date().toLocaleDateString('pt-BR')}`,
      lastMessage: currentMessages[currentMessages.length - 1]?.content || 'Chat iniciado',
      timestamp: new Date(),
      agentId: mode === 'agent' ? agentId || undefined : undefined,
      teamId: mode === 'team' ? teamId || undefined : undefined,
      messageCount: currentMessages.length,
      mode,
      messages: [...currentMessages]
    }

    const updatedChats = [newChat, ...savedChats]
    setSavedChats(updatedChats)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedChats))
    toast.success('Chat salvo com sucesso!')
    return true
  }, [savedChats, mode, agentId, teamId])

  const loadChat = useCallback(async (chat: SavedChat) => {
    setIsLoading(true)
    
    try {
      // Definir modo e entidade
      setMode(chat.mode)
      if (chat.mode === 'agent' && chat.agentId) {
        setAgentId(chat.agentId)
        setTeamId(null)
      } else if (chat.mode === 'team' && chat.teamId) {
        setTeamId(chat.teamId)
        setAgentId(null)
      }

      // Carregar mensagens
      setMessages(chat.messages)
      setSessionId(chat.id)

      toast.success(`Chat "${chat.title}" carregado!`)
    } catch (error) {
      console.error('Erro ao carregar chat:', error)
      toast.error('Erro ao carregar chat')
    } finally {
      setIsLoading(false)
    }
  }, [setMode, setAgentId, setTeamId, setMessages, setSessionId])

  const deleteChat = useCallback((chatId: string) => {
    if (confirm('Tem certeza que deseja excluir este chat?')) {
      const updatedChats = savedChats.filter(chat => chat.id !== chatId)
      setSavedChats(updatedChats)
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedChats))
      toast.success('Chat excluído!')
    }
  }, [savedChats])

  const editChatTitle = useCallback((chatId: string, newTitle: string) => {
    const updatedChats = savedChats.map(chat => 
      chat.id === chatId ? { ...chat, title: newTitle } : chat
    )
    setSavedChats(updatedChats)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedChats))
    toast.success('Título atualizado!')
  }, [savedChats])

  const getEntityName = useCallback((chat: SavedChat) => {
    if (chat.mode === 'agent' && chat.agentId) {
      const agent = agents.find(a => a.id === chat.agentId)
      return agent?.name || 'Agente'
    } else if (chat.mode === 'team' && chat.teamId) {
      const team = teams.find(t => t.id === chat.teamId)
      return team?.name || 'Time'
    }
    return 'Chat'
  }, [agents, teams])

  return {
    savedChats,
    isLoading,
    saveCurrentChat,
    loadChat,
    deleteChat,
    editChatTitle,
    getEntityName,
    loadSavedChats
  }
}
