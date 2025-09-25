'use client'

import { ReactNode } from 'react'

interface PageContentProps {
  children: ReactNode
  className?: string
}

export function PageContent({ children, className = '' }: PageContentProps) {
  return (
    <div className={`flex-1 overflow-y-auto ${className}`}>
      <div className="p-6">
        {children}
      </div>
    </div>
  )
}
