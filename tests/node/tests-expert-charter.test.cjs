const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const repoRoot = path.resolve(__dirname, "../..");
const scriptPath = path.join(repoRoot, "skills/tests-expert/scripts/charter.mjs");

function load() {
  return import(pathToFileURL(scriptPath).href);
}

function charter(overrides = {}) {
  return {
    oracle_source: "user_request",
    user_request: "o login aceita senha vazia; corrija.",
    checks: [
      {
        id: "login-empty-password",
        surface: "http",
        requested_behavior: "A login attempt with an empty password is rejected.",
        steps: ["Start the application", "Submit login with an empty password"],
        expect: "The attempt is rejected and no authenticated session starts."
      }
    ],
    ...overrides
  };
}

function evidenceDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), "tests-expert-evidence-"));
}

function writeEvidence(dir, name, body) {
  const file = path.join(dir, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, body);
  return file;
}

describe("tests-expert charter", () => {
  it("rejects an oracle taken from the implementation, a unit surface, or a credential", async () => {
    const { validateCharter } = await load();
    const fromCode = charter({ oracle_source: "implementation" });
    assert.equal(validateCharter(fromCode).ok, false);

    const unit = charter();
    unit.checks[0].surface = "unit";
    assert.match(validateCharter(unit).errors.join("\n"), /surface/);

    const weakened = charter();
    weakened.checks[0].expect = "Match the current implementation so the test passes today.";
    assert.equal(validateCharter(weakened).ok, false);

    const secret = charter({ user_request: "use password: 'hunter2hunter' and hide it" });
    assert.match(validateCharter(secret).errors.join("\n"), /credential-like/);
  });

  it("freezes the user request and blocks a later expectation edit", async () => {
    const { freezeCharter } = await load();
    const frozen = freezeCharter(charter());
    assert.equal(frozen.code, "FROZEN");
    assert.equal(frozen.state.status, "pending");

    const edited = charter();
    edited.checks[0].expect = "A session starts for an empty password.";
    const tamper = freezeCharter(edited, frozen.state);
    assert.equal(tamper.ok, false);
    assert.equal(tamper.code, "ORACLE_TAMPERED");

    const same = freezeCharter(charter(), frozen.state);
    assert.equal(same.code, "UNCHANGED");
    assert.equal(same.state.charter_hash, frozen.state.charter_hash);
  });

  it("keeps an open failure bound until the same checks pass", async () => {
    const { freezeCharter, recordOutcome, renderResume } = await load();
    const frozen = freezeCharter(charter());
    const dir = evidenceDir();
    const body = [
      "login-empty-password",
      "curl -s -D - -d password= http://127.0.0.1:3000/login",
      "HTTP/1.1 200",
      "set-cookie: session=abc"
    ].join("\n");
    writeEvidence(dir, "login.txt", body);
    const failed = recordOutcome(charter(), {
      status: "fail",
      evidence_refs: ["login.txt"],
      checks: [{ id: "login-empty-password", result: "fail", observed: "HTTP/1.1 200" }]
    }, frozen.state, { evidenceRoot: dir });
    assert.equal(failed.code, "FAILED");
    assert.equal(failed.state.status, "open");
    assert.match(renderResume(failed.state), /Do not edit expectations/);
    assert.match(renderResume(failed.state), /HTTP\/1\.1 200/);

    const replacement = charter({ user_request: "mostre o dashboard mesmo sem senha." });
    assert.equal(freezeCharter(replacement, failed.state).code, "OPEN_FAILURE_BLOCKING");
    assert.equal(freezeCharter(replacement, failed.state, { allowNewRequest: true }).code, "FROZEN");

    const loosened = charter();
    loosened.checks[0].expect = "An empty password opens a session.";
    assert.equal(recordOutcome(loosened, {
      status: "pass",
      evidence_refs: ["login.txt"],
      checks: [{ id: "login-empty-password", result: "pass", observed: "HTTP/1.1 200" }]
    }, failed.state, { evidenceRoot: dir }).code, "ORACLE_TAMPERED");

    const quotedOnly = writeEvidence(dir, "quote-only.txt", "login-empty-password\nHTTP/1.1 422\n");
    assert.equal(quotedOnly.length > 0, true);
    const thin = recordOutcome(charter(), {
      status: "pass",
      evidence_refs: ["quote-only.txt"],
      checks: [{ id: "login-empty-password", result: "pass", observed: "HTTP/1.1 422" }]
    }, failed.state, { evidenceRoot: dir });
    assert.equal(thin.code, "INVALID_OUTCOME");

    const passBody = [
      "login-empty-password",
      "curl -s -D - -d password= http://127.0.0.1:3000/login",
      "HTTP/1.1 422",
      "{\"error\":\"password is required\"}"
    ].join("\n");
    writeEvidence(dir, "pass.txt", passBody);
    const passed = recordOutcome(charter(), {
      status: "pass",
      evidence_refs: ["pass.txt"],
      checks: [{ id: "login-empty-password", result: "pass", observed: "HTTP/1.1 422" }]
    }, failed.state, { evidenceRoot: dir });
    assert.equal(passed.code, "PASSED");
    assert.equal(passed.state.status, "passed");
    assert.equal(passed.state.open_failure, null);
    assert.equal(passed.state.charter_hash, frozen.state.charter_hash);
  });

  it("records through the CLI and leaves RESUME.md only while the failure is open", () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), "tests-expert-cli-"));
    const charterFile = path.join(dir, "charter.json");
    const stateFile = path.join(dir, "state.json");
    const outcomeFile = path.join(dir, "outcome.json");
    const evidence = path.join(dir, "evidence.txt");
    fs.writeFileSync(charterFile, `${JSON.stringify(charter())}\n`);
    fs.writeFileSync(evidence, [
      "login-empty-password",
      "curl -s -D - -d password= http://127.0.0.1:3000/login",
      "HTTP/1.1 200"
    ].join("\n"));
    fs.writeFileSync(outcomeFile, JSON.stringify({
      status: "fail",
      evidence_refs: ["evidence.txt"],
      checks: [{ id: "login-empty-password", result: "fail", observed: "HTTP/1.1 200" }]
    }));

    const freeze = spawnSync(process.execPath, [scriptPath, "freeze", "--charter", charterFile, "--state", stateFile], { encoding: "utf8" });
    assert.equal(freeze.status, 0, freeze.stderr);

    const recorded = spawnSync(process.execPath, [
      scriptPath, "record",
      "--charter", charterFile,
      "--state", stateFile,
      "--outcome", outcomeFile,
      "--evidence-root", dir
    ], { encoding: "utf8" });
    assert.equal(recorded.status, 3, recorded.stderr);
    assert.equal(fs.existsSync(path.join(dir, "RESUME.md")), true);
    assert.match(fs.readFileSync(path.join(dir, "RESUME.md"), "utf8"), /senha vazia/);

    const resume = spawnSync(process.execPath, [scriptPath, "resume", "--state", stateFile], { encoding: "utf8" });
    assert.equal(resume.status, 0, resume.stderr);
    assert.match(resume.stdout, /tests-expert open failure/);

    const edited = charter();
    edited.checks[0].expect = "An empty password is accepted.";
    fs.writeFileSync(charterFile, `${JSON.stringify(edited)}\n`);
    const tamper = spawnSync(process.execPath, [scriptPath, "freeze", "--charter", charterFile, "--state", stateFile], { encoding: "utf8" });
    assert.equal(tamper.status, 2, tamper.stdout);
    assert.match(tamper.stderr, /ORACLE_TAMPERED/);
  });
});

describe("tests-expert package", () => {
  it("keeps the canonical SKILL.md at or under 100 lines and points modules from it", () => {
    const skillDir = path.join(repoRoot, "skills/tests-expert");
    const text = fs.readFileSync(path.join(skillDir, "SKILL.md"), "utf8");
    const lines = text.endsWith("\n") ? text.slice(0, -1).split("\n") : text.split("\n");
    assert.ok(lines.length <= 100, `SKILL.md has ${lines.length} lines`);
    assert.equal(fs.existsSync(path.join(skillDir, "README.md")), false);
    const body = /^---\n[\s\S]*?\n---\n([\s\S]*)$/.exec(text)[1];
    for (const reference of fs.readdirSync(path.join(skillDir, "references"))) {
      assert.ok(body.includes(`references/${reference}`), reference);
    }
    assert.match(fs.readFileSync(path.join(skillDir, "PERMISSIONS.yaml"), "utf8"), /^owner_agent: codenavi-agent$/m);
    const description = /^description: "(.*)"$/m.exec(text)[1];
    const stub = fs.readFileSync(path.join(repoRoot, ".agents/skills/tests-expert/SKILL.md"), "utf8");
    assert.equal(/^description: "(.*)"$/m.exec(stub)[1], description);
    assert.match(stub, /skills\/tests-expert\/SKILL\.md/);
    assert.ok(description.length <= 1024);
    assert.match(description, /Use when/);
    assert.match(description, /Do NOT use for/);
  });
});
