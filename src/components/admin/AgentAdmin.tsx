'use client'

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Plus, 
  Edit, 
  Trash2, 
  Copy, 
  Play, 
  Pause, 
  Archive, 
  Settings,
  Activity,
  Users,
  Brain,
  Zap
} from 'lucide-react'
// import { toast } from 'sonner'

interface Agent {
  id: string
  name: string
  description: string
  type: 'agent' | 'orchestrator'
  model: string
  status: 'active' | 'inactive' | 'archived'
  session_id?: string
  created_at: string
}

interface AgentTemplate {
  id: string
  name: string
  description: string
  type: 'agent' | 'orchestrator'
  model: string
  knowledge_sources: string[]
  capabilities: string[]
}

interface AgentHealth {
  agent_id: string
  status: 'healthy' | 'warning' | 'error'
  last_check: string
  metrics: Record<string, any>
  issues: string[]
}

export function AgentAdmin() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [templates, setTemplates] = useState<AgentTemplate[]>([])
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [showEditDialog, setShowEditDialog] = useState(false)
  const [showTemplatesDialog, setShowTemplatesDialog] = useState(false)

  // Estados para formulários
  const [agentForm, setAgentForm] = useState({
    name: '',
    description: '',
    type: 'agent' as 'agent' | 'orchestrator',
    model: 'gpt-4',
    knowledge_sources: [] as string[]
  })

  const [cloneForm, setCloneForm] = useState({
    new_name: '',
    new_description: '',
    session_id: ''
  })

  // Carregar dados iniciais
  useEffect(() => {
    loadAgents()
    loadTemplates()
  }, [])

  const loadAgents = async () => {
    try {
      setIsLoading(true)
      const response = await fetch('/api/agents')
      if (response.ok) {
        const data = await response.json()
        setAgents(data)
      }
    } catch (error) {
      console.error('Erro ao carregar agentes')
    } finally {
      setIsLoading(false)
    }
  }

  const loadTemplates = async () => {
    try {
      const response = await fetch('/api/agents/templates')
      if (response.ok) {
        const data = await response.json()
        setTemplates(data)
      }
    } catch (error) {
      console.error('Erro ao carregar templates')
    }
  }

  const createAgent = async () => {
    try {
      const response = await fetch('/api/agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: `agent-${Date.now()}`,
          ...agentForm
        })
      })

      if (response.ok) {
        console.log('Agente criado com sucesso!')
        setShowCreateDialog(false)
        resetForm()
        loadAgents()
      } else {
        throw new Error('Erro ao criar agente')
      }
    } catch (error) {
      console.error('Erro ao criar agente')
    }
  }

  const updateAgent = async (agentId: string, updates: Partial<Agent>) => {
    try {
      const response = await fetch(`/api/agents/${agentId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
      })

      if (response.ok) {
        console.log('Agente atualizado com sucesso!')
        setShowEditDialog(false)
        loadAgents()
      } else {
        throw new Error('Erro ao atualizar agente')
      }
    } catch (error) {
      console.error('Erro ao atualizar agente')
    }
  }

  const deleteAgent = async (agentId: string) => {
    try {
      const response = await fetch(`/api/agents/${agentId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        console.log('Agente removido com sucesso!')
        loadAgents()
      } else {
        throw new Error('Erro ao remover agente')
      }
    } catch (error) {
      console.error('Erro ao remover agente')
    }
  }

  const cloneAgent = async (agentId: string) => {
    try {
      const response = await fetch(`/api/agents/${agentId}/clone`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cloneForm)
      })

      if (response.ok) {
        console.log('Agente clonado com sucesso!')
        setShowEditDialog(false)
        resetCloneForm()
        loadAgents()
      } else {
        throw new Error('Erro ao clonar agente')
      }
    } catch (error) {
      console.error('Erro ao clonar agente')
    }
  }

  const createFromTemplate = async (templateId: string, customName: string) => {
    try {
      const response = await fetch('/api/agents/from-template', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          template_id: templateId,
          session_id: 'default-session',
          custom_name: customName
        })
      })

      if (response.ok) {
        console.log('Agente criado do template com sucesso!')
        setShowTemplatesDialog(false)
        loadAgents()
      } else {
        throw new Error('Erro ao criar agente do template')
      }
    } catch (error) {
      console.error('Erro ao criar agente do template')
    }
  }

  const restartAgent = async (agentId: string) => {
    try {
      const response = await fetch(`/api/agents/${agentId}/restart`, {
        method: 'POST'
      })

      if (response.ok) {
        console.log('Agente reiniciado com sucesso!')
        loadAgents()
      } else {
        throw new Error('Erro ao reiniciar agente')
      }
    } catch (error) {
      console.error('Erro ao reiniciar agente')
    }
  }

  const archiveAgent = async (agentId: string) => {
    try {
      const response = await fetch(`/api/agents/${agentId}/archive`, {
        method: 'POST'
      })

      if (response.ok) {
        console.log('Agente arquivado com sucesso!')
        loadAgents()
      } else {
        throw new Error('Erro ao arquivar agente')
      }
    } catch (error) {
      console.error('Erro ao arquivar agente')
    }
  }

  const resetForm = () => {
    setAgentForm({
      name: '',
      description: '',
      type: 'agent',
      model: 'gpt-4',
      knowledge_sources: []
    })
  }

  const resetCloneForm = () => {
    setCloneForm({
      new_name: '',
      new_description: '',
      session_id: ''
    })
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500'
      case 'inactive': return 'bg-yellow-500'
      case 'archived': return 'bg-gray-500'
      default: return 'bg-gray-500'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Ativo'
      case 'inactive': return 'Inativo'
      case 'archived': return 'Arquivado'
      default: return 'Desconhecido'
    }
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Administração de Agentes</h1>
          <p className="text-muted-foreground">Gerencie e monitore seus agentes de IA</p>
        </div>
        
        <div className="flex gap-2">
          <Dialog open={showTemplatesDialog} onOpenChange={setShowTemplatesDialog}>
            <DialogTrigger asChild>
              <Button variant="outline">
                <Brain className="h-4 w-4 mr-2" />
                Templates
              </Button>
            </DialogTrigger>
          </Dialog>

          <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Novo Agente
              </Button>
            </DialogTrigger>
          </Dialog>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Users className="h-4 w-4 text-blue-500" />
              <div>
                <p className="text-sm font-medium">Total</p>
                <p className="text-2xl font-bold">{agents.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Activity className="h-4 w-4 text-green-500" />
              <div>
                <p className="text-sm font-medium">Ativos</p>
                <p className="text-2xl font-bold">
                  {agents.filter(a => a.status === 'active').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Zap className="h-4 w-4 text-yellow-500" />
              <div>
                <p className="text-sm font-medium">Orquestradores</p>
                <p className="text-2xl font-bold">
                  {agents.filter(a => a.type === 'orchestrator').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Brain className="h-4 w-4 text-purple-500" />
              <div>
                <p className="text-sm font-medium">Templates</p>
                <p className="text-2xl font-bold">{templates.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Agents List */}
      <Card>
        <CardHeader>
          <CardTitle>Agentes</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="text-center py-8">Carregando...</div>
          ) : (
            <div className="space-y-4">
              {agents.map((agent) => (
                <div key={agent.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-brand-blue rounded-lg flex items-center justify-center">
                      <Brain className="h-5 w-5 text-white" />
                    </div>
                    <div>
                      <h3 className="font-medium">{agent.name}</h3>
                      <p className="text-sm text-muted-foreground">{agent.description}</p>
                      <div className="flex items-center space-x-2 mt-1">
                        <Badge variant="outline">{agent.type}</Badge>
                        <Badge className={getStatusColor(agent.status)}>
                          {getStatusText(agent.status)}
                        </Badge>
                        <span className="text-xs text-muted-foreground">{agent.model}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        setSelectedAgent(agent)
                        setShowEditDialog(true)
                      }}
                    >
                      <Edit className="h-4 w-4" />
                    </Button>
                    
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        setSelectedAgent(agent)
                        cloneAgent(agent.id)
                      }}
                    >
                      <Copy className="h-4 w-4" />
                    </Button>

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => restartAgent(agent.id)}
                    >
                      <Play className="h-4 w-4" />
                    </Button>

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => archiveAgent(agent.id)}
                    >
                      <Archive className="h-4 w-4" />
                    </Button>

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => deleteAgent(agent.id)}
                      className="text-red-500 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}

              {agents.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  Nenhum agente encontrado
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Create Agent Dialog */}
      <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Criar Novo Agente</DialogTitle>
          </DialogHeader>
          
          <div className="space-y-4">
            <div>
              <Label htmlFor="name">Nome</Label>
              <Input
                id="name"
                value={agentForm.name}
                onChange={(e) => setAgentForm({ ...agentForm, name: e.target.value })}
                placeholder="Nome do agente"
              />
            </div>

            <div>
              <Label htmlFor="description">Descrição</Label>
              <Textarea
                id="description"
                value={agentForm.description}
                onChange={(e) => setAgentForm({ ...agentForm, description: e.target.value })}
                placeholder="Descrição do agente"
              />
            </div>

            <div>
              <Label htmlFor="type">Tipo</Label>
              <Select
                value={agentForm.type}
                onValueChange={(value: 'agent' | 'orchestrator') => 
                  setAgentForm({ ...agentForm, type: value })
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="agent">Agente</SelectItem>
                  <SelectItem value="orchestrator">Orquestrador</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="model">Modelo</Label>
              <Select
                value={agentForm.model}
                onValueChange={(value) => setAgentForm({ ...agentForm, model: value })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="gpt-4">GPT-4</SelectItem>
                  <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
                  <SelectItem value="claude-3">Claude 3</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex justify-end space-x-2">
              <Button variant="outline" onClick={() => setShowCreateDialog(false)}>
                Cancelar
              </Button>
              <Button onClick={createAgent}>
                Criar Agente
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Templates Dialog */}
      <Dialog open={showTemplatesDialog} onOpenChange={setShowTemplatesDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Criar Agente do Template</DialogTitle>
          </DialogHeader>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {templates.map((template) => (
              <Card key={template.id} className="cursor-pointer hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-brand-blue rounded-lg flex items-center justify-center">
                      <Brain className="h-4 w-4 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-medium">{template.name}</h3>
                      <p className="text-sm text-muted-foreground mb-2">{template.description}</p>
                      <div className="flex flex-wrap gap-1 mb-2">
                        {template.capabilities.map((cap) => (
                          <Badge key={cap} variant="outline" className="text-xs">
                            {cap}
                          </Badge>
                        ))}
                      </div>
                      <Button
                        size="sm"
                        onClick={() => createFromTemplate(template.id, template.name)}
                        className="w-full"
                      >
                        Criar do Template
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
