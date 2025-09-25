import React from 'react'
import { cn } from '@/lib/utils'

interface TextFieldUnstyledProps {
  children: React.ReactNode
  className?: string
}

interface TextFieldInputProps {
  placeholder?: string
  value?: string
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
  onKeyPress?: (event: React.KeyboardEvent<HTMLInputElement>) => void
  className?: string
}

export function TextFieldUnstyled({ children, className }: TextFieldUnstyledProps) {
  return (
    <div className={cn('flex items-center', className)}>
      {children}
    </div>
  )
}

TextFieldUnstyled.Input = function TextFieldInput({ 
  placeholder, 
  value, 
  onChange, 
  onKeyPress,
  className 
}: TextFieldInputProps) {
  return (
    <input
      type="text"
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      onKeyPress={onKeyPress}
      className={cn(
        'flex-1 border-none outline-none bg-transparent text-default-font placeholder-subtext-color',
        className
      )}
    />
  )
}
