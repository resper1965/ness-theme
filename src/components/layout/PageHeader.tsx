'use client'

import { Button } from '@/components/ui/button'
import { ArrowLeft, Home } from 'lucide-react'
import Link from 'next/link'
import { ReactNode } from 'react'

interface PageHeaderProps {
  title: string
  description?: string
  breadcrumb?: string[]
  actions?: ReactNode
}

export function PageHeader({ 
  title, 
  description, 
  breadcrumb = ['Início'], 
  actions 
}: PageHeaderProps) {
  return (
    <div className="border-b border-border bg-background/80 backdrop-blur-sm">
      <div className="flex items-center justify-between px-6 py-4">
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
        
        <div className="flex items-center space-x-4">
          {actions}
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            {breadcrumb.map((item, index) => (
              <div key={index} className="flex items-center space-x-2">
                {index > 0 && <span>/</span>}
                <span className={index === breadcrumb.length - 1 ? 'text-foreground font-medium' : 'hover:text-foreground transition-colors'}>
                  {item}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
