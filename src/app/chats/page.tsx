'use client'

import React, { useState, useEffect } from 'react'
import { MainLayout } from '@/components/layout/MainLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { History, MessageSquare, Calendar, Trash2, Edit2, Save, X } from 'lucide-react'

export default function ChatsPage() {
  const handleNewChat = () => {
    window.location.href = '/'
  }

  const handleChatClick = (sessionId: string) => {
    // Salvar a sessão selecionada e redirecionar para o chat
    localStorage.setItem('current-session-id', sessionId)
    window.location.href = '/'
  }

  const handleEditChat = (chatId: string, currentTitle: string) => {
    setEditingChat(chatId)
    setEditTitle(currentTitle)
  }

  const handleSaveEdit = (chatId: string) => {
    if (editTitle.trim()) {
      // Atualizar o título do chat no localStorage
      const chatKey = `chat-${chatId}`
      const messages = JSON.parse(localStorage.getItem(chatKey) || '[]')
      
      // Adicionar metadados do chat se não existir
      if (messages.length > 0) {
        messages[0].chatTitle = editTitle.trim()
        localStorage.setItem(chatKey, JSON.stringify(messages))
        
        // Recarregar a lista de chats
        loadSavedChats()
      }
    }
    setEditingChat(null)
    setEditTitle('')
  }

  const handleCancelEdit = () => {
    setEditingChat(null)
    setEditTitle('')
  }

  const loadSavedChats = () => {
    try {
      const chats = []
      
      // Buscar todas as chaves do localStorage que começam com 'chat-'
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i)
        if (key && key.startsWith('chat-session-')) {
          const messages = JSON.parse(localStorage.getItem(key) || '[]')
          if (messages.length > 0) {
            const sessionId = key.replace('chat-', '')
            const firstMessage = messages[0]
            const lastMessage = messages[messages.length - 1]
            
            chats.push({
              id: sessionId,
              title: firstMessage.chatTitle || firstMessage.content.substring(0, 50) + (firstMessage.content.length > 50 ? '...' : ''),
              lastMessage: lastMessage.content,
              timestamp: lastMessage.timestamp,
              messageCount: messages.length,
              sessionId: sessionId
            })
          }
        }
      }
      
      // Ordenar por timestamp (mais recente primeiro)
      chats.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      
      setSavedChats(chats)
    } catch (error) {
      console.error('Erro ao carregar chats salvos:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSettings = () => {
    window.location.href = '/configuracoes'
  }

  const handleLogout = () => {
    console.log('Logout realizado')
  }

  // Buscar chats salvos do localStorage ou backend
  const [savedChats, setSavedChats] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [editingChat, setEditingChat] = useState<string | null>(null)
  const [editTitle, setEditTitle] = useState('')

  useEffect(() => {
    loadSavedChats()
  }, [])

  return (
    <MainLayout 
      pageTitle="Chats"
      onNewChat={handleNewChat}
      onSettings={handleSettings}
      onLogout={handleLogout}
    >
      <div className="p-6">
        <div className="mb-6">
          <p className="text-muted-foreground">
            Gerencie suas conversas e histórico de chats
          </p>
        </div>

        {isLoading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">Carregando chats...</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {savedChats.map((chat) => (
            <Card 
              key={chat.id} 
              className="hover:shadow-md transition-shadow"
            >
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  {editingChat === chat.id ? (
                    <div className="flex items-center gap-2 flex-1">
                      <MessageSquare className="h-5 w-5 text-primary" />
                      <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="flex-1 px-2 py-1 border rounded text-lg font-semibold"
                        autoFocus
                        onKeyPress={(e) => {
                          if (e.key === 'Enter') handleSaveEdit(chat.id)
                          if (e.key === 'Escape') handleCancelEdit()
                        }}
                      />
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleSaveEdit(chat.id)}
                        className="text-green-600 hover:text-green-700"
                      >
                        <Save className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={handleCancelEdit}
                        className="text-red-600 hover:text-red-700"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  ) : (
                    <>
                      <CardTitle 
                        className="text-lg flex items-center gap-2 cursor-pointer flex-1"
                        onClick={() => handleChatClick(chat.sessionId)}
                      >
                        <MessageSquare className="h-5 w-5 text-primary" />
                        {chat.title}
                      </CardTitle>
                      <div className="flex items-center gap-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation()
                            handleEditChat(chat.id, chat.title)
                          }}
                          className="text-blue-600 hover:text-blue-700"
                        >
                          <Edit2 className="h-4 w-4" />
                        </Button>
                        <Badge variant="secondary">
                          {chat.messageCount} mensagens
                        </Badge>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="text-red-600 hover:text-red-700"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </>
                  )}
                </div>
              </CardHeader>
              <CardContent 
                className="cursor-pointer"
                onClick={() => handleChatClick(chat.sessionId)}
              >
                <p className="text-muted-foreground mb-3">{chat.lastMessage}</p>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="h-4 w-4" />
                  {chat.timestamp}
                </div>
              </CardContent>
            </Card>
            ))}
          </div>
        )}

        {!isLoading && savedChats.length === 0 && (
          <Card className="text-center py-12">
            <CardContent>
              <History className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Nenhum chat salvo</h3>
              <p className="text-muted-foreground mb-4">
                Seus chats aparecerão aqui quando você começar a conversar
              </p>
              <Button onClick={handleNewChat}>
                <MessageSquare className="h-4 w-4 mr-2" />
                Iniciar Novo Chat
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </MainLayout>
  )
}