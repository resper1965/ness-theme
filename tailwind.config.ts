import type { Config } from 'tailwindcss'

export default {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'ness': {
          50: 'rgb(0, 173, 232)',
          100: 'rgb(207, 250, 254)',
          200: 'rgb(165, 243, 252)',
          300: 'rgb(103, 232, 249)',
          400: 'rgb(34, 211, 238)',
          500: 'rgb(6, 182, 212)',
          600: 'rgb(8, 145, 178)',
          700: 'rgb(14, 116, 144)',
          800: 'rgb(21, 94, 117)',
          900: 'rgb(22, 78, 99)',
        },
        'brand': {
          50: 'rgb(0, 173, 232)',
          primary: 'rgb(34, 211, 238)',
        },
        'default': {
          font: 'rgb(17, 24, 39)',
          background: 'rgb(255, 255, 255)',
        },
        'subtext': 'rgb(107, 114, 128)',
        'neutral-border': 'rgb(229, 231, 235)',
      },
      fontFamily: {
        'montserrat': ['Montserrat', 'sans-serif'],
      },
    },
  },
  plugins: [],
} satisfies Config