import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  devIndicators: false,
  output: 'standalone',
  experimental: {
    serverComponentsExternalPackages: [],
  },
  images: {
    domains: ['localhost'],
  },
  assetPrefix: process.env.NODE_ENV === 'production' ? '' : '',
  publicRuntimeConfig: {
    assetsPath: '/assets',
  },
}

export default nextConfig
