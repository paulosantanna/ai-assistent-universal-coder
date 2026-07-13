const assert = require("node:assert/strict");

describe("AEOS node test toolchain", () => {
  it("runs the shared node smoke test", () => {
    assert.equal("AEOS".toLowerCase(), "aeos");
  });
});
