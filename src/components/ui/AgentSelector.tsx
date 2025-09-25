'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { CheckCircle, Circle, Bot, Users, Brain, PenTool, BarChart3, Settings } from 'lucide-react'
import { toast } from 'sonner'

interface Agent {
  id: string
  name: string
  description: string
  type: 'agent' | 'orchestrator'
  model: string
  status: string
  capabilities?: string[]
}

interface AgentSelectorProps {
  onAgentsSelected?: (selectedAgents: Agent[]) => void
  maxAgents?: number
  maxOrchestrators?: number
}

const agentIcons = {
  'assistant-agent': Bot,
  'research-agent': Brain,
  'writer-agent': PenTool,
  'analyst-agent': BarChart3,
  'orchestrator-agent': Settings
}

export function AgentSelector({ 
  onAgentsSelected, 
  maxAgents = 10, 
  maxOrchestrators = 10 
}: AgentSelectorProps) {
  const [agents, setAgents] = useState<Agent[]>([])
  const [selectedAgents, setSelectedAgents] = useState<Agent[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadAgents()
    loadSelectedAgents()
  }, [])

  const loadSelectedAgents = () => {
    const saved = localStorage.getItem('selectedAgents')
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        setSelectedAgents(parsed)
        onAgentsSelected?.(parsed)
      } catch (error) {
        console.error('Erro ao carregar agentes selecionados:', error)
      }
    }
  }

  const loadAgents = async () => {
    try {
      setIsLoading(true)
      console.log('Carregando agentes...')
      const response = await fetch('http://localhost:7777/agents')
      console.log('Response status:', response.status)
      if (response.ok) {
        const agentsData = await response.json()
        console.log('Agentes carregados:', agentsData)
        setAgents(agentsData)
      } else {
        // Fallback para agentes mockup se a API não estiver disponível
        console.log('Usando agentes mockup...')
        setAgents([
          {
            id: 'assistant-agent',
            name: 'Assistente Geral',
            description: 'Agente assistente para tarefas gerais e conversação',
            type: 'agent',
            model: 'gpt-4',
            status: 'active',
            capabilities: ['conversation', 'general_help', 'information']
          },
          {
            id: 'research-agent',
            name: 'Pesquisador',
            description: 'Agente especializado em pesquisa e análise de dados',
            type: 'agent',
            model: 'gpt-4',
            status: 'active',
            capabilities: ['web_search', 'data_analysis', 'research']
          },
          {
            id: 'writer-agent',
            name: 'Escritor',
            description: 'Agente especializado em criação de conteúdo e redação',
            type: 'agent',
            model: 'gpt-4',
            status: 'active',
            capabilities: ['content_creation', 'writing', 'editing']
          },
          {
            id: 'analyst-agent',
            name: 'Analista',
            description: 'Agente especializado em análise de dados e insights',
            type: 'agent',
            model: 'gpt-4',
            status: 'active',
            capabilities: ['data_analysis', 'insights', 'statistics']
          },
          {
            id: 'orchestrator-agent',
            name: 'Orquestrador',
            description: 'Agente coordenador que gerencia outros agentes',
            type: 'orchestrator',
            model: 'gpt-4',
            status: 'active',
            capabilities: ['coordination', 'management', 'synthesis']
          }
        ])
      }
    } catch (error) {
      console.error('Erro ao carregar agentes:', error)
      toast.error('Erro ao carregar agentes')
    } finally {
      setIsLoading(false)
    }
  }

  const toggleAgent = (agent: Agent) => {
    const isSelected = selectedAgents.some(selected => selected.id === agent.id)
    
    let newSelectedAgents
    if (isSelected) {
      newSelectedAgents = selectedAgents.filter(selected => selected.id !== agent.id)
    } else {
      newSelectedAgents = [...selectedAgents, agent]
    }
    
    setSelectedAgents(newSelectedAgents)
    
    // Salvar automaticamente no localStorage
    localStorage.setItem('selectedAgents', JSON.stringify(newSelectedAgents))
    
    // Notificar o componente pai
    onAgentsSelected?.(newSelectedAgents)
  }

  const handleConfirmSelection = () => {
    if (selectedAgents.length === 0) {
      toast.error('Selecione pelo menos um agente')
      return
    }
    
    onAgentsSelected?.(selectedAgents)
    toast.success(`${selectedAgents.length} agente(s) selecionado(s)`)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Carregando agentes...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-lg font-semibold mb-2">Selecionar Agentes</h3>
        <p className="text-sm text-muted-foreground">
          Selecione os agentes que deseja usar
        </p>
        <div className="flex items-center justify-center gap-4 mt-4">
          <Badge variant="outline">
            {selectedAgents.filter(a => a.type === 'agent').length} Agentes
          </Badge>
          <Badge variant="outline">
            {selectedAgents.filter(a => a.type === 'orchestrator').length} Orquestradores
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {agents.map((agent) => {
          const isSelected = selectedAgents.some(selected => selected.id === agent.id)
          const Icon = agentIcons[agent.id as keyof typeof agentIcons] || Bot
          
          return (
            <Card 
              key={agent.id}
              className={`cursor-pointer transition-all duration-200 ${
                isSelected 
                  ? 'ring-2 ring-primary bg-primary/5' 
                  : 'hover:shadow-md'
              }`}
              onClick={() => toggleAgent(agent)}
            >
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 rounded-md bg-primary/10">
                    <Icon className="h-4 w-4 text-primary" />
                  </div>
                  <div>
                    <CardTitle className="text-sm">{agent.name}</CardTitle>
                    <Badge 
                      variant={agent.type === 'orchestrator' ? 'default' : 'secondary'}
                      className="text-xs"
                    >
                      {agent.type === 'orchestrator' ? 'Orquestrador' : 'Agente'}
                    </Badge>
                  </div>
                </div>
                <div className="flex items-center">
                  {isSelected ? (
                    <CheckCircle className="h-4 w-4 text-primary" />
                  ) : (
                    <Circle className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
              </div>
            </CardHeader>
            <CardContent className="pt-0">
              <p className="text-xs text-muted-foreground mb-2 line-clamp-2">
                {agent.description}
              </p>
              <div className="flex flex-wrap gap-1">
                {agent.capabilities?.slice(0, 2).map((capability) => (
                  <Badge key={capability} variant="outline" className="text-xs">
                    {capability}
                  </Badge>
                ))}
                {agent.capabilities && agent.capabilities.length > 2 && (
                  <Badge variant="outline" className="text-xs">
                    +{agent.capabilities.length - 2}
                  </Badge>
                )}
              </div>
            </CardContent>
            </Card>
          )
        })}
      </div>

      {selectedAgents.length > 0 && (
        <div className="flex justify-center">
          <Button onClick={handleConfirmSelection} className="w-full max-w-md">
            Confirmar Seleção ({selectedAgents.length} agente(s))
          </Button>
        </div>
      )}
    </div>
  )
}
