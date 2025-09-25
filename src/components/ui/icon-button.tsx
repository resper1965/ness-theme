import React from 'react'
import { cn } from '@/lib/utils'

interface IconButtonProps {
  icon: React.ReactNode
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void
  variant?: 'neutral' | 'brand' | 'ghost'
  size?: 'small' | 'medium' | 'large'
  disabled?: boolean
  className?: string
}

export function IconButton({ 
  icon, 
  onClick, 
  variant = 'neutral',
  size = 'medium',
  disabled = false,
  className 
}: IconButtonProps) {
  const sizeClasses = {
    small: 'w-8 h-8',
    medium: 'w-10 h-10',
    large: 'w-12 h-12'
  }

  const variantClasses = {
    neutral: 'bg-neutral-100 hover:bg-neutral-200 text-neutral-700',
    brand: 'bg-brand-blue hover:bg-brand-primary text-white',
    ghost: 'bg-transparent hover:bg-neutral-100 text-neutral-700'
  }

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        'flex items-center justify-center rounded-lg transition-colors',
        sizeClasses[size],
        variantClasses[variant],
        disabled && 'opacity-50 cursor-not-allowed',
        className
      )}
    >
      {icon}
    </button>
  )
}
