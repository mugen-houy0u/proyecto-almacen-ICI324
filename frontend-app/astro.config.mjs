import { defineConfig } from 'astro/config'
import preact from '@astrojs/preact'
import { fileURLToPath } from 'node:url'

import tailwindcss from '@tailwindcss/vite';

import node from "@astrojs/node";

export default defineConfig({
  integrations: [preact()],
  
  output: "server",
  adapter: node({
    mode: 'standalone',
  }),

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

    plugins: [tailwindcss()],
  },
})