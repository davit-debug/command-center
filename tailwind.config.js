/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./*.html', './tools/*.html', './blog/*.html', './case-studies/*.html'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#58E6FF', light: '#7AEDFF', dark: '#3ED8F5' },
        accent: { DEFAULT: '#FC81FE', dark: '#E070E2' },
        surface: { DEFAULT: '#ffffff', alt: '#f8fafc', dark: '#020710', 'dark-alt': '#0F0F0F' },
        heading: { DEFAULT: '#0f172a', dark: '#f8fafc' },
        body: { DEFAULT: '#475569', dark: '#94a3b8' },
        success: '#21C743',
        ai: { purple: '#8B5CF6', blue: '#3B82F6', teal: '#14B8A6', orange: '#F97316', pink: '#EC4899' },
      },
      fontFamily: {
        'heading': ['"Dachi the Lynx"', 'sans-serif'],
        'body': ['FiraGO', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
