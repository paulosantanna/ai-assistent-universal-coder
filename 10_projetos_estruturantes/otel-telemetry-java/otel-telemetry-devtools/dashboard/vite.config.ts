import { defineConfig } from 'vite';

/** Build lib-mode IIFE: um único script clássico (sem módulos ES) para abrir o
 *  dist/index.html por duplo clique em file:// — caminhos relativos obrigatórios.
 *  Saída vai para os resources do jar do devtools (servida pelo sink em /). */
export default defineConfig({
  build: {
    lib: {
      entry: 'src/main.ts',
      formats: ['iife'],
      name: 'OtelTelemetryDashboard',
      // nome exato (o default iife acrescentaria .iife.js; index.html referencia ./dashboard.js)
      fileName: () => 'dashboard.js',
      // Vite 6: default virou o nome do pacote; index.html e o sink mapeiam /style.css
      cssFileName: 'style',
    },
    outDir: '../src/main/resources/dashboard',
    emptyOutDir: true,
    target: 'es2020',
    reportCompressedSize: false,
  },
});
