'use client'

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Plus, Trash2, Bot, Users, Settings } from 'lucide-react'
import { toast } from 'sonner'

interface AgentTemplate {
  id: string
  name: string
  description: string
  model: string
  type: string
  knowledge_sources: string[]
}

interface AvailableModel {
  id: string
  name: string
  description: string
}

export function DynamicAgentCreator() {
  const [agentName, setAgentName] = useState('')
  const [agentDescription, setAgentDescription] = useState('')
  const [selectedModel, setSelectedModel] = useState('gpt-4')
  const [agentType, setAgentType] = useState('agent')
  const [knowledgeSources, setKnowledgeSources] = useState<string[]>([])
  const [availableModels, setAvailableModels] = useState<AvailableModel[]>([])
  const [templates, setTemplates] = useState<AgentTemplate[]>([])
  const [isCreating, setIsCreating] = useState(false)
  const [createdAgents, setCreatedAgents] = useState<any[]>([])

  useEffect(() => {
    loadAvailableModels()
    loadTemplates()
    loadCreatedAgents()
  }, [])

  const loadAvailableModels = async () => {
    try {
      const response = await fetch('http://localhost:7777/dynamic/available-models')
      const data = await response.json()
      setAvailableModels(data.models)
    } catch (error) {
      console.error('Erro ao carregar modelos:', error)
    }
  }

  const loadTemplates = async () => {
    try {
      const response = await fetch('http://localhost:7777/dynamic/agent-templates')
      const data = await response.json()
      setTemplates(data.templates)
    } catch (error) {
      console.error('Erro ao carregar templates:', error)
    }
  }

  const loadCreatedAgents = async () => {
    try {
      const response = await fetch('http://localhost:7777/agents')
      const data = await response.json()
      setCreatedAgents(data.agents || [])
    } catch (error) {
      console.error('Erro ao carregar agentes criados:', error)
    }
  }

  const handleCreateAgent = async () => {
    if (!agentName.trim()) {
      toast.error('Nome do agente é obrigatório')
      return
    }

    setIsCreating(true)
    try {
      const response = await fetch('http://localhost:7777/dynamic/create-agent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: agentName,
          description: agentDescription,
          model: selectedModel,
          agent_type: agentType,
          knowledge_sources: knowledgeSources
        })
      })

      if (response.ok) {
        const agent = await response.json()
        toast.success(`Agente "${agent.name}" criado com sucesso!`)
        setAgentName('')
        setAgentDescription('')
        setKnowledgeSources([])
        loadCreatedAgents()
      } else {
        const error = await response.json()
        toast.error(`Erro ao criar agente: ${error.detail}`)
      }
    } catch (error) {
      console.error('Erro ao criar agente:', error)
      toast.error('Erro ao criar agente')
    } finally {
      setIsCreating(false)
    }
  }

  const handleCreateFromTemplate = async (template: AgentTemplate) => {
    setIsCreating(true)
    try {
      const response = await fetch('http://localhost:7777/dynamic/create-from-template', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template_id: template.id,
          custom_name: `${template.name} Personalizado`
        })
      })

      if (response.ok) {
        const agent = await response.json()
        toast.success(`Agente "${agent.name}" criado do template!`)
        loadCreatedAgents()
      } else {
        const error = await response.json()
        toast.error(`Erro ao criar agente: ${error.detail}`)
      }
    } catch (error) {
      console.error('Erro ao criar agente do template:', error)
      toast.error('Erro ao criar agente do template')
    } finally {
      setIsCreating(false)
    }
  }

  const addKnowledgeSource = () => {
    const source = prompt('Digite a fonte de conhecimento:')
    if (source && !knowledgeSources.includes(source)) {
      setKnowledgeSources([...knowledgeSources, source])
    }
  }

  const removeKnowledgeSource = (source: string) => {
    setKnowledgeSources(knowledgeSources.filter(s => s !== source))
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            Criar Agente Dinâmico
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="agent-name">Nome do Agente</Label>
              <Input
                id="agent-name"
                value={agentName}
                onChange={(e) => setAgentName(e.target.value)}
                placeholder="Ex: Assistente de Vendas"
              />
            </div>
            <div>
              <Label htmlFor="agent-type">Tipo do Agente</Label>
              <Select value={agentType} onValueChange={setAgentType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="agent">
                    <div className="flex items-center gap-2">
                      <Bot className="h-4 w-4" />
                      Agente
                    </div>
                  </SelectItem>
                  <SelectItem value="orchestrator">
                    <div className="flex items-center gap-2">
                      <Users className="h-4 w-4" />
                      Orquestrador
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div>
            <Label htmlFor="agent-description">Descrição</Label>
            <Textarea
              id="agent-description"
              value={agentDescription}
              onChange={(e) => setAgentDescription(e.target.value)}
              placeholder="Descreva as capacidades e especialidades do agente..."
              rows={3}
            />
          </div>

          <div>
            <Label htmlFor="agent-model">Modelo de IA</Label>
            <Select value={selectedModel} onValueChange={setSelectedModel}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {availableModels.map((model) => (
                  <SelectItem key={model.id} value={model.id}>
                    <div>
                      <div className="font-medium">{model.name}</div>
                      <div className="text-sm text-muted-foreground">{model.description}</div>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label>Fontes de Conhecimento</Label>
            <div className="flex flex-wrap gap-2 mb-2">
              {knowledgeSources.map((source) => (
                <Badge key={source} variant="secondary" className="flex items-center gap-1">
                  {source}
                  <button
                    onClick={() => removeKnowledgeSource(source)}
                    className="ml-1 hover:text-destructive"
                  >
                    ×
                  </button>
                </Badge>
              ))}
            </div>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={addKnowledgeSource}
              className="w-full"
            >
              <Plus className="h-4 w-4 mr-2" />
              Adicionar Fonte de Conhecimento
            </Button>
          </div>

          <Button
            onClick={handleCreateAgent}
            disabled={isCreating || !agentName.trim()}
            className="w-full"
          >
            {isCreating ? 'Criando...' : 'Criar Agente'}
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Templates de Agentes
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {templates.map((template) => (
              <Card key={template.id} className="p-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <h3 className="font-medium">{template.name}</h3>
                    <Badge variant={template.type === 'orchestrator' ? 'default' : 'secondary'}>
                      {template.type === 'orchestrator' ? 'Orquestrador' : 'Agente'}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">{template.description}</p>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span>Modelo: {template.model}</span>
                    {template.knowledge_sources.length > 0 && (
                      <span>• Fontes: {template.knowledge_sources.join(', ')}</span>
                    )}
                  </div>
                  <Button
                    size="sm"
                    onClick={() => handleCreateFromTemplate(template)}
                    disabled={isCreating}
                    className="w-full"
                  >
                    Criar do Template
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            Agentes Criados
          </CardTitle>
        </CardHeader>
        <CardContent>
          {createdAgents.length === 0 ? (
            <p className="text-muted-foreground text-center py-4">
              Nenhum agente criado ainda
            </p>
          ) : (
            <div className="space-y-2">
              {createdAgents.map((agent) => (
                <div key={agent.id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <div className="font-medium">{agent.name}</div>
                    <div className="text-sm text-muted-foreground">{agent.description}</div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary">{agent.model}</Badge>
                    <Badge variant={agent.type === 'orchestrator' ? 'default' : 'outline'}>
                      {agent.type === 'orchestrator' ? 'Orquestrador' : 'Agente'}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
