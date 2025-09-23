import type { Metadata } from 'next'
import { Montserrat } from 'next/font/google'
import { NuqsAdapter } from 'nuqs/adapters/next/app'
import { Toaster } from '@/components/ui/sonner'
import './globals.css'
const montserrat = Montserrat({
  variable: '--font-montserrat',
  weight: ['300', '400', '500', '600', '700'],
  subsets: ['latin'],
  display: 'swap'
})

export const metadata: Metadata = {
  title: 'Gabi - Chat Multi-Agentes',
  description:
    'Gabi - Chat Multi-Agentes com tecnologia avançada. Interface moderna para interação com agentes de IA.',
  icons: {
    icon: '/favicon.ico',
  },
}

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${montserrat.variable} font-montserrat antialiased`}>
        <NuqsAdapter>{children}</NuqsAdapter>
        <Toaster />
      </body>
    </html>
  )
}
