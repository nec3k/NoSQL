/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./Module1/templates/**/*.html'],
  theme: {
    extend: {},
  },
  plugins: [require('@tailwindcss/forms'),],
}

