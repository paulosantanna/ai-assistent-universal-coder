import { defineConfig } from 'vitest/config'
import type { Plugin } from 'vite'
import react from '@vitejs/plugin-react'

// Remove type="module"/crossorigin do index.html gerado e marca o script como
// defer: o Vite envolve a entrada em script de módulo mesmo com formato iife, e
// script de módulo não roda em páginas file:// (Chrome: CORS). Módulo é sempre
// deferred; clássico não — sem o defer, ele executa no <head> antes de
// <div id="root"> existir e o React falha ("Target container is not a DOM").
// enforce 'post' garante que roda após o vite:build-html emitir o ativo.
const scriptClassicoNoIndex = (): Plugin => ({
  name: 'iife-classic-index-html',
  enforce: 'post',
  generateBundle(_options, bundle) {
    const html = bundle['index.html']
    if (html && html.type === 'asset') {
      html.source = String(html.source)
        .replace(' type="module"', ' defer')
        .replace(' crossorigin', '')
    }
  },
})

// base relativa para funcionar em GitHub Pages sob subcaminho.
// Formato iife + caminhos relativos abrem o dist/index.html por file://:
// Chromium bloqueia <script type="module"> em página file:// (CORS), mas
// script clássico funciona; o código não usa import.meta nem import() dinâmico.
export default defineConfig({
  base: './',
  plugins: [react(), scriptClassicoNoIndex()],
  build: {
    rollupOptions: {
      output: {
        format: 'iife',
        inlineDynamicImports: true,
      },
    },
  },
  test: {
    environment: 'node',
    include: ['tests/**/*.test.ts'],
  },
})
