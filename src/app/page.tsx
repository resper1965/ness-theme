"use client";

import React, { useState, useCallback, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, Send, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { MainLayout } from "@/components/layout/MainLayout";

interface ChatMessage {
  id: string;
  content: string;
  agent_id: string;
  session_id: string;
  timestamp: string;
  metadata: Record<string, any>;
}

function Gabi_ChatSimple() {
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(() => {
    // Gerar um ID único para a sessão ou usar um existente
    if (typeof window !== 'undefined') {
      const savedSessionId = localStorage.getItem('current-session-id');
      if (savedSessionId) {
        return savedSessionId;
      }
      const newSessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('current-session-id', newSessionId);
      return newSessionId;
    }
    return 'default-session';
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll automático para o final quando uma nova mensagem chegar
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Carregar mensagens salvas do localStorage
  useEffect(() => {
    const savedMessages = localStorage.getItem(`chat-${sessionId}`);
    if (savedMessages) {
      try {
        const parsedMessages = JSON.parse(savedMessages);
        setMessages(parsedMessages);
      } catch (error) {
        console.error('Erro ao carregar mensagens salvas:', error);
      }
    } else {
      // Se não há mensagens salvas, limpar o estado
      setMessages([]);
    }
  }, [sessionId]);

  // Salvar mensagens no localStorage sempre que mudarem
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(`chat-${sessionId}`, JSON.stringify(messages));
    }
  }, [messages, sessionId]);

  const sendMessage = useCallback(async (message: string) => {
    if (!message.trim()) {
      toast.error('Mensagem não pode estar vazia');
      return;
    }

    setIsLoading(true);
    
    // Adicionar mensagem do usuário imediatamente
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      content: message,
      agent_id: 'user',
      session_id: sessionId,
      timestamp: new Date().toISOString(),
      metadata: {}
    };
    
    setMessages(prev => [...prev, userMessage]);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);
      
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
      });
      
      clearTimeout(timeoutId);

      if (response.ok) {
        const messageResponse = await response.json();
        
        // Adicionar resposta do agente
        const agentMessage: ChatMessage = {
          id: messageResponse.id,
          content: messageResponse.content,
          agent_id: messageResponse.agent_id,
          session_id: messageResponse.session_id,
          timestamp: messageResponse.timestamp,
          metadata: messageResponse.metadata
        };
        
        setMessages(prev => [...prev, agentMessage]);
        toast.success('Mensagem enviada!');
      } else {
        const error = await response.json();
        toast.error(`Erro: ${error.detail}`);
      }
    } catch (error: any) {
      console.error('Erro ao enviar mensagem:', error);
      if (error.name === 'AbortError') {
        toast.error('Timeout: Tente novamente');
      } else {
        toast.error('Erro de conexão');
      }
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    const message = inputMessage;
    setInputMessage('');
    await sendMessage(message);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    localStorage.removeItem(`chat-${sessionId}`);
    toast.success('Chat limpo!');
  };

  const handleNewChat = () => {
    // Criar nova sessão
    const newSessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    setSessionId(newSessionId);
    localStorage.setItem('current-session-id', newSessionId);
    
    setMessages([]);
    setInputMessage('');
    toast.success('Novo chat iniciado!');
  };

  const handleSettings = () => {
    window.location.href = '/configuracoes';
  };

  const handleLogout = () => {
    console.log('Logout realizado');
  };

  return (
    <MainLayout 
      pageTitle="Chat"
      onNewChat={handleNewChat}
      onSettings={handleSettings}
      onLogout={handleLogout}
    >
      <div className="flex flex-col h-full">
            {/* Header do Chat - Fixo */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-border bg-background flex-shrink-0 sticky top-0 z-20">
              <div className="flex items-center gap-3">
                <Badge variant="secondary">
                  {messages.length} mensagens
                </Badge>
                <Badge variant="outline" className="text-xs">
                  Sessão: {sessionId.substring(0, 8)}...
                </Badge>
              </div>
          {messages.length > 0 && (
            <Button
              variant="outline"
              size="sm"
              onClick={clearChat}
              className="text-red-600 hover:text-red-700"
            >
              <Trash2 className="h-4 w-4 mr-1" />
              Limpar Chat
            </Button>
          )}
        </div>

        {/* Área de mensagens - Scroll automático */}
        <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
          {messages.length === 0 ? (
            <div className="flex-1 flex flex-col items-center justify-center px-6 py-12">
              <div className="w-full max-w-2xl">
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-semibold text-foreground mb-2">
                    Como posso ajudar?
                  </h2>
                  <p className="text-muted-foreground">
                    Comece uma conversa digitando sua mensagem abaixo
                  </p>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex-1 overflow-y-auto px-6 py-4 scroll-smooth max-h-full">
              <div className="max-w-4xl mx-auto space-y-4 pb-4">
                {messages.map((message) => (
                  <Card key={message.id} className={`p-4 ${
                    message.agent_id === 'user' 
                      ? 'ml-auto bg-blue-50 border-blue-200' 
                      : 'mr-auto bg-gray-50 border-gray-200'
                  }`}>
                    <CardContent className="p-0">
                      <div className="flex items-start gap-3">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                          message.agent_id === 'user' 
                            ? 'bg-blue-600 text-white' 
                            : 'bg-gray-600 text-white'
                        }`}>
                          {message.agent_id === 'user' ? 'U' : 'G'}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-medium text-sm">
                              {message.agent_id === 'user' ? 'Você' : 'Gabi'}
                            </span>
                            <span className="text-xs text-gray-500">
                              {new Date(message.timestamp).toLocaleTimeString()}
                            </span>
                          </div>
                          <p className="text-foreground whitespace-pre-wrap">{message.content}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
                {isLoading && (
                  <Card className="mr-auto bg-gray-50 border-gray-200 p-4">
                    <CardContent className="p-0">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-gray-600 text-white flex items-center justify-center text-sm font-medium">
                          G
                        </div>
                        <div className="flex items-center gap-2">
                          <Loader2 className="h-4 w-4 animate-spin" />
                          <span className="text-gray-600">Gabi está pensando...</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
                {/* Elemento para scroll automático */}
                <div ref={messagesEndRef} />
              </div>
            </div>
          )}

            {/* Campo de entrada - Fixo na parte inferior */}
            <div className="border-t border-border p-4 flex-shrink-0 sticky bottom-0 bg-background z-10">
            <div className="max-w-4xl mx-auto">
              <div className="bg-accent rounded-lg p-4 border border-border">
                <div className="flex items-center gap-2">
                  <Input
                    placeholder="Digite sua mensagem..."
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={isLoading}
                    className="flex-1"
                  />
                  <Button
                    onClick={handleSendMessage}
                    disabled={isLoading || !inputMessage.trim()}
                    className="bg-blue-600 hover:bg-blue-700 text-white"
                  >
                    {isLoading ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Send className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </div>

              {/* Footer */}
              <div className="text-center mt-4">
                <p className="text-sm text-muted-foreground">
                  powered by <span className="font-medium">ness<span className="text-[#00ade8]">.</span></span>
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  Inteligência Artificial pode cometer erros.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

export default Gabi_ChatSimple;