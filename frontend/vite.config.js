import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // lightningcss (the Vite 8 default) fails to minify a legacy
    // selector in semantic-ui-css 2.5.0's bundled stylesheet.
    cssMinify: false,
  },
})
