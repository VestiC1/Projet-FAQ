// Configuration Tailwind + Hero UI
const { heroui } = require("@heroui/react");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Chemins vers vos fichiers Next.js
    "./src/pages/**/*.{js,jsx}",
    "./src/components/**/*.{js,jsx}",
    "./src/app/**/*.{js,jsx}",
    // Chemin vers les composants Hero UI (important!)
    "./node_modules/@heroui/theme/dist/**/*.{js,jsx}",
  ],
  theme: {
    extend: {},
  },
  darkMode: "class", // Active le mode sombre avec une classe CSS
  plugins: [heroui(),
  require("@tailwindcss/typography"),  // ← add this
  ], // Active le plugin Hero UI
};