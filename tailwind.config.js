/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#0B1120",
          surface: "#131B2E",
          border: "#232E45",
        },
        paper: {
          DEFAULT: "#F5F6F8",
          surface: "#FFFFFF",
          border: "#E2E5EB",
        },
        accent: {
          DEFAULT: "#C97A3D",
          strong: "#A8632E",
          soft: "#E2984F",
        },
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"],
      },
      keyframes: {
        "pulse-travel": {
          "0%": { strokeDashoffset: "240" },
          "100%": { strokeDashoffset: "0" },
        },
      },
      animation: {
        "pulse-travel": "pulse-travel 3.5s linear infinite",
      },
    },
  },
  plugins: [],
};
