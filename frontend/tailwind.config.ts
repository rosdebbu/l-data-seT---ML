import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: {
          950: "#060907",
          900: "#090d0b",
          850: "#0d1410",
          800: "#121b16",
          700: "#1a2720",
          border: "rgba(16, 185, 129, 0.15)",
        },
        accent: {
          emerald: "#10b981",
          emeraldLight: "#34d399",
          mint: "#a7f3d0",
          lime: "#84cc16",
          teal: "#14b8a6",
        }
      },
      fontFamily: {
        sans: ["var(--font-outfit)", "Inter", "system-ui", "sans-serif"],
        mono: ["var(--font-jetbrains)", "JetBrains Mono", "monospace"],
      },
      boxShadow: {
        "emerald-glow": "0 0 30px -5px rgba(16, 185, 129, 0.3)",
        "card-subtle": "0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.05)",
      }
    },
  },
  plugins: [],
};
export default config;
