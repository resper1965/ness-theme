import type { Config } from "tailwindcss";
export default {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#FAFAFA",
        primaryAccent: "#18181B",
        brand: "#FF4017",
        background: {
          DEFAULT: "#111113",
          secondary: "#27272A",
        },
        secondary: "#f5f5f5",
        border: "#FAFAFA26",
        accent: "#27272A",
        muted: "#A1A1AA",
        destructive: "#E53935",
        positive: "#22C55E",
      },
      fontFamily: {
        geist: "var(--font-geist-sans)",
        dmmono: "var(--font-dm-mono)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
