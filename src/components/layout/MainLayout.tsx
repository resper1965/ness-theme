'use client'

import React from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { GabiSidebarLogo } from '@/components/ui/GabiLogo'
import { 
  MessageSquare, 
  Settings, 
  Server, 
  History,
  LogOut,
  Menu,
  X
} from 'lucide-react'
import { useState } from 'react'

interface MainLayoutProps {
  children: React.ReactNode
  pageTitle?: string
  onNewChat?: () => void
  onSettings?: () => void
  onLogout?: () => void
}

export function MainLayout({ 
  children, 
  pageTitle = "Chat Multi-Agentes",
  onNewChat, 
  onSettings, 
  onLogout 
}: MainLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const getCurrentPath = () => {
    if (typeof window !== 'undefined') {
      return window.location.pathname
    }
    return '/'
  }

  const navigationItems = [
    {
      name: 'Chat',
      href: '/',
      icon: MessageSquare,
      current: getCurrentPath() === '/'
    },
    {
      name: 'Chats',
      href: '/chats',
      icon: History,
      current: getCurrentPath() === '/chats'
    },
    {
      name: 'Gabi.OS',
      href: '/gabi-os',
      icon: Server,
      current: getCurrentPath() === '/gabi-os'
    },
    {
      name: 'Configurações',
      href: '/configuracoes',
      icon: Settings,
      current: getCurrentPath() === '/configuracoes'
    }
  ]

  return (
    <div className="h-screen bg-background flex">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-sidebar border-r border-sidebar-border
        transform transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0 lg:static lg:inset-0
      `}>
        <div className="flex h-screen flex-col overflow-hidden">
          {/* Header - Mesma altura do header da página */}
          <div className="flex items-center justify-between px-4 border-b border-sidebar-border bg-sidebar flex-shrink-0" style={{ height: '50px' }}>
            <GabiSidebarLogo />
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
            {navigationItems.map((item) => {
              const Icon = item.icon
              return (
                <a
                  key={item.name}
                  href={item.href}
                  className={`
                    flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium
                    transition-colors duration-200
                    ${item.current 
                      ? 'bg-primary text-primary-foreground' 
                      : 'text-muted-foreground hover:bg-accent hover:text-foreground'
                    }
                  `}
                  onClick={() => setSidebarOpen(false)}
                >
                  <Icon className="h-4 w-4" />
                  {item.name}
                </a>
              )
            })}
          </nav>

          {/* Footer - No final do sidebar */}
          <div className="mt-auto p-4 border-t border-sidebar-border flex-shrink-0">
            <Button
              variant="outline"
              size="sm"
              onClick={onLogout}
              className="w-full justify-start gap-2 text-red-600 hover:bg-red-50 hover:text-red-700"
            >
              <LogOut className="h-4 w-4" />
              Sair
            </Button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Top bar - Fixo no topo da área de conteúdo */}
        <div className="fixed top-0 right-0 left-64 z-30 bg-background border-b border-border shadow-sm lg:left-64">
          <div className="flex items-center justify-between px-4" style={{ height: '50px' }}>
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden"
              >
                <Menu className="h-4 w-4" />
              </Button>
              <h2 className="text-xl font-semibold text-foreground">
                {pageTitle}
              </h2>
            </div>
            <div className="flex items-center gap-2">
              <Button
                onClick={onNewChat}
                size="sm"
                className="bg-primary hover:bg-primary/90"
              >
                <MessageSquare className="h-4 w-4 mr-2" />
                Novo Chat
              </Button>
            </div>
          </div>
        </div>

            {/* Page content */}
            <main className="flex-1 overflow-hidden pt-12">
              {children}
            </main>
      </div>
    </div>
  )
}