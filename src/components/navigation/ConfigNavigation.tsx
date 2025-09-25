'use client'

import { Button } from '@/components/ui/button'
import { ArrowLeft, Home, Settings, Database, BarChart3 } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

interface ConfigNavigationProps {
  currentTab?: string
}

export function ConfigNavigation({ currentTab }: ConfigNavigationProps) {
  const pathname = usePathname()
  
  return (
    <div className="sticky top-0 z-50 bg-background/80 backdrop-blur-sm border-b border-border">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Navegação principal */}
          <div className="flex items-center space-x-4">
            <Link href="/">
              <Button variant="outline" size="sm" className="flex items-center space-x-2 hover:bg-accent">
                <ArrowLeft className="h-4 w-4" />
                <span>Voltar ao Chat</span>
              </Button>
            </Link>
            <Link href="/">
              <Button variant="ghost" size="sm" className="flex items-center space-x-2 hover:bg-accent">
                <Home className="h-4 w-4" />
                <span>Início</span>
              </Button>
            </Link>
          </div>
          
          {/* Breadcrumb dinâmico */}
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground transition-colors">
              Início
            </Link>
            <span>/</span>
            <Link href="/configuracoes" className="hover:text-foreground transition-colors">
              Configurações
            </Link>
            {currentTab && (
              <>
                <span>/</span>
                <span className="text-foreground font-medium capitalize">
                  {currentTab}
                </span>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export function ConfigTabsNavigation() {
  const tabs = [
    { id: 'agents', label: 'Agentes', icon: Settings },
    { id: 'ingestion', label: 'Ingestão', icon: Database },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'system', label: 'Sistema', icon: Settings },
    { id: 'security', label: 'Segurança', icon: Settings }
  ]
  
  return (
    <div className="bg-background border-b border-border">
      <div className="container mx-auto px-6">
        <nav className="flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <Link
                key={tab.id}
                href={`/configuracoes?tab=${tab.id}`}
                className="flex items-center space-x-2 py-4 px-2 border-b-2 border-transparent hover:border-border transition-colors"
              >
                <Icon className="h-4 w-4" />
                <span className="text-sm font-medium">{tab.label}</span>
              </Link>
            )
          })}
        </nav>
      </div>
    </div>
  )
}
