'use client'

import * as React from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { useStore } from '@/store'
import { useQueryState } from 'nuqs'
import { MessageSquare, Clock, Trash2, Settings } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { ptBR } from 'date-fns/locale'

interface ChatSession {
  id: string
  title: string
  lastMessage: string
  timestamp: Date
  agentId?: string
  teamId?: string
  messageCount: number
}

export function ChatHistory() {
  const { mode, agents, teams } = useStore()
  const [sessions, setSessions] = React.useState<ChatSession[]>([])
  const [agentId] = useQueryState('agent')
  const [teamId] = useQueryState('team')

  // Carregar sessões do localStorage
  React.useEffect(() => {
    const savedSessions = localStorage.getItem('gabi-chat-sessions')
    if (savedSessions) {
      try {
        const parsed = JSON.parse(savedSessions)
        setSessions(parsed.map((s: any) => ({
          ...s,
          timestamp: new Date(s.timestamp)
        })))
      } catch (error) {
        console.error('Erro ao carregar sessões:', error)
      }
    }
  }, [])

  // Salvar sessões no localStorage
  React.useEffect(() => {
    if (sessions.length > 0) {
      localStorage.setItem('gabi-chat-sessions', JSON.stringify(sessions))
    }
  }, [sessions])

  const getCurrentEntityName = () => {
    if (mode === 'team' && teamId) {
      const team = teams.find(t => t.id === teamId)
      return team?.name || 'Time'
    } else if (mode === 'agent' && agentId) {
      const agent = agents.find(a => a.id === agentId)
      return agent?.name || 'Agente'
    }
    return 'Chat'
  }

  const createNewSession = () => {
    const newSession: ChatSession = {
      id: `session-${Date.now()}`,
      title: `Nova conversa com ${getCurrentEntityName()}`,
      lastMessage: 'Conversa iniciada',
      timestamp: new Date(),
      agentId: mode === 'agent' ? agentId || undefined : undefined,
      teamId: mode === 'team' ? teamId || undefined : undefined,
      messageCount: 0
    }
    
    setSessions(prev => [newSession, ...prev])
    return newSession.id
  }

  const deleteSession = (sessionId: string) => {
    setSessions(prev => prev.filter(s => s.id !== sessionId))
  }

  const loadSession = (sessionId: string) => {
    // Implementar carregamento da sessão
    console.log('Carregando sessão:', sessionId)
  }

  if (sessions.length === 0) {
    return (
      <div className="px-4 py-2">
        <div className="flex items-center gap-2 text-sm font-medium text-sidebar-foreground mb-2">
          <MessageSquare className="h-4 w-4" />
          Histórico de Chats
        </div>
        <Card className="bg-sidebar border-cyan-800">
          <CardContent className="p-4 text-center">
            <MessageSquare className="h-8 w-8 mx-auto text-muted-foreground mb-2" />
            <p className="text-xs text-muted-foreground mb-3">
              Nenhum chat encontrado
            </p>
            <Button 
              size="sm" 
              className="w-full"
              onClick={createNewSession}
            >
              Iniciar Nova Conversa
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
          Histórico de Chats
        </div>
        <Button
          size="sm"
          variant="ghost"
          onClick={createNewSession}
          className="h-6 w-6 p-0"
        >
          <MessageSquare className="h-3 w-3" />
        </Button>
      </div>
      
      <div className="space-y-2 max-h-64 overflow-y-auto">
        {sessions.map((session) => (
          <Card 
            key={session.id} 
            className="bg-sidebar border-cyan-800 hover:bg-sidebar-accent cursor-pointer transition-colors"
            onClick={() => loadSession(session.id)}
          >
            <CardContent className="p-3">
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <h4 className="text-xs font-medium text-sidebar-foreground truncate">
                    {session.title}
                  </h4>
                  <p className="text-xs text-muted-foreground truncate mt-1">
                    {session.lastMessage}
                  </p>
                  <div className="flex items-center gap-2 mt-2">
                    <Clock className="h-3 w-3 text-muted-foreground" />
                    <span className="text-xs text-muted-foreground">
                      {formatDistanceToNow(session.timestamp, { 
                        addSuffix: true, 
                        locale: ptBR 
                      })}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      • {session.messageCount} msgs
                    </span>
                  </div>
                </div>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={(e) => {
                    e.stopPropagation()
                    deleteSession(session.id)
                  }}
                  className="h-6 w-6 p-0 text-muted-foreground hover:text-destructive"
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
