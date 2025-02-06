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
        primaryAccent: "#18181B",
        secondary: "#f5f5f5",
        border: "#FAFAFA26",
        muted: "#A1A1AA",
      },
      fontFamily: {
        geist: ["Geist"],
        geist_mono: ["Geist Mono", "monospace"],
        inter: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
