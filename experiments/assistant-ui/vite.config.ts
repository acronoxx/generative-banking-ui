import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // Les requêtes de la page vers /api sont relayées au serveur de l'agent
  server: { proxy: { '/api': 'http://localhost:4100' } },
})
