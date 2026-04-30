import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/static/',
  build: {
    outDir: '../static/dist',  // donde Django busca los archivos
    emptyOutDir: true,
    manifest: true,  // necesario para django-vite
  },
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    }
  }
})