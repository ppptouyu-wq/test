import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig(() => {
  // If you run backend on 5000, proxy /api to avoid CORS in dev.
  return {
    plugins: [vue()],
    server: {
      proxy: {
        "/api": {
          target: process.env.VITE_API_BASE || "http://localhost:5000",
          changeOrigin: true
        }
      }
    }
  };
});

