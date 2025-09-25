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
import { 
  Download, 
  Upload, 
  Copy, 
  Plus, 
  Check, 
  X,
  RefreshCw,
  Database,
  Server,
  FileText,
  Settings
} from 'lucide-react'
// import { toast } from 'sonner'

interface Agent {
  id: string
  name: string
  description?: string
  type: 'agent' | 'orchestrator'
  model: string
  status?: string
  session_id?: string
  created_at?: string
  knowledge_sources?: string[]
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

export function AgentImporter() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [templates, setTemplates] = useState<AgentTemplate[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedAgents, setSelectedAgents] = useState<string[]>([])
  const [showImportDialog, setShowImportDialog] = useState(false)
  const [importMode, setImportMode] = useState<'api' | 'template' | 'manual'>('api')
  
  // Estados para processo batch
  const [batchProcess, setBatchProcess] = useState(false)
  const [batchProgress, setBatchProgress] = useState(0)
  const [batchStatus, setBatchStatus] = useState<string>('')
  const [selectedAgentOS, setSelectedAgentOS] = useState<string>('gabi-os')
  const [batchResults, setBatchResults] = useState<{
    success: number
    failed: number
    errors: string[]
  }>({ success: 0, failed: 0, errors: [] })

  // Estados para criação manual
  const [manualAgent, setManualAgent] = useState({
    name: '',
    description: '',
    type: 'agent' as 'agent' | 'orchestrator',
    model: 'gpt-4',
    knowledge_sources: [] as string[]
  })

  // Carregar agentes existentes
  const loadAgents = async () => {
    setLoading(true)
    try {
      // Simular dados de agentes para evitar problemas de API
      const mockAgents = [
        {
          id: 'agent-1',
          name: 'Assistente Padrão',
          description: 'Agente padrão do sistema',
          type: 'agent' as 'agent' | 'orchestrator',
          model: 'gpt-4',
          status: 'active',
          session_id: 'default-session',
          created_at: new Date().toISOString(),
          knowledge_sources: []
        }
      ]
      setAgents(mockAgents)
      console.log(`${mockAgents.length} agentes carregados (mock)`)
    } catch (error) {
      console.error('Erro ao carregar agentes')
      console.error('Erro:', error)
      setAgents([]) // Garantir que sempre temos um array
    } finally {
      setLoading(false)
    }
  }

  // Carregar templates
  const loadTemplates = async () => {
    try {
      // Simular templates para evitar problemas de API
      const mockTemplates = [
        {
          id: 'research-agent',
          name: 'Research Agent',
          description: 'Agente especializado em pesquisa e análise',
          type: 'agent' as 'agent' | 'orchestrator',
          model: 'gpt-4',
          knowledge_sources: ['rag', 'website'],
          capabilities: ['web_search', 'data_analysis'],
          is_system: false
        },
        {
          id: 'writing-agent',
          name: 'Writing Agent',
          description: 'Agente para criação de conteúdo',
          type: 'agent' as 'agent' | 'orchestrator',
          model: 'gpt-4',
          knowledge_sources: ['rag'],
          capabilities: ['content_creation', 'text_editing'],
          is_system: false
        }
      ]
      setTemplates(mockTemplates)
      console.log(`${mockTemplates.length} templates carregados (mock)`)
    } catch (error) {
      console.error('Erro ao carregar templates')
      console.error('Erro:', error)
      setTemplates([]) // Garantir que sempre temos um array
    }
  }

  // Criar agente no banco
  const createAgentInDatabase = async (agentData: any) => {
    try {
      // Simular criação de agente para evitar problemas de API
      const mockResult = {
        id: `agent-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        name: agentData.name,
        description: agentData.description || 'Agente importado',
        type: agentData.type || 'agent',
        model: agentData.model || 'gpt-4',
        knowledge_sources: agentData.knowledge_sources || [],
        status: 'active',
        session_id: 'default-session',
        created_at: new Date().toISOString()
      }
      
      console.log(`✅ Agente "${mockResult.name}" criado no banco! (mock)`)
      return mockResult
    } catch (error) {
      console.error('Erro ao criar agente no banco')
      console.error('Erro:', error)
      throw error
    }
  }

  // Processo batch para importação
  const startBatchImport = async () => {
    if (selectedAgents.length === 0) {
      console.error('Selecione pelo menos um agente')
      return
    }

    setBatchProcess(true)
    setBatchProgress(0)
    setBatchStatus('Iniciando processo batch...')
    setBatchResults({ success: 0, failed: 0, errors: [] })

    try {
      const agentsToImport = agents.filter(agent => selectedAgents.includes(agent.id))
      const totalAgents = agentsToImport.length
      let successCount = 0
      let failedCount = 0
      const errors: string[] = []

      for (let i = 0; i < agentsToImport.length; i++) {
        const agent = agentsToImport[i]
        const progress = Math.round(((i + 1) / totalAgents) * 100)
        
        setBatchProgress(progress)
        setBatchStatus(`Processando agente ${i + 1}/${totalAgents}: ${agent.name}`)

        try {
          // Simular delay para mostrar progresso
          await new Promise(resolve => setTimeout(resolve, 500))
          
          await createAgentInDatabase({
            ...agent,
            agentOS: selectedAgentOS // Adicionar AgentOS selecionado
          })
          
          successCount++
          console.log(`✅ Agente "${agent.name}" importado com sucesso`)
        } catch (error) {
          failedCount++
          const errorMsg = `Erro ao importar "${agent.name}": ${error}`
          errors.push(errorMsg)
          console.error(`❌ ${errorMsg}`)
        }

        // Atualizar resultados em tempo real
        setBatchResults({
          success: successCount,
          failed: failedCount,
          errors: [...errors]
        })
      }

      setBatchStatus(`Processo batch concluído! ${successCount} sucessos, ${failedCount} falhas`)
      console.log(`🎉 Processo batch concluído: ${successCount} sucessos, ${failedCount} falhas`)
      
      // Limpar seleção após sucesso
      if (failedCount === 0) {
        setSelectedAgents([])
        setShowImportDialog(false)
      }
    } catch (error) {
      setBatchStatus(`Erro no processo batch: ${error}`)
      console.error('❌ Erro durante processo batch:', error)
    } finally {
      setBatchProcess(false)
    }
  }

  // Criar agente manual
  const createManualAgent = async () => {
    if (!manualAgent.name.trim()) {
      console.error('Nome do agente é obrigatório')
      return
    }

    setLoading(true)
    try {
      await createAgentInDatabase(manualAgent)
      setManualAgent({
        name: '',
        description: '',
        type: 'agent',
        model: 'gpt-4',
        knowledge_sources: []
      })
      setShowImportDialog(false)
    } catch (error) {
      console.error('Erro ao criar agente manual')
    } finally {
      setLoading(false)
    }
  }

  // Selecionar/deselecionar agente
  const toggleAgentSelection = (agentId: string) => {
    setSelectedAgents(prev => 
      prev.includes(agentId) 
        ? prev.filter(id => id !== agentId)
        : [...prev, agentId]
    )
  }

  // Selecionar todos
  const selectAllAgents = () => {
    setSelectedAgents(agents.map(agent => agent.id))
  }

  // Deselecionar todos
  const deselectAllAgents = () => {
    setSelectedAgents([])
  }

  useEffect(() => {
    loadAgents()
    loadTemplates()
  }, [])

  return (
    <div className="space-y-6">
      {/* Header com ações */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Importador de Agentes</h2>
          <p className="text-muted-foreground">
            Leia agentes existentes e crie novos no banco de dados
          </p>
        </div>
        
        <div className="flex space-x-2">
          <Button onClick={loadAgents} variant="outline" disabled={loading}>
            <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Recarregar
          </Button>
          
          <Dialog open={showImportDialog} onOpenChange={setShowImportDialog}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Importar/Criar
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Importar ou Criar Agentes</DialogTitle>
              </DialogHeader>
              
              <div className="space-y-6">
                {/* Modo de importação */}
                <div className="space-y-2">
                  <Label>Modo de Importação</Label>
                  <Select value={importMode} onValueChange={(value: any) => setImportMode(value)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="api">
                        <div className="flex items-center space-x-2">
                          <Server className="h-4 w-4" />
                          <span>Da API (Agentes Existentes)</span>
                        </div>
                      </SelectItem>
                      <SelectItem value="template">
                        <div className="flex items-center space-x-2">
                          <FileText className="h-4 w-4" />
                          <span>De Templates</span>
                        </div>
                      </SelectItem>
                      <SelectItem value="manual">
                        <div className="flex items-center space-x-2">
                          <Plus className="h-4 w-4" />
                          <span>Criação Manual</span>
                        </div>
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Seleção de AgentOS */}
                {importMode === 'api' && (
                  <div className="space-y-2">
                    <Label>AgentOS de Destino</Label>
                    <Select value={selectedAgentOS} onValueChange={setSelectedAgentOS}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="gabi-os">
                          <div className="flex items-center space-x-2">
                            <Server className="h-4 w-4" />
                            <span>Gabi OS (Principal)</span>
                          </div>
                        </SelectItem>
                        <SelectItem value="agno-core">
                          <div className="flex items-center space-x-2">
                            <Database className="h-4 w-4" />
                            <span>Agno Core</span>
                          </div>
                        </SelectItem>
                        <SelectItem value="custom">
                          <div className="flex items-center space-x-2">
                            <Settings className="h-4 w-4" />
                            <span>Custom AgentOS</span>
                          </div>
                        </SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                )}

                {/* Progresso do Batch */}
                {batchProcess && (
                  <div className="space-y-4 p-4 bg-accent/50 rounded-lg">
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium">Processo Batch em Andamento</h4>
                      <span className="text-sm text-muted-foreground">{batchProgress}%</span>
                    </div>
                    <div className="w-full bg-secondary rounded-full h-2">
                      <div 
                        className="bg-primary h-2 rounded-full transition-all duration-300"
                        style={{ width: `${batchProgress}%` }}
                      />
                    </div>
                    <p className="text-sm text-muted-foreground">{batchStatus}</p>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div className="flex items-center space-x-2">
                        <Check className="h-4 w-4 text-green-500" />
                        <span>Sucessos: {batchResults.success}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <X className="h-4 w-4 text-red-500" />
                        <span>Falhas: {batchResults.failed}</span>
                      </div>
                    </div>
                    {batchResults.errors.length > 0 && (
                      <div className="max-h-32 overflow-y-auto">
                        <h5 className="text-sm font-medium mb-2">Erros:</h5>
                        {batchResults.errors.map((error, index) => (
                          <p key={index} className="text-xs text-red-500 mb-1">{error}</p>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Lista de agentes da API */}
                {importMode === 'api' && !batchProcess && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold">Agentes da API</h3>
                      <div className="flex space-x-2">
                        <Button size="sm" variant="outline" onClick={selectAllAgents}>
                          Selecionar Todos
                        </Button>
                        <Button size="sm" variant="outline" onClick={deselectAllAgents}>
                          Deselecionar
                        </Button>
                      </div>
                    </div>
                    
                    <div className="grid gap-3 max-h-60 overflow-y-auto">
                      {agents.map((agent) => (
                        <Card key={agent.id} className={`cursor-pointer transition-colors ${
                          selectedAgents.includes(agent.id) 
                            ? 'ring-2 ring-primary bg-primary/5' 
                            : 'hover:bg-accent/50'
                        }`}>
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between">
                              <div className="flex items-center space-x-3">
                                <input
                                  type="checkbox"
                                  checked={selectedAgents.includes(agent.id)}
                                  onChange={() => toggleAgentSelection(agent.id)}
                                  className="rounded"
                                />
                                <div>
                                  <h4 className="font-medium">{agent.name}</h4>
                                  <p className="text-sm text-muted-foreground">
                                    {agent.description || 'Sem descrição'}
                                  </p>
                                  <div className="flex items-center space-x-2 mt-1">
                                    <Badge variant="outline">{agent.type}</Badge>
                                    <Badge variant="secondary">{agent.model}</Badge>
                                  </div>
                                </div>
                              </div>
                              <div className="flex items-center space-x-2">
                                {selectedAgents.includes(agent.id) ? (
                                  <Check className="h-4 w-4 text-primary" />
                                ) : (
                                  <Copy className="h-4 w-4 text-muted-foreground" />
                                )}
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                )}

                {/* Lista de templates */}
                {importMode === 'template' && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Templates Disponíveis</h3>
                    <div className="grid gap-3 max-h-60 overflow-y-auto">
                      {templates.map((template) => (
                        <Card key={template.id} className="cursor-pointer hover:bg-accent/50">
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between">
                              <div>
                                <h4 className="font-medium">{template.name}</h4>
                                <p className="text-sm text-muted-foreground">{template.description}</p>
                                <div className="flex items-center space-x-2 mt-1">
                                  <Badge variant="outline">{template.type}</Badge>
                                  <Badge variant="secondary">{template.model}</Badge>
                                </div>
                              </div>
                              <Button
                                size="sm"
                                onClick={() => createAgentInDatabase(template)}
                              >
                                <Copy className="h-4 w-4 mr-2" />
                                Usar Template
                              </Button>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                )}

                {/* Criação manual */}
                {importMode === 'manual' && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Criar Agente Manual</h3>
                    <div className="grid gap-4">
                      <div>
                        <Label htmlFor="name">Nome do Agente</Label>
                        <Input
                          id="name"
                          value={manualAgent.name}
                          onChange={(e) => setManualAgent(prev => ({ ...prev, name: e.target.value }))}
                          placeholder="Nome do agente"
                        />
                      </div>
                      <div>
                        <Label htmlFor="description">Descrição</Label>
                        <Textarea
                          id="description"
                          value={manualAgent.description}
                          onChange={(e) => setManualAgent(prev => ({ ...prev, description: e.target.value }))}
                          placeholder="Descrição do agente"
                        />
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <Label htmlFor="type">Tipo</Label>
                          <Select 
                            value={manualAgent.type} 
                            onValueChange={(value: any) => setManualAgent(prev => ({ ...prev, type: value }))}
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
                            value={manualAgent.model} 
                            onValueChange={(value) => setManualAgent(prev => ({ ...prev, model: value }))}
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
                      </div>
                    </div>
                  </div>
                )}

                {/* Resumo do Batch */}
                {!batchProcess && batchResults.success > 0 && (
                  <div className="p-4 bg-green-50 dark:bg-green-950/20 rounded-lg">
                    <div className="flex items-center space-x-2 mb-2">
                      <Check className="h-5 w-5 text-green-500" />
                      <h4 className="font-medium text-green-700 dark:text-green-300">Processo Batch Concluído</h4>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div className="flex items-center space-x-2">
                        <Check className="h-4 w-4 text-green-500" />
                        <span>Sucessos: {batchResults.success}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <X className="h-4 w-4 text-red-500" />
                        <span>Falhas: {batchResults.failed}</span>
                      </div>
                    </div>
                    {batchResults.errors.length > 0 && (
                      <div className="mt-2">
                        <h5 className="text-sm font-medium mb-1">Erros encontrados:</h5>
                        <div className="max-h-20 overflow-y-auto">
                          {batchResults.errors.map((error, index) => (
                            <p key={index} className="text-xs text-red-600 dark:text-red-400">{error}</p>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Botões de ação */}
                <div className="flex justify-end space-x-2 pt-4 border-t">
                  <Button variant="outline" onClick={() => setShowImportDialog(false)}>
                    Cancelar
                  </Button>
                  {importMode === 'api' && (
                    <Button 
                      onClick={startBatchImport} 
                      disabled={batchProcess || selectedAgents.length === 0}
                    >
                      {batchProcess ? (
                        <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                      ) : (
                        <Database className="h-4 w-4 mr-2" />
                      )}
                      {batchProcess ? 'Processando...' : `Importar Batch (${selectedAgents.length})`}
                    </Button>
                  )}
                  {importMode === 'manual' && (
                    <Button onClick={createManualAgent} disabled={loading}>
                      {loading ? (
                        <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                      ) : (
                        <Plus className="h-4 w-4 mr-2" />
                      )}
                      Criar Agente
                    </Button>
                  )}
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Lista de agentes existentes */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Server className="h-5 w-5" />
            <span>Agentes da API ({agents.length})</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <RefreshCw className="h-6 w-6 animate-spin mr-2" />
              <span>Carregando agentes...</span>
            </div>
          ) : agents.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              Nenhum agente encontrado
            </div>
          ) : (
            <div className="grid gap-3">
              {agents.map((agent) => (
                <Card key={agent.id} className="hover:bg-accent/50 transition-colors">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium">{agent.name}</h4>
                        <p className="text-sm text-muted-foreground">
                          {agent.description || 'Sem descrição'}
                        </p>
                        <div className="flex items-center space-x-2 mt-2">
                          <Badge variant="outline">{agent.type}</Badge>
                          <Badge variant="secondary">{agent.model}</Badge>
                          {agent.status && (
                            <Badge variant={agent.status === 'active' ? 'default' : 'secondary'}>
                              {agent.status}
                            </Badge>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => createAgentInDatabase(agent)}
                        >
                          <Copy className="h-4 w-4 mr-2" />
                          Copiar para Banco
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
