import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const truncateText = (text: string, limit: number) => {
  if (text) {
    return text.length > limit ? `${text.slice(0, limit)}..` : text
  }
  return ''
}

export const isValidUrl = (url: string): boolean => {
  try {
    const parsed = new URL(url)

    const isHttp = parsed.protocol === 'http:' || parsed.protocol === 'https:'

    const hasHost = !!parsed.hostname

    return isHttp && hasHost
  } catch {
    return false
  }
}
