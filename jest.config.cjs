module.exports = {
  testEnvironment: "node",
  testMatch: ["<rootDir>/tests/node/**/*.test.cjs"],
  collectCoverageFrom: ["aeos/**/*.js", "runtime/src/**/*.ts"],
};
