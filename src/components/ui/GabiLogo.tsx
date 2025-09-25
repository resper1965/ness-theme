'use client'

import React from 'react'
import Image from 'next/image'
import { useTheme } from 'next-themes'
import GabiLogoFc from '@/assets/Gabi-logo-fc.png'
import GabiLogoFe from '@/assets/Gabi-logo-fe.png'

interface GabiLogoProps {
  className?: string
  width?: number
  height?: number
  priority?: boolean
  alt?: string
}

export function GabiLogo({ 
  className = '', 
  width = 32, 
  height = 32, 
  priority = false,
  alt = 'Gabi'
}: GabiLogoProps) {
  const { theme, resolvedTheme } = useTheme()
  
  // Determinar qual logo usar baseado no tema
  const isDark = resolvedTheme === 'dark' || theme === 'dark'
  const logoSrc = isDark ? GabiLogoFe : GabiLogoFc
  
  return (
    <Image
      src={logoSrc}
      alt={alt}
      width={width}
      height={height}
      priority={priority}
      className={`object-contain ${className}`}
    />
  )
}

// Componente específico para o sidebar
export function GabiSidebarLogo({ className = '' }: { className?: string }) {
  return (
    <GabiLogo 
      className={`w-25 h-25 ${className}`}
      width={100}
      height={100}
      priority={true}
    />
  )
}

// Componente para headers
export function GabiHeaderLogo({ className = '' }: { className?: string }) {
  return (
    <GabiLogo 
      className={`w-10 h-10 ${className}`}
      width={40}
      height={40}
      priority={true}
    />
  )
}

