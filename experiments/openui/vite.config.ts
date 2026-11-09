import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Les requêtes de la page vers /api sont relayées au serveur de l'agent
export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/api": "http://localhost:4200" } },
});
