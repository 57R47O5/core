import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import path from "path"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // eslint-disable-next-line no-undef
      "@src": path.resolve(__dirname, "../../src"), 
    },
    dedupe: ["react", "react-dom"]
  },
  server: {
    host: "localhost",
    port: 3000,
    strictPort: true,
    fs: {
      allow: [
        ".",                   // raíz del proyecto
        "../src",           // carpeta común que a vigilar
      ]
    }
  },
  
})
