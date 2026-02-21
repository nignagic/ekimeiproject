import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const backendHost = process.env.BACKEND_HOST || "http://web:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      "/api": {
        target: backendHost,
        changeOrigin: true,
      },
      "/auth": {
        target: backendHost,
        changeOrigin: true,
      },
      "/static": {
        target: backendHost,
        changeOrigin: true,
      },
      "/media": {
        target: backendHost,
        changeOrigin: true,
      },
    },
  },
});
