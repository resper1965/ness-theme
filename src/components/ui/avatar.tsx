import React from 'react'
import { cn } from '@/lib/utils'

interface AvatarProps {
  size?: 'small' | 'medium' | 'large'
  variant?: 'neutral' | 'brand'
  image?: string
  children?: React.ReactNode
  className?: string
}

export function Avatar({ 
  size = 'medium', 
  variant = 'neutral', 
  image, 
  children, 
  className 
}: AvatarProps) {
  const sizeClasses = {
    small: 'w-8 h-8 text-xs',
    medium: 'w-10 h-10 text-sm',
    large: 'w-12 h-12 text-base'
  }

  const variantClasses = {
    neutral: 'bg-neutral-200 text-neutral-700',
    brand: 'bg-brand-blue text-white'
  }

  return (
    <div
      className={cn(
        'flex items-center justify-center rounded-full font-medium',
        sizeClasses[size],
        variantClasses[variant],
        className
      )}
    >
      {image ? (
        <img 
          src={image} 
          alt="Avatar" 
          className="w-full h-full rounded-full object-cover"
        />
      ) : (
        children
      )}
    </div>
  )
}
