import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://127.0.0.1:6060', changeOrigin: true, secure: false }, ##いま 絶対URL（http://127.0.0.1:6060） を使っているなら、proxyは一切使われません
      '/ask': { target: 'http://127.0.0.1:6060', changeOrigin: true, secure: false },
    },
  },
})
