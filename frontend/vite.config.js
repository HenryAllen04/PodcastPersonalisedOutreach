import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    watch: null, // Disable file watching entirely for Docker
    hmr: false,  // Disable hot module reload
  },
  // Optimization for Docker
  optimizeDeps: {
    esbuildOptions: {
      // Avoid file system issues in Docker
      keepNames: true,
    },
  },
  // Additional settings for Docker compatibility
  resolve: {
    preserveSymlinks: true,
  },
})
