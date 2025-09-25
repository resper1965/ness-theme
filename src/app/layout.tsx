import type { Metadata } from 'next'
import { Montserrat } from 'next/font/google'
import { NuqsAdapter } from 'nuqs/adapters/next/app'
import { Toaster } from '@/components/ui/sonner'
import { ThemeProvider } from '@/components/theme-provider'
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
  keywords: ['chat', 'IA', 'agentes', 'multi-agentes', 'Gabi', 'Agno'],
  authors: [{ name: 'ness.' }],
  creator: 'ness.',
  publisher: 'ness.',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://gabi.ness.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'Gabi - Chat Multi-Agentes',
    description: 'Gabi - Chat Multi-Agentes com tecnologia avançada. Interface moderna para interação com agentes de IA.',
    url: 'https://gabi.ness.com',
    siteName: 'Gabi',
    images: [
      {
        url: '/icon-512.png',
        width: 512,
        height: 512,
        alt: 'Gabi - Chat Multi-Agentes',
      },
    ],
    locale: 'pt_BR',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Gabi - Chat Multi-Agentes',
    description: 'Gabi - Chat Multi-Agentes com tecnologia avançada. Interface moderna para interação com agentes de IA.',
    images: ['/icon-512.png'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: [
      { url: '/favicon.ico', sizes: 'any' },
      { url: '/icon-192.png', sizes: '192x192', type: 'image/png' },
      { url: '/icon-512.png', sizes: '512x512', type: 'image/png' },
    ],
    apple: [
      { url: '/icon-192.png', sizes: '192x192', type: 'image/png' },
    ],
    other: [
      {
        rel: 'mask-icon',
        url: '/icon-192.png',
        color: '#00ade8',
      },
    ],
  },
  manifest: '/manifest.json',
}

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com"/>
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous"/>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet"/>
        <link href="https://fonts.googleapis.com/css2?family=monospace:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet"/>
        
        {/* Favicon e ícones */}
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="icon" href="/icon-192.png" sizes="192x192" type="image/png" />
        <link rel="icon" href="/icon-512.png" sizes="512x512" type="image/png" />
        <link rel="apple-touch-icon" href="/icon-192.png" />
        <link rel="mask-icon" href="/icon-192.png" color="#00ade8" />
        
        {/* PWA Manifest */}
        <link rel="manifest" href="/manifest.json" />
        
        {/* Meta tags adicionais para UX */}
        <meta name="application-name" content="Gabi" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Gabi" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="msapplication-TileColor" content="#00ade8" />
        <meta name="msapplication-tap-highlight" content="no" />
        <meta name="theme-color" content="#00ade8" />
        
        {/* Viewport otimizado */}
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover" />
      </head>
      <body className={`${montserrat.variable} font-montserrat antialiased`}>
        <ThemeProvider
          defaultTheme="light"
          storageKey="gabi-theme"
        >
          <NuqsAdapter>
            {children}
          </NuqsAdapter>
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  )
}
