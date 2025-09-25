import React from 'react'
import { cn } from '@/lib/utils'

interface DefaultPageLayoutProps {
  children: React.ReactNode
  className?: string
}

export function DefaultPageLayout({ children, className }: DefaultPageLayoutProps) {
  return (
    <div className={cn('min-h-screen bg-default-background', className)}>
      {children}
    </div>
  )
}
