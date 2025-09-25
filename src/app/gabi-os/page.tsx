'use client'

import React, { useState, useEffect } from 'react'
import { MainLayout } from '@/components/layout/MainLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Server, Settings, Activity, Database, Users, CheckCircle, XCircle, Loader2, Plus, Trash2, FileText, Globe, Database as DbIcon, Link, Upload } from 'lucide-react'
import { AgentSelector } from '@/components/ui/AgentSelector'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { toast } from 'sonner'

export default function GabiOSPage() {
  const [agentOSUrl, setAgentOSUrl] = useState('')
  const [isConnected, setIsConnected] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingAgents, setIsLoadingAgents] = useState(false)
  const [agentOSData, setAgentOSData] = useState<any>(null)
  const [agents, setAgents] = useState<any[]>([])
  const [selectedAgents, setSelectedAgents] = useState<any[]>([])
  const [activeTab, setActiveTab] = useState('connection')
  
  // Estados para configurações runtime
  const [modelConfig, setModelConfig] = useState({
    provider: 'openai',
    model: 'gpt-5',
    temperature: 0.7,
    maxTokens: 4000
  })
  const [knowledgeConfig, setKnowledgeConfig] = useState({
    sources: [] as string[],
    ragEnabled: true,
    maxSources: 10,
    sourceTypes: [] as Array<{
      id: string,
      type: 'url' | 'sql' | 'document' | 'api' | 'file' | 'mcp',
      name: string,
      connection: string,
      config: any
    }>
  })
  const [toolsConfig, setToolsConfig] = useState({
    availableTools: ['web_search', 'calculator', 'file_reader', 'code_executor'],
    enabledTools: ['web_search', 'calculator'],
    customTools: [] as string[]
  })
  
  // Estados para MCP
  const [mcpTools, setMcpTools] = useState<any[]>([])
  const [isLoadingMcp, setIsLoadingMcp] = useState(false)

  const handleNewChat = () => {
    window.location.href = '/'
  }

  const handleSettings = () => {
    window.location.href = '/configuracoes'
  }

  const handleLogout = () => {
    console.log('Logout realizado')
  }

  const handleAgentsSelected = (agents: any[]) => {
    setSelectedAgents(agents)
    // Salvar agentes selecionados no localStorage
    localStorage.setItem('selectedAgents', JSON.stringify(agents))
    toast.success(`${agents.length} agente(s) selecionado(s) com sucesso!`)
  }

  const saveModelConfig = () => {
    localStorage.setItem('modelConfig', JSON.stringify(modelConfig))
    toast.success('Configurações de modelo salvas!')
  }

  const saveKnowledgeConfig = () => {
    localStorage.setItem('knowledgeConfig', JSON.stringify(knowledgeConfig))
    toast.success('Configurações de conhecimento salvas!')
  }

  const saveToolsConfig = () => {
    localStorage.setItem('toolsConfig', JSON.stringify(toolsConfig))
    toast.success('Configurações de ferramentas salvas!')
  }

  const addKnowledgeSource = (type: 'url' | 'sql' | 'document' | 'api' | 'file' | 'mcp') => {
    const newSource = {
      id: `source-${Date.now()}`,
      type,
      name: '',
      connection: '',
      config: {}
    }
    setKnowledgeConfig({
      ...knowledgeConfig,
      sourceTypes: [...knowledgeConfig.sourceTypes, newSource]
    })
  }

  const updateKnowledgeSource = (id: string, updates: any) => {
    setKnowledgeConfig({
      ...knowledgeConfig,
      sourceTypes: knowledgeConfig.sourceTypes.map(source => 
        source.id === id ? { ...source, ...updates } : source
      )
    })
  }

  const removeKnowledgeSource = (id: string) => {
    setKnowledgeConfig({
      ...knowledgeConfig,
      sourceTypes: knowledgeConfig.sourceTypes.filter(source => source.id !== id)
    })
  }

  // Função para carregar ferramentas MCP
  const loadMcpTools = async () => {
    setIsLoadingMcp(true)
    try {
      const response = await fetch('http://localhost:7777/mcp/tools')
      const data = await response.json()
      if (data.status === 'success') {
        setMcpTools(data.tools)
        toast.success(`${data.tools.length} ferramentas MCP carregadas!`)
      }
    } catch (error) {
      console.error('Erro ao carregar ferramentas MCP:', error)
      toast.error('Erro ao carregar ferramentas MCP')
    } finally {
      setIsLoadingMcp(false)
    }
  }

  const testConnection = async () => {
    if (!agentOSUrl.trim()) {
      toast.error('Por favor, insira uma URL válida')
      return
    }

    setIsLoading(true)
    try {
      const response = await fetch(`${agentOSUrl}/health`)
      if (response.ok) {
        const data = await response.json()
        setAgentOSData(data)
        setIsConnected(true)
        // Salvar automaticamente quando conectar
        localStorage.setItem('agentOSUrl', agentOSUrl)
        localStorage.setItem('agentOSConnected', 'true')
        localStorage.setItem('agentOSData', JSON.stringify(data))
        toast.success('Conexão estabelecida com sucesso!')
      } else {
        throw new Error('Falha na conexão')
      }
    } catch (error) {
      setIsConnected(false)
      setAgentOSData(null)
      toast.error('Falha ao conectar com o AgentOS')
    } finally {
      setIsLoading(false)
    }
  }

  const saveConfiguration = () => {
    if (isConnected && agentOSUrl) {
      localStorage.setItem('agentOSUrl', agentOSUrl)
      localStorage.setItem('agentOSConnected', 'true')
      localStorage.setItem('agentOSData', JSON.stringify(agentOSData))
      toast.success('Configuração salva com sucesso!')
    }
  }

  const loadAgents = async () => {
    if (!agentOSUrl || !isConnected) {
      toast.error('Configure e conecte ao AgentOS primeiro')
      return
    }

    setIsLoadingAgents(true)
    try {
      // Tentar diferentes endpoints comuns para listar agentes
      const endpoints = [
        `${agentOSUrl}/agents`,
        `${agentOSUrl}/api/agents`,
        `${agentOSUrl}/v1/agents`,
        `${agentOSUrl}/agentos/agents`
      ]

      let agentsData = []
      let success = false

      for (const endpoint of endpoints) {
        try {
          const response = await fetch(endpoint, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          })

          if (response.ok) {
            const data = await response.json()
            agentsData = Array.isArray(data) ? data : (data.agents || data.data || [])
            success = true
            break
          }
        } catch (error) {
          console.log(`Endpoint ${endpoint} falhou:`, error)
          continue
        }
      }

      if (success) {
        setAgents(agentsData)
        toast.success(`${agentsData.length} Gabi.OS carregados com sucesso!`)
      } else {
        // Tentar endpoint do backend Gabi
        try {
          const response = await fetch('http://localhost:7777/agents')
          if (response.ok) {
            const data = await response.json()
            setAgents(data)
            toast.success(`${data.length} Gabi.OS carregados do backend!`)
          } else {
            throw new Error('Backend não disponível')
          }
        } catch (error) {
          toast.error('Não foi possível carregar Gabi.OS. Verifique a conexão.')
        }
      }
    } catch (error) {
      console.error('Erro ao carregar agentes:', error)
      toast.error('Erro ao carregar agentes do AgentOS')
    } finally {
      setIsLoadingAgents(false)
    }
  }

  useEffect(() => {
    const savedUrl = localStorage.getItem('agentOSUrl')
    const savedConnected = localStorage.getItem('agentOSConnected')
    const savedData = localStorage.getItem('agentOSData')
    
    if (savedUrl) {
      setAgentOSUrl(savedUrl)
      
      if (savedConnected === 'true' && savedData) {
        try {
          const data = JSON.parse(savedData)
          setAgentOSData(data)
          setIsConnected(true)
        } catch (error) {
          // Se houver erro ao parsear, testar conexão
          testConnectionWithSavedUrl(savedUrl)
        }
      } else {
        // Testar conexão automaticamente se há URL salva
        testConnectionWithSavedUrl(savedUrl)
      }
    }

    // Carregar configurações salvas
    const savedModelConfig = localStorage.getItem('modelConfig')
    if (savedModelConfig) {
      try {
        setModelConfig(JSON.parse(savedModelConfig))
      } catch (error) {
        console.error('Erro ao carregar configurações de modelo:', error)
      }
    }

    const savedKnowledgeConfig = localStorage.getItem('knowledgeConfig')
    if (savedKnowledgeConfig) {
      try {
        setKnowledgeConfig(JSON.parse(savedKnowledgeConfig))
      } catch (error) {
        console.error('Erro ao carregar configurações de conhecimento:', error)
      }
    }

    const savedToolsConfig = localStorage.getItem('toolsConfig')
    if (savedToolsConfig) {
      try {
        setToolsConfig(JSON.parse(savedToolsConfig))
      } catch (error) {
        console.error('Erro ao carregar configurações de ferramentas:', error)
      }
    }
  }, [])

  const testConnectionWithSavedUrl = async (url: string) => {
    setIsLoading(true)
    try {
      const response = await fetch(`${url}/health`)
      if (response.ok) {
        const data = await response.json()
        setAgentOSData(data)
        setIsConnected(true)
      } else {
        setIsConnected(false)
        setAgentOSData(null)
      }
    } catch (error) {
      setIsConnected(false)
      setAgentOSData(null)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <MainLayout 
      pageTitle="Gabi.OS"
      onNewChat={handleNewChat}
      onSettings={handleSettings}
      onLogout={handleLogout}
    >
      <div className="p-6">
        <div className="mb-6">
          <p className="text-muted-foreground">
            Configure a conexão e selecione agentes para acessar Gabi<span className="text-[#00ade8]">.</span>OS
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="connection">Conexão</TabsTrigger>
            <TabsTrigger value="agents">Agentes</TabsTrigger>
            <TabsTrigger value="models">Modelos</TabsTrigger>
            <TabsTrigger value="knowledge">Conhecimento</TabsTrigger>
            <TabsTrigger value="tools">Ferramentas</TabsTrigger>
          </TabsList>

          <TabsContent value="connection" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Configuração do AgentOS */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Server className="h-5 w-5 text-blue-600" />
                Configuração
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="agentOSUrl">URL</Label>
                <Input
                  id="agentOSUrl"
                  type="url"
                  placeholder="https://seu-servidor.com"
                  value={agentOSUrl}
                  onChange={(e) => setAgentOSUrl(e.target.value)}
                  className="mt-1"
                />
              </div>
              
              <div className="flex gap-2">
                <Button 
                  onClick={testConnection}
                  disabled={isLoading || !agentOSUrl.trim()}
                  className="flex-1"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Testando...
                    </>
                  ) : (
                    <>
                      <Activity className="h-4 w-4 mr-2" />
                      Testar Conexão
                    </>
                  )}
                </Button>
                
                {isConnected && (
                  <Button 
                    onClick={saveConfiguration}
                    variant="outline"
                  >
                    <Settings className="h-4 w-4 mr-2" />
                    Salvar
                  </Button>
                )}
              </div>

              {/* Status da Conexão */}
              <div className="flex items-center gap-2">
                {isConnected ? (
                  <>
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span className="text-sm text-green-600">Conectado</span>
                  </>
                ) : (
                  <>
                    <XCircle className="h-4 w-4 text-red-600" />
                    <span className="text-sm text-red-600">Desconectado</span>
                  </>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Informações do AgentOS */}
          {isConnected && agentOSData && (
            <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5 text-green-600" />
                Informações
              </CardTitle>
            </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Status</span>
                    <Badge variant="default" className="bg-green-600">
                      {agentOSData.status || 'Online'}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Versão</span>
                    <span className="text-sm text-muted-foreground">
                      {agentOSData.version || 'N/A'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Agentes</span>
                    <span className="text-sm text-muted-foreground">
                      {agentOSData.agents_count || 0}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Sessões</span>
                    <span className="text-sm text-muted-foreground">
                      {agentOSData.sessions_count || 0}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Agentes Disponíveis */}
          {isConnected && (
            <Card className="lg:col-span-2">
              <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Users className="h-5 w-5 text-purple-600" />
                    Gabi<span className="text-[#00ade8]">.</span>OS Disponíveis
                    {agents.length > 0 && (
                      <Badge variant="secondary" className="ml-2">
                        {agents.length} Gabi<span className="text-[#00ade8]">.</span>OS
                      </Badge>
                    )}
                  </CardTitle>
              </CardHeader>
              <CardContent>
                {agents.length === 0 ? (
                  <div className="text-center py-8">
                    <Users className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-lg font-semibold mb-2">Gabi<span className="text-[#00ade8]">.</span>OS</h3>
                    <p className="text-muted-foreground mb-4">
                      Os Gabi<span className="text-[#00ade8]">.</span>OS disponíveis serão carregados do seu servidor configurado
                    </p>
                    <Button 
                      variant="outline" 
                      onClick={loadAgents}
                      disabled={isLoadingAgents}
                    >
                      {isLoadingAgents ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Carregando...
                        </>
                      ) : (
                        <>
                      <Activity className="h-4 w-4 mr-2" />
                          Carregar Gabi<span className="text-[#00ade8]">.</span>OS
                        </>
                      )}
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <p className="text-sm text-muted-foreground">
                            {agents.length} Gabi<span className="text-[#00ade8]">.</span>OS carregados do servidor
                          </p>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={loadAgents}
                        disabled={isLoadingAgents}
                      >
                        {isLoadingAgents ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          <Activity className="h-4 w-4" />
                        )}
                      </Button>
                    </div>
                    
                    <div className="overflow-x-auto">
                      <table className="w-full border-collapse">
                        <thead>
                          <tr className="border-b">
                            <th className="text-left p-3 font-medium">Nome</th>
                            <th className="text-left p-3 font-medium">Descrição</th>
                            <th className="text-left p-3 font-medium">Status</th>
                            <th className="text-left p-3 font-medium">Tipo</th>
                          </tr>
                        </thead>
                        <tbody>
                          {agents.map((agent) => (
                            <tr key={agent.id} className="border-b hover:bg-gray-50">
                              <td className="p-3 font-medium">{agent.name}</td>
                              <td className="p-3 text-sm text-muted-foreground">{agent.description}</td>
                              <td className="p-3">
                                <Badge 
                                  variant={agent.status === 'active' ? 'default' : 'secondary'}
                                  className={agent.status === 'active' ? 'bg-green-600' : ''}
                                >
                                  {agent.status}
                                </Badge>
                              </td>
                              <td className="p-3">
                                <Badge variant="outline" className="text-xs">
                                  {agent.type}
                                </Badge>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
            </div>
          </TabsContent>

          <TabsContent value="agents" className="space-y-6">
            <div className="space-y-6">
              <AgentSelector 
                onAgentsSelected={handleAgentsSelected}
                maxAgents={10}
                maxOrchestrators={10}
              />
              
            </div>
          </TabsContent>

          <TabsContent value="models" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Settings className="h-5 w-5 text-blue-600" />
                    Configuração de Modelo
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="modelProvider">Provedor</Label>
                    <select
                      id="modelProvider"
                      value={modelConfig.provider}
                      onChange={(e) => setModelConfig({...modelConfig, provider: e.target.value})}
                      className="w-full mt-1 p-2 border rounded-md"
                    >
                      <option value="openai">OpenAI</option>
                      <option value="anthropic">Anthropic</option>
                      <option value="google">Google (Gemini)</option>
                      <option value="azure">Azure OpenAI</option>
                      <option value="meta">Meta (Llama)</option>
                      <option value="microsoft">Microsoft (Phi)</option>
                      <option value="cohere">Cohere</option>
                      <option value="mistral">Mistral AI</option>
                      <option value="groq">Groq</option>
                      <option value="together">Together AI</option>
                    </select>
                  </div>
                  
                  <div>
                    <Label htmlFor="modelName">Modelo</Label>
                    <select
                      id="modelName"
                      value={modelConfig.model}
                      onChange={(e) => setModelConfig({...modelConfig, model: e.target.value})}
                      className="w-full mt-1 p-2 border rounded-md"
                    >
                      {/* OpenAI Models */}
                      <optgroup label="OpenAI">
                        <option value="gpt-5">GPT-5 (Latest)</option>
                        <option value="gpt-4o">GPT-4o (Omni)</option>
                        <option value="gpt-4o-mini">GPT-4o Mini</option>
                        <option value="gpt-4-turbo">GPT-4 Turbo</option>
                        <option value="gpt-4">GPT-4</option>
                        <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                      </optgroup>
                      
                      {/* Anthropic Models */}
                      <optgroup label="Anthropic">
                        <option value="claude-3.5-sonnet">Claude 3.5 Sonnet</option>
                        <option value="claude-3.5-haiku">Claude 3.5 Haiku</option>
                        <option value="claude-3-opus">Claude 3 Opus</option>
                        <option value="claude-3-sonnet">Claude 3 Sonnet</option>
                        <option value="claude-3-haiku">Claude 3 Haiku</option>
                        <option value="claude-2">Claude 2</option>
                      </optgroup>
                      
                      {/* Google Models */}
                      <optgroup label="Google">
                        <option value="gemini-2.0-flash">Gemini 2.0 Flash</option>
                        <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                        <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
                        <option value="gemini-1.0-pro">Gemini 1.0 Pro</option>
                      </optgroup>
                      
                      {/* Meta Models */}
                      <optgroup label="Meta">
                        <option value="llama-3.1-405b">Llama 3.1 405B</option>
                        <option value="llama-3.1-70b">Llama 3.1 70B</option>
                        <option value="llama-3.1-8b">Llama 3.1 8B</option>
                        <option value="llama-3-70b">Llama 3 70B</option>
                      </optgroup>
                      
                      {/* Microsoft Models */}
                      <optgroup label="Microsoft">
                        <option value="phi-3-medium">Phi-3 Medium</option>
                        <option value="phi-3-mini">Phi-3 Mini</option>
                        <option value="phi-2">Phi-2</option>
                      </optgroup>
                    </select>
                  </div>

                  <div>
                    <Label htmlFor="temperature">Temperatura: {modelConfig.temperature}</Label>
                    <input
                      id="temperature"
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={modelConfig.temperature}
                      onChange={(e) => setModelConfig({...modelConfig, temperature: parseFloat(e.target.value)})}
                      className="w-full mt-1"
                    />
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>Conservador (0.0)</span>
                      <span>Criativo (1.0)</span>
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="maxTokens">Máximo de Tokens</Label>
                    <Input
                      id="maxTokens"
                      type="number"
                      value={modelConfig.maxTokens}
                      onChange={(e) => setModelConfig({...modelConfig, maxTokens: parseInt(e.target.value)})}
                      className="mt-1"
                    />
                  </div>

                  <Button onClick={saveModelConfig} className="w-full">
                    <Settings className="h-4 w-4 mr-2" />
                    Salvar Configurações
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Database className="h-5 w-5 text-green-600" />
                    Informações do Modelo
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Provedor</span>
                      <Badge variant="outline">{modelConfig.provider}</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Modelo</span>
                      <Badge variant="outline">{modelConfig.model}</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Temperatura</span>
                      <span className="text-sm text-muted-foreground">{modelConfig.temperature}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Max Tokens</span>
                      <span className="text-sm text-muted-foreground">{modelConfig.maxTokens}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="knowledge" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Database className="h-5 w-5 text-purple-600" />
                    Fontes de Conhecimento
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Tipos de Fontes Disponíveis */}
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <Label>Adicionar Nova Fonte</Label>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={loadMcpTools}
                        disabled={isLoadingMcp}
                        className="flex items-center gap-2"
                      >
                        {isLoadingMcp ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          <Settings className="h-4 w-4" />
                        )}
                        {isLoadingMcp ? 'Carregando...' : 'Carregar MCP'}
                      </Button>
                    </div>
                    <div className="grid grid-cols-2 gap-2 mt-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => addKnowledgeSource('url')}
                        className="flex items-center gap-2"
                      >
                        <Globe className="h-4 w-4" />
                        URL/Website
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => addKnowledgeSource('sql')}
                        className="flex items-center gap-2"
                      >
                        <DbIcon className="h-4 w-4" />
                        Base SQL
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => addKnowledgeSource('document')}
                        className="flex items-center gap-2"
                      >
                        <FileText className="h-4 w-4" />
                        Documento
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => addKnowledgeSource('api')}
                        className="flex items-center gap-2"
                      >
                        <Link className="h-4 w-4" />
                        API
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => addKnowledgeSource('mcp')}
                        className="flex items-center gap-2"
                      >
                        <Settings className="h-4 w-4" />
                        MCP Tools
                      </Button>
                    </div>
                  </div>

                  {/* Ferramentas MCP Disponíveis */}
                  {mcpTools.length > 0 && (
                    <div>
                      <Label>Ferramentas MCP Disponíveis</Label>
                      <div className="grid grid-cols-1 gap-2 mt-2">
                        {mcpTools.map((tool, index) => (
                          <Card key={index} className="p-3">
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-2">
                                <Settings className="h-4 w-4 text-cyan-600" />
                                <div>
                                  <div className="font-medium">{tool.name}</div>
                                  <div className="text-sm text-gray-600">{tool.description}</div>
                                  <div className="flex flex-wrap gap-1 mt-1">
                                    {tool.capabilities.slice(0, 3).map((cap: string, i: number) => (
                                      <Badge key={i} variant="outline" className="text-xs">
                                        {cap}
                                      </Badge>
                                    ))}
                                    {tool.capabilities.length > 3 && (
                                      <Badge variant="outline" className="text-xs">
                                        +{tool.capabilities.length - 3} mais
                                      </Badge>
                                    )}
                                  </div>
                                </div>
                              </div>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => {
                                  const newSource = {
                                    id: `mcp-${Date.now()}`,
                                    type: 'mcp' as const,
                                    name: tool.name,
                                    connection: '',
                                    config: { tool: tool.name.toLowerCase().replace(' ', '_') }
                                  }
                                  setKnowledgeConfig({
                                    ...knowledgeConfig,
                                    sourceTypes: [...knowledgeConfig.sourceTypes, newSource]
                                  })
                                  toast.success(`Ferramenta ${tool.name} adicionada!`)
                                }}
                              >
                                Adicionar
                              </Button>
                            </div>
                          </Card>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Fontes Configuradas */}
                  <div>
                    <Label>Fontes Configuradas</Label>
                    <div className="space-y-3 mt-2">
                      {knowledgeConfig.sourceTypes.map((source) => (
                        <Card key={source.id} className="p-3">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                              {source.type === 'url' && <Globe className="h-4 w-4 text-blue-600" />}
                              {source.type === 'sql' && <DbIcon className="h-4 w-4 text-green-600" />}
                              {source.type === 'document' && <FileText className="h-4 w-4 text-purple-600" />}
                              {source.type === 'api' && <Link className="h-4 w-4 text-orange-600" />}
                              {source.type === 'mcp' && <Settings className="h-4 w-4 text-cyan-600" />}
                              <Badge variant="outline" className="text-xs">
                                {source.type.toUpperCase()}
                              </Badge>
                            </div>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => removeKnowledgeSource(source.id)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                          
                          <div className="space-y-2">
                            <Input
                              placeholder="Nome da fonte"
                              value={source.name}
                              onChange={(e) => updateKnowledgeSource(source.id, { name: e.target.value })}
                            />
                            
                            {source.type === 'url' && (
                              <Input
                                placeholder="https://exemplo.com"
                                value={source.connection}
                                onChange={(e) => updateKnowledgeSource(source.id, { connection: e.target.value })}
                              />
                            )}
                            
                            {source.type === 'sql' && (
                              <div className="space-y-2">
                                <Input
                                  placeholder="postgresql://user:pass@host:port/db"
                                  value={source.connection}
                                  onChange={(e) => updateKnowledgeSource(source.id, { connection: e.target.value })}
                                />
                                <Input
                                  placeholder="Tabela principal (ex: products)"
                                  value={source.config.table || ''}
                                  onChange={(e) => updateKnowledgeSource(source.id, { 
                                    config: { ...source.config, table: e.target.value }
                                  })}
                                />
                              </div>
                            )}
                            
                            {source.type === 'document' && (
                              <div className="space-y-2">
                                <Input
                                  placeholder="Caminho do arquivo ou URL"
                                  value={source.connection}
                                  onChange={(e) => updateKnowledgeSource(source.id, { connection: e.target.value })}
                                />
                                <select
                                  value={source.config.format || 'pdf'}
                                  onChange={(e) => updateKnowledgeSource(source.id, { 
                                    config: { ...source.config, format: e.target.value }
                                  })}
                                  className="w-full p-2 border rounded-md text-sm"
                                >
                                  <option value="pdf">PDF</option>
                                  <option value="docx">Word</option>
                                  <option value="txt">Texto</option>
                                  <option value="md">Markdown</option>
                                </select>
                              </div>
                            )}
                            
                            {source.type === 'api' && (
                              <div className="space-y-2">
                                <Input
                                  placeholder="https://api.exemplo.com/endpoint"
                                  value={source.connection}
                                  onChange={(e) => updateKnowledgeSource(source.id, { connection: e.target.value })}
                                />
                                <Input
                                  placeholder="API Key (opcional)"
                                  type="password"
                                  value={source.config.apiKey || ''}
                                  onChange={(e) => updateKnowledgeSource(source.id, { 
                                    config: { ...source.config, apiKey: e.target.value }
                                  })}
                                />
                              </div>
                            )}
                            
                            {source.type === 'mcp' && (
                              <div className="space-y-2">
                                <div className="grid grid-cols-2 gap-2">
                                  <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => updateKnowledgeSource(source.id, { 
                                      config: { ...source.config, tool: 'filesystem' }
                                    })}
                                    className={source.config.tool === 'filesystem' ? 'bg-blue-100' : ''}
                                  >
                                    Sistema de Arquivos
                                  </Button>
                                  <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => updateKnowledgeSource(source.id, { 
                                      config: { ...source.config, tool: 'database' }
                                    })}
                                    className={source.config.tool === 'database' ? 'bg-green-100' : ''}
                                  >
                                    Banco de Dados
                                  </Button>
                                  <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => updateKnowledgeSource(source.id, { 
                                      config: { ...source.config, tool: 'github' }
                                    })}
                                    className={source.config.tool === 'github' ? 'bg-purple-100' : ''}
                                  >
                                    GitHub
                                  </Button>
                                  <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => updateKnowledgeSource(source.id, { 
                                      config: { ...source.config, tool: 'web' }
                                    })}
                                    className={source.config.tool === 'web' ? 'bg-orange-100' : ''}
                                  >
                                    Web Tools
                                  </Button>
                                </div>
                                {source.config.tool && (
                                  <div className="p-2 bg-gray-50 rounded text-sm">
                                    <strong>Ferramenta selecionada:</strong> {source.config.tool}
                                  </div>
                                )}
                              </div>
                            )}
                          </div>
                        </Card>
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="ragEnabled"
                      checked={knowledgeConfig.ragEnabled}
                      onChange={(e) => setKnowledgeConfig({...knowledgeConfig, ragEnabled: e.target.checked})}
                    />
                    <Label htmlFor="ragEnabled">Habilitar RAG (Retrieval Augmented Generation)</Label>
                  </div>

                  <div>
                    <Label htmlFor="maxSources">Máximo de Fontes</Label>
                    <Input
                      id="maxSources"
                      type="number"
                      value={knowledgeConfig.maxSources}
                      onChange={(e) => setKnowledgeConfig({...knowledgeConfig, maxSources: parseInt(e.target.value)})}
                      className="mt-1"
                    />
                  </div>

                  <Button onClick={saveKnowledgeConfig} className="w-full">
                    <Database className="h-4 w-4 mr-2" />
                    Salvar Configurações
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="h-5 w-5 text-green-600" />
                    Status do Conhecimento
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">RAG Habilitado</span>
                      <Badge variant={knowledgeConfig.ragEnabled ? 'default' : 'secondary'}>
                        {knowledgeConfig.ragEnabled ? 'Ativo' : 'Inativo'}
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Fontes Configuradas</span>
                      <span className="text-sm text-muted-foreground">
                        {knowledgeConfig.sourceTypes.length}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Máximo de Fontes</span>
                      <span className="text-sm text-muted-foreground">{knowledgeConfig.maxSources}</span>
                    </div>
                    
                    {/* Tipos de Fontes */}
                    <div className="space-y-2">
                      <span className="text-sm font-medium">Tipos de Fontes:</span>
                      <div className="flex flex-wrap gap-1">
                        {knowledgeConfig.sourceTypes.map((source) => (
                          <Badge key={source.id} variant="outline" className="text-xs">
                            {source.type.toUpperCase()}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    
                    {/* Exemplos de Configuração */}
                    <div className="space-y-2">
                      <span className="text-sm font-medium">Exemplos de Configuração:</span>
                      <div className="text-xs text-muted-foreground space-y-1">
                        <div><strong>SQL:</strong> postgresql://user:pass@host:port/db</div>
                        <div><strong>URL:</strong> https://docs.exemplo.com</div>
                        <div><strong>Documento:</strong> /path/to/file.pdf</div>
                        <div><strong>API:</strong> https://api.exemplo.com/data</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="tools" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Settings className="h-5 w-5 text-orange-600" />
                    Ferramentas Disponíveis
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label>Ferramentas Habilitadas</Label>
                    <div className="space-y-2 mt-2">
                      {toolsConfig.availableTools.map((tool) => (
                        <div key={tool} className="flex items-center space-x-2">
                          <input
                            type="checkbox"
                            id={tool}
                            checked={toolsConfig.enabledTools.includes(tool)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setToolsConfig({
                                  ...toolsConfig,
                                  enabledTools: [...toolsConfig.enabledTools, tool]
                                })
                              } else {
                                setToolsConfig({
                                  ...toolsConfig,
                                  enabledTools: toolsConfig.enabledTools.filter(t => t !== tool)
                                })
                              }
                            }}
                          />
                          <Label htmlFor={tool} className="text-sm">
                            {tool.replace('_', ' ').toUpperCase()}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <Label>Ferramentas Personalizadas</Label>
                    <div className="space-y-2 mt-2">
                      {toolsConfig.customTools.map((tool, index) => (
                        <div key={index} className="flex gap-2">
                          <Input
                            value={tool}
                            onChange={(e) => {
                              const newTools = [...toolsConfig.customTools]
                              newTools[index] = e.target.value
                              setToolsConfig({...toolsConfig, customTools: newTools})
                            }}
                            placeholder="Nome da ferramenta"
                          />
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              const newTools = toolsConfig.customTools.filter((_, i) => i !== index)
                              setToolsConfig({...toolsConfig, customTools: newTools})
                            }}
                          >
                            <XCircle className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setToolsConfig({
                            ...toolsConfig,
                            customTools: [...toolsConfig.customTools, '']
                          })
                        }}
                      >
                        <Activity className="h-4 w-4 mr-2" />
                        Adicionar Ferramenta
                      </Button>
                    </div>
                  </div>

                  <Button onClick={saveToolsConfig} className="w-full">
                    <Settings className="h-4 w-4 mr-2" />
                    Salvar Configurações
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="h-5 w-5 text-green-600" />
                    Status das Ferramentas
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Ferramentas Ativas</span>
                      <span className="text-sm text-muted-foreground">
                        {toolsConfig.enabledTools.length}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Ferramentas Personalizadas</span>
                      <span className="text-sm text-muted-foreground">
                        {toolsConfig.customTools.filter(t => t.trim()).length}
                      </span>
                    </div>
                    <div className="space-y-1">
                      <span className="text-sm font-medium">Ferramentas Habilitadas:</span>
                      <div className="flex flex-wrap gap-1">
                        {toolsConfig.enabledTools.map((tool) => (
                          <Badge key={tool} variant="outline" className="text-xs">
                            {tool.replace('_', ' ')}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </MainLayout>
  )
}