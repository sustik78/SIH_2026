/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        gov: {
          navy: '#0B192C',
          deep: '#1E3E62',
          blue: '#1E40AF',
          accent: '#2563EB',
          saffron: '#D97706',
          gold: '#B45309',
          surface: '#F8FAFC',
          border: '#E2E8F0',
          darkSurface: '#0F172A',
          darkCard: '#1E293B'
        }
      },
      fontFamily: {
        sans: ['Inter', 'Outfit', 'Segoe UI', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
