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
        brand: "#FF4017",
        primary: "#18181B",
        background: "#111113",
        secondary: "#f5f5f5",
        border: "#FAFAFA26",
        "input-border": "#27272A",
        muted: "#A1A1AA",
      },
      fontFamily: {
        geist: "var(--font-geist-sans)",
        geist_mono: "var(--font-geist-mono)",
        dm_mono: "var(--font-dm-mono)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
