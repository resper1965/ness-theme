'use client'

import { MainLayout } from '@/components/layout/MainLayout'
import { PageHeader } from '@/components/layout/PageHeader'
import { PageContent } from '@/components/layout/PageContent'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { AgentAdmin } from '@/components/admin/AgentAdmin'
import { AgentImporter } from '@/components/admin/AgentImporter'
import { EntityManager } from '@/components/admin/EntityManager'
import { DynamicAgentCreator } from '@/components/admin/DynamicAgentCreator'
import { WorkflowManager } from '@/components/admin/WorkflowManager'
import { Settings, Users, Database, Shield, Bell, BarChart3, Workflow } from 'lucide-react'
import { Suspense } from 'react'

function ConfiguracoesContent() {
  const handleNewChat = () => {
    window.location.href = '/'
  }

  const handleSettings = () => {
    // Já estamos na página de configurações
  }

  const handleLogout = () => {
    console.log('Logout realizado')
  }

  return (
    <MainLayout 
      pageTitle="Configurações"
      onNewChat={handleNewChat}
      onSettings={handleSettings}
      onLogout={handleLogout}
    >
      <div className="p-6">
        <div className="mb-8">
          <p className="text-muted-foreground">Gerencie as configurações do sistema Gabi</p>
        </div>

            <Tabs defaultValue="dynamic-agents" className="space-y-6">
              <TabsList className="grid w-full grid-cols-2 md:grid-cols-3 lg:grid-cols-7">
                <TabsTrigger value="workflows" className="flex items-center space-x-2">
                  <Workflow className="h-4 w-4" />
                  <span>Workflows</span>
                </TabsTrigger>
                <TabsTrigger value="dynamic-agents" className="flex items-center space-x-2">
                  <Users className="h-4 w-4" />
                  <span>Gabi.OS Dinâmicos</span>
                </TabsTrigger>
                <TabsTrigger value="entities" className="flex items-center space-x-2">
                  <Users className="h-4 w-4" />
                  <span>Entidades</span>
                </TabsTrigger>
                <TabsTrigger value="agents" className="flex items-center space-x-2">
                  <Users className="h-4 w-4" />
                  <span>Gabi.OS</span>
                </TabsTrigger>
            <TabsTrigger value="ingestion" className="flex items-center space-x-2">
              <Database className="h-4 w-4" />
              <span>Ingestão</span>
            </TabsTrigger>
            <TabsTrigger value="analytics" className="flex items-center space-x-2">
              <BarChart3 className="h-4 w-4" />
              <span>Analytics</span>
            </TabsTrigger>
            <TabsTrigger value="system" className="flex items-center space-x-2">
              <Settings className="h-4 w-4" />
              <span>Sistema</span>
            </TabsTrigger>
            <TabsTrigger value="security" className="flex items-center space-x-2">
              <Shield className="h-4 w-4" />
              <span>Segurança</span>
            </TabsTrigger>
            <TabsTrigger value="notifications" className="flex items-center space-x-2">
              <Bell className="h-4 w-4" />
              <span>Notificações</span>
            </TabsTrigger>
          </TabsList>

              <TabsContent value="workflows">
                <div className="space-y-6">
                  <WorkflowManager />
                </div>
              </TabsContent>

              <TabsContent value="dynamic-agents">
                <div className="space-y-6">
                  <DynamicAgentCreator />
                </div>
              </TabsContent>

              <TabsContent value="entities">
                <div className="space-y-6">
                  <EntityManager />
                </div>
              </TabsContent>

              <TabsContent value="agents">
                <div className="space-y-6">
                  <AgentAdmin />
                  <AgentImporter />
                </div>
              </TabsContent>

              <TabsContent value="ingestion">
                <Card>
                  <CardHeader>
                    <CardTitle>Gerenciamento de Ingestão de Dados</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="text-center py-8 text-muted-foreground">
                        Sistema de persistência de dados de ingestão em desenvolvimento...
                        <br />
                        <span className="text-sm">Funcionalidades: Rastreamento, Analytics, Busca de dados históricos</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="analytics">
                <Card>
                  <CardHeader>
                    <CardTitle>Analytics e Relatórios</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="text-center py-8 text-muted-foreground">
                        Dashboard de analytics em desenvolvimento...
                        <br />
                        <span className="text-sm">Métricas de uso, Performance, Relatórios automáticos</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="system">
                <Card>
                  <CardHeader>
                    <CardTitle>Configurações do Sistema</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="text-center py-8 text-muted-foreground">
                        Configurações do sistema em desenvolvimento...
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="security">
                <Card>
                  <CardHeader>
                    <CardTitle>Segurança</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="text-center py-8 text-muted-foreground">
                        Configurações de segurança em desenvolvimento...
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="notifications">
                <Card>
                  <CardHeader>
                    <CardTitle>Notificações</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="text-center py-8 text-muted-foreground">
                        Configurações de notificações em desenvolvimento...
                      </div>
                    </div>
                  </CardContent>
                </Card>
          </TabsContent>
            </Tabs>
          </div>
        </MainLayout>
  )
}

export default function ConfiguracoesPage() {
  return (
    <Suspense fallback={
      <div className="flex h-screen bg-background items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-blue"></div>
      </div>
    }>
      <ConfiguracoesContent />
    </Suspense>
  )
}
