import { defineConfig } from 'astro/config'
import preact from '@astrojs/preact'
import tailwind from '@astrojs/tailwind'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  integrations: [preact(), tailwind()],
  vite: {
    resolve: {
      alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
    },
    server: {
      port: 4321,
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000', // tu backend FastAPI
          changeOrigin: true,
        },
      },
    },
  },
})
