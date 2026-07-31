import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["tests/node/smoke.test.cjs"],
    environment: "node",
    globals: true,
  },
});
