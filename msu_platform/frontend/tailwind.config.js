/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        msu: {
          blue: '#003366',
          gold: '#FFCC00',
          dark: '#0A192F',
          light: '#F0F4F8',
        }
      },
    },
  },
  plugins: [],
}
