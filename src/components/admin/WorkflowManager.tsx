'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Workflow, 
  Users, 
  Play, 
  Pause, 
  Square, 
  Plus, 
  Trash2, 
  Settings,
  CheckCircle,
  Clock,
  AlertCircle
} from 'lucide-react'
import { toast } from 'sonner'

interface WorkflowTemplate {
  id: string
  name: string
  description: string
  type: string
  agents: Array<{
    name: string
    type: string
    model: string
    description: string
    capabilities: string[]
  }>
  sequence: Array<{
    step: number
    agent: string
    action: string
  }>
}

interface WorkflowInstance {
  id: string
  template_id: string
  session_id: string
  name: string
  description: string
  type: string
  agents: any[]
  sequence: any[]
  status: string
  created_at: string
  custom_config: any
}

export function WorkflowManager() {
  const [templates, setTemplates] = useState<WorkflowTemplate[]>([])
  const [workflows, setWorkflows] = useState<WorkflowInstance[]>([])
  const [selectedTemplate, setSelectedTemplate] = useState<string>('')
  const [sessionId, setSessionId] = useState<string>('')
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingTemplates, setIsLoadingTemplates] = useState(true)

  // Carregar templates de workflow
  useEffect(() => {
    loadWorkflowTemplates()
  }, [])

  const loadWorkflowTemplates = async () => {
    try {
      setIsLoadingTemplates(true)
      const response = await fetch('http://localhost:7777/workflows/templates')
      if (response.ok) {
        const data = await response.json()
        setTemplates(data)
      } else {
        toast.error('Erro ao carregar templates de workflow')
      }
    } catch (error) {
      console.error('Erro ao carregar templates:', error)
      toast.error('Erro de conexão ao carregar templates')
    } finally {
      setIsLoadingTemplates(false)
    }
  }

  const loadWorkflows = async () => {
    try {
      const response = await fetch('http://localhost:7777/workflows/')
      if (response.ok) {
        const data = await response.json()
        setWorkflows(data)
      } else {
        toast.error('Erro ao carregar workflows')
      }
    } catch (error) {
      console.error('Erro ao carregar workflows:', error)
      toast.error('Erro de conexão ao carregar workflows')
    }
  }

  const createWorkflow = async () => {
    if (!selectedTemplate || !sessionId.trim()) {
      toast.error('Selecione um template e insira um ID de sessão')
      return
    }

    try {
      setIsLoading(true)
      const response = await fetch('http://localhost:7777/workflows/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template_id: selectedTemplate,
          session_id: sessionId.trim(),
          custom_config: {}
        })
      })

      if (response.ok) {
        const data = await response.json()
        toast.success(`Workflow "${data.name}" criado com sucesso!`)
        setSelectedTemplate('')
        setSessionId('')
        loadWorkflows()
      } else {
        const error = await response.json()
        toast.error(`Erro: ${error.detail}`)
      }
    } catch (error) {
      console.error('Erro ao criar workflow:', error)
      toast.error('Erro de conexão ao criar workflow')
    } finally {
      setIsLoading(false)
    }
  }

  const updateWorkflowStatus = async (workflowId: string, status: string) => {
    try {
      const response = await fetch(`http://localhost:7777/workflows/${workflowId}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status })
      })

      if (response.ok) {
        toast.success(`Status do workflow atualizado para ${status}`)
        loadWorkflows()
      } else {
        toast.error('Erro ao atualizar status do workflow')
      }
    } catch (error) {
      console.error('Erro ao atualizar status:', error)
      toast.error('Erro de conexão ao atualizar status')
    }
  }

  const deleteWorkflow = async (workflowId: string) => {
    try {
      const response = await fetch(`http://localhost:7777/workflows/${workflowId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        toast.success('Workflow removido com sucesso!')
        loadWorkflows()
      } else {
        toast.error('Erro ao remover workflow')
      }
    } catch (error) {
      console.error('Erro ao remover workflow:', error)
      toast.error('Erro de conexão ao remover workflow')
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case 'paused':
        return <Pause className="h-4 w-4 text-yellow-600" />
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-blue-600" />
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-600" />
      default:
        return <Clock className="h-4 w-4 text-gray-600" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'paused':
        return 'bg-yellow-100 text-yellow-800'
      case 'completed':
        return 'bg-blue-100 text-blue-800'
      case 'error':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Workflow className="h-5 w-5 text-purple-600" />
            Gerenciador de Workflows Agno
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="templates" className="space-y-4">
            <TabsList>
              <TabsTrigger value="templates">Templates</TabsTrigger>
              <TabsTrigger value="create">Criar Workflow</TabsTrigger>
              <TabsTrigger value="instances">Instâncias</TabsTrigger>
            </TabsList>

            <TabsContent value="templates">
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Templates de Workflow Disponíveis</h3>
                {isLoadingTemplates ? (
                  <div className="text-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
                    <p className="text-muted-foreground">Carregando templates...</p>
                  </div>
                ) : (
                  <div className="grid gap-4">
                    {templates.map((template) => (
                      <Card key={template.id} className="hover:shadow-md transition-shadow">
                        <CardHeader className="pb-3">
                          <div className="flex items-center justify-between">
                            <CardTitle className="text-lg">{template.name}</CardTitle>
                            <Badge variant="outline">{template.type}</Badge>
                          </div>
                          <p className="text-sm text-muted-foreground">{template.description}</p>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-3">
                            <div>
                              <h4 className="font-medium mb-2">Agentes ({template.agents.length})</h4>
                              <div className="space-y-1">
                                {template.agents.map((agent, index) => (
                                  <div key={index} className="flex items-center gap-2 text-sm">
                                    <Users className="h-3 w-3" />
                                    <span className="font-medium">{agent.name}</span>
                                    <Badge variant="secondary" className="text-xs">
                                      {agent.type}
                                    </Badge>
                                  </div>
                                ))}
                              </div>
                            </div>
                            <div>
                              <h4 className="font-medium mb-2">Sequência ({template.sequence.length} passos)</h4>
                              <div className="space-y-1">
                                {template.sequence.map((step, index) => (
                                  <div key={index} className="flex items-center gap-2 text-sm">
                                    <span className="w-6 h-6 rounded-full bg-primary text-primary-foreground text-xs flex items-center justify-center">
                                      {step.step}
                                    </span>
                                    <span>{step.agent}</span>
                                    <span className="text-muted-foreground">- {step.action}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </div>
            </TabsContent>

            <TabsContent value="create">
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Criar Novo Workflow</h3>
                <div className="grid gap-4">
                  <div>
                    <Label htmlFor="template">Template</Label>
                    <Select value={selectedTemplate} onValueChange={setSelectedTemplate}>
                      <SelectTrigger>
                        <SelectValue placeholder="Selecione um template" />
                      </SelectTrigger>
                      <SelectContent>
                        {templates.map((template) => (
                          <SelectItem key={template.id} value={template.id}>
                            {template.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <Label htmlFor="sessionId">ID da Sessão</Label>
                    <Input
                      id="sessionId"
                      placeholder="session-123"
                      value={sessionId}
                      onChange={(e) => setSessionId(e.target.value)}
                    />
                  </div>

                  <Button 
                    onClick={createWorkflow}
                    disabled={isLoading || !selectedTemplate || !sessionId.trim()}
                    className="w-full"
                  >
                    {isLoading ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Criando...
                      </>
                    ) : (
                      <>
                        <Plus className="h-4 w-4 mr-2" />
                        Criar Workflow
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="instances">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Workflows Ativos</h3>
                  <Button onClick={loadWorkflows} variant="outline" size="sm">
                    <Settings className="h-4 w-4 mr-2" />
                    Atualizar
                  </Button>
                </div>
                
                <div className="grid gap-4">
                  {workflows.map((workflow) => (
                    <Card key={workflow.id} className="hover:shadow-md transition-shadow">
                      <CardHeader className="pb-3">
                        <div className="flex items-center justify-between">
                          <CardTitle className="text-lg">{workflow.name}</CardTitle>
                          <div className="flex items-center gap-2">
                            {getStatusIcon(workflow.status)}
                            <Badge className={getStatusColor(workflow.status)}>
                              {workflow.status}
                            </Badge>
                          </div>
                        </div>
                        <p className="text-sm text-muted-foreground">{workflow.description}</p>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div className="flex items-center justify-between text-sm">
                            <span>Sessão: {workflow.session_id}</span>
                            <span>Criado: {new Date(workflow.created_at).toLocaleString()}</span>
                          </div>
                          
                          <div className="flex items-center gap-2">
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => updateWorkflowStatus(workflow.id, 'active')}
                              disabled={workflow.status === 'active'}
                            >
                              <Play className="h-3 w-3 mr-1" />
                              Iniciar
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => updateWorkflowStatus(workflow.id, 'paused')}
                              disabled={workflow.status === 'paused'}
                            >
                              <Pause className="h-3 w-3 mr-1" />
                              Pausar
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => updateWorkflowStatus(workflow.id, 'completed')}
                              disabled={workflow.status === 'completed'}
                            >
                              <Square className="h-3 w-3 mr-1" />
                              Finalizar
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => deleteWorkflow(workflow.id)}
                              className="text-red-600 hover:text-red-700"
                            >
                              <Trash2 className="h-3 w-3 mr-1" />
                              Remover
                            </Button>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                  
                  {workflows.length === 0 && (
                    <Card className="text-center py-8">
                      <CardContent>
                        <Workflow className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                        <h3 className="text-lg font-semibold mb-2">Nenhum workflow ativo</h3>
                        <p className="text-muted-foreground mb-4">
                          Crie um novo workflow para começar
                        </p>
                        <Button onClick={() => loadWorkflows()}>
                          <Settings className="h-4 w-4 mr-2" />
                          Atualizar Lista
                        </Button>
                      </CardContent>
                    </Card>
                  )}
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}
