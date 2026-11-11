import { defineConfig } from 'vitest/config';

/** Testes do loader (C22): sem DOM, environment node. */
export default defineConfig({
  test: {
    environment: 'node',
    include: ['tests/**/*.test.ts'],
  },
});
