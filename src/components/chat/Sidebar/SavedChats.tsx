'use client'

import * as React from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { useStore } from '@/store'
import { useQueryState } from 'nuqs'
import { MessageSquare, Clock, Trash2, Edit, Play, User, Users2 } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { ptBR } from 'date-fns/locale'
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

export function SavedChats() {
  const { mode, agents, teams, setMessages, setMode } = useStore()
  const [savedChats, setSavedChats] = React.useState<SavedChat[]>([])
  const [isLoading, setIsLoading] = React.useState(false)
  const [agentId, setAgentId] = useQueryState('agent')
  const [teamId, setTeamId] = useQueryState('team')
  const [, setSessionId] = useQueryState('session')

  // Carregar chats salvos do localStorage
  React.useEffect(() => {
    loadSavedChats()
  }, [])

  const loadSavedChats = () => {
    try {
      const saved = localStorage.getItem('gabi-saved-chats')
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
  }

  const saveCurrentChat = () => {
    const currentMessages = useStore.getState().messages
    if (currentMessages.length === 0) {
      toast.error('Nenhuma mensagem para salvar')
      return
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
    localStorage.setItem('gabi-saved-chats', JSON.stringify(updatedChats))
    toast.success('Chat salvo com sucesso!')
  }

  const loadChat = (chat: SavedChat) => {
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
  }

  const deleteChat = (chatId: string) => {
    if (confirm('Tem certeza que deseja excluir este chat?')) {
      const updatedChats = savedChats.filter(chat => chat.id !== chatId)
      setSavedChats(updatedChats)
      localStorage.setItem('gabi-saved-chats', JSON.stringify(updatedChats))
      toast.success('Chat excluído!')
    }
  }

  const editChatTitle = (chatId: string, newTitle: string) => {
    const updatedChats = savedChats.map(chat => 
      chat.id === chatId ? { ...chat, title: newTitle } : chat
    )
    setSavedChats(updatedChats)
    localStorage.setItem('gabi-saved-chats', JSON.stringify(updatedChats))
    toast.success('Título atualizado!')
  }

  const getEntityName = (chat: SavedChat) => {
    if (chat.mode === 'agent' && chat.agentId) {
      const agent = agents.find(a => a.id === chat.agentId)
      return agent?.name || 'Agente'
    } else if (chat.mode === 'team' && chat.teamId) {
      const team = teams.find(t => t.id === chat.teamId)
      return team?.name || 'Time'
    }
    return 'Chat'
  }

  if (savedChats.length === 0) {
    return (
      <div className="px-4 py-2">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2 text-sm font-medium text-sidebar-foreground">
            <MessageSquare className="h-4 w-4" />
            Chats Salvos
          </div>
          <Button
            size="sm"
            variant="ghost"
            onClick={saveCurrentChat}
            className="h-6 w-6 p-0"
          >
            <MessageSquare className="h-3 w-3" />
          </Button>
        </div>
        
        <Card className="bg-sidebar border-cyan-800">
          <CardContent className="p-4 text-center">
            <MessageSquare className="h-8 w-8 mx-auto text-muted-foreground mb-2" />
            <p className="text-xs text-muted-foreground mb-3">
              Nenhum chat salvo
            </p>
            <Button 
              size="sm" 
              className="w-full"
              onClick={saveCurrentChat}
            >
              Salvar Chat Atual
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="px-4 py-2">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2 text-sm font-medium text-sidebar-foreground">
          <MessageSquare className="h-4 w-4" />
          Chats Salvos ({savedChats.length})
        </div>
        <Button
          size="sm"
          variant="ghost"
          onClick={saveCurrentChat}
          className="h-6 w-6 p-0"
        >
          <MessageSquare className="h-3 w-3" />
        </Button>
      </div>
      
      <div className="space-y-2 max-h-64 overflow-y-auto">
        {savedChats.map((chat) => (
          <Card 
            key={chat.id} 
            className="bg-sidebar border-cyan-800 hover:bg-sidebar-accent cursor-pointer transition-colors group"
            onClick={() => loadChat(chat)}
          >
            <CardContent className="p-3">
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="text-xs font-medium text-sidebar-foreground truncate">
                      {chat.title}
                    </h4>
                    <Badge variant="secondary" className="text-xs">
                      {chat.mode === 'agent' ? <User className="h-3 w-3 mr-1" /> : <Users2 className="h-3 w-3 mr-1" />}
                      {getEntityName(chat)}
                    </Badge>
                  </div>
                  
                  <p className="text-xs text-muted-foreground truncate mb-2">
                    {chat.lastMessage}
                  </p>
                  
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <Clock className="h-3 w-3" />
                    <span>
                      {formatDistanceToNow(chat.timestamp, { 
                        addSuffix: true, 
                        locale: ptBR 
                      })}
                    </span>
                    <span>•</span>
                    <span>{chat.messageCount} msgs</span>
                  </div>
                </div>
                
                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={(e) => {
                      e.stopPropagation()
                      const newTitle = prompt('Novo título:', chat.title)
                      if (newTitle && newTitle.trim()) {
                        editChatTitle(chat.id, newTitle.trim())
                      }
                    }}
                    className="h-6 w-6 p-0"
                  >
                    <Edit className="h-3 w-3" />
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={(e) => {
                      e.stopPropagation()
                      deleteChat(chat.id)
                    }}
                    className="h-6 w-6 p-0 text-destructive hover:text-destructive"
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
