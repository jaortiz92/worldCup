import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    // 1. host: '0.0.0.0' es OBLIGATORIO en Docker para que 
    // el contenedor exponga el puerto hacia Nginx.
    host: '0.0.0.0', 
    
    // 2. Mantenemos el puerto estándar de Vite.
    port: 5173,      
    
    // 3. LA SOLUCIÓN: Le decimos a Vite que confíe en el tráfico 
    // que viene de dominios externos como Ngrok.
    allowedHosts: true 
  }
})