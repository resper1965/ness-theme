import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
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
