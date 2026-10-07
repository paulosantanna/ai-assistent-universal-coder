const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const repoRoot = path.resolve(__dirname, "../..");
const SKILLS = [
  "architecture-decision-record",
  "architecture-decision-log",
  "architecturally-significant-requirement",
  "architecture-knowledge-management"
];

function load(relativePath) {
  return import(pathToFileURL(path.join(repoRoot, relativePath)).href);
}

function tempLog(files) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "aeos-adl-"));
  for (const [name, content] of Object.entries(files)) fs.writeFileSync(path.join(dir, name), content);
  return dir;
}

function madr({ title, status, date, extra = "" }) {
  return [
    "---",
    `status: ${status}`,
    `date: ${date}`,
    "---",
    `# ${title}`,
    "## Context and Problem Statement",
    `Context for ${title}. ${extra}`,
    "## Considered Options",
    "* Option A",
    "* Option B",
    "## Decision Outcome",
    'Chosen option: "Option A", because it meets the drivers.',
    "### Consequences",
    "* Good, because it is simple.",
    "* Bad, because it adds operations work.",
    "### Confirmation",
    "Design review.",
    ""
  ].join("\n");
}

describe("Architecture knowledge skills (TLC skill format)", () => {
  it("ship SKILL.md packages that satisfy the TLC skill-architect contract", () => {
    for (const skill of SKILLS) {
      const dir = path.join(repoRoot, "skills", skill);
      const text = fs.readFileSync(path.join(dir, "SKILL.md"), "utf8");
      const [, frontmatter, body] = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/.exec(text);
      assert.match(frontmatter, new RegExp(`^name: ${skill}$`, "m"), skill);
      const description = /^description: (.*)$/m.exec(frontmatter)[1];
      assert.ok(description.length <= 1024, `${skill} description too long`);
      assert.match(description, /Use when/, skill);
      assert.match(description, /Do NOT use for/, skill);
      assert.doesNotMatch(description, /[<>]/, skill);
      assert.match(frontmatter, /^license: CC-BY-4\.0$/m, skill);
      assert.match(frontmatter, /^ {2}author: \S/m, skill);
      assert.match(frontmatter, /^ {2}version: \d+\.\d+\.\d+$/m, skill);
      assert.ok(body.trim().split("\n").length < 500, `${skill} body over 500 lines`);
      assert.match(body, /Governance: CodENavi v1/, skill);
      assert.match(body, /codenavi-agent/, skill);
      assert.equal(fs.existsSync(path.join(dir, "README.md")), false, `${skill} must not ship README.md`);
      for (const file of ["AGENT.md", "POLICY.md", "PERMISSIONS.yaml"]) assert.ok(fs.existsSync(path.join(dir, file)), `${skill}/${file}`);
      assert.match(fs.readFileSync(path.join(dir, "PERMISSIONS.yaml"), "utf8"), /^owner_agent: codenavi-agent$/m, skill);
      for (const reference of fs.readdirSync(path.join(dir, "references"))) {
        assert.ok(body.includes(`references/${reference}`), `${skill} does not reference references/${reference}`);
      }
    }
  });

  it("keeps the TLC create-adr baseline verbatim with its CC-BY-4.0 attribution", () => {
    const original = fs.readFileSync(path.join(repoRoot, "skills/architecture-decision-record/references/ORIGINAL_SKILL.md"), "utf8");
    assert.match(original, /^name: create-adr$/m);
    assert.match(original, /^license: CC-BY-4\.0$/m);
    assert.match(original, /author: Tech Leads Club/);
    const template = fs.readFileSync(path.join(repoRoot, "skills/architecture-decision-record/assets/madr-template.md"), "utf8");
    assert.match(template, /### Confirmation/);
    assert.match(template, /decision-makers:/);
  });
});

describe("adr_lint", () => {
  it("passes a complete MADR 4.0.0 record in strict mode and leaves path parameters alone", async () => {
    const { lintAdr } = await load("skills/architecture-decision-record/scripts/adr_lint.mjs");
    const result = lintAdr(madr({ title: "Use PostgreSQL for orders", status: "accepted", date: "2026-10-07", extra: "Contract `/orders/{orderId}` and /users/{userId}." }), { strict: true });
    assert.equal(result.status, "PASS", JSON.stringify(result.errors));
    assert.equal(result.format, "madr");
    assert.equal(result.adr_status.value, "accepted");
    assert.equal(result.options_count, 2);
  });

  it("rejects question titles, missing sections and leftover template placeholders", async () => {
    const { lintAdr } = await load("skills/architecture-decision-record/scripts/adr_lint.mjs");
    const bad = lintAdr("# Should we use Kafka?\n\n## Context\n\nAdmins are bored.\n\n## Decision Outcome\n\nWe use Kafka.\n");
    const codes = bad.errors.map((item) => item.code);
    for (const code of ["TITLE_IS_QUESTION", "STATUS_MISSING", "OPTIONS_MISSING", "CONSEQUENCES_MISSING"]) assert.ok(codes.includes(code), code);
    const template = fs.readFileSync(path.join(repoRoot, "skills/architecture-decision-record/assets/madr-template.md"), "utf8");
    assert.ok(lintAdr(template).errors.some((item) => item.code === "PLACEHOLDER_LEFT"));
  });

  it("promotes authoring warnings to errors only in strict mode", async () => {
    const { lintAdr } = await load("skills/architecture-decision-record/scripts/adr_lint.mjs");
    const record = madr({ title: "Use Redis for sessions", status: "accepted", date: "2026-10-07" }).replace("### Confirmation\nDesign review.\n", "");
    assert.equal(lintAdr(record).status, "PASS");
    assert.ok(lintAdr(record).warnings.some((item) => item.code === "CONFIRMATION_MISSING"));
    assert.equal(lintAdr(record, { strict: true }).status, "FAIL");
  });

  it("reads Portuguese Y-statements and Nygard supersession links", async () => {
    const { lintAdr } = await load("skills/architecture-decision-record/scripts/adr_lint.mjs");
    const y = lintAdr("# ADR-0004: Usar fila para notificações\n\n**Data**: 2026-10-01 | **Status**: Aceito\n\nNo contexto do serviço de notificações, diante de picos de 10x, decidimos por uma fila gerenciada, para alcançar entrega garantida, aceitando latência adicional.\n", { strict: true });
    assert.equal(y.status, "PASS", JSON.stringify(y.errors));
    assert.equal(y.format, "y-statement");
    assert.equal(y.adr_status.value, "accepted");
    const nygard = lintAdr("# ADR 3: LDAP for tenants\n\n## Status\n\nSuperseded by [OIDC](0009-oidc-federation.md)\n\n## Context\n\nTenants.\n\n## Decision\n\nWe will use LDAP.\n\n## Consequences\n\nOnboarding slows down.\n");
    assert.equal(nygard.format, "nygard");
    assert.equal(nygard.adr_status.superseded_by, "ADR-0009");
  });

  it("recognizes the workspace ADR template used by aeos/docs/adr", async () => {
    const { lintAdr } = await load("skills/architecture-decision-record/scripts/adr_lint.mjs");
    const text = fs.readFileSync(path.join(repoRoot, "aeos/docs/adr/ADR-0001-WORKSPACE-OS-STRANGLER.md"), "utf8");
    const result = lintAdr(text);
    assert.equal(result.format, "aeos-template");
    assert.equal(result.adr_status.value, "proposed");
    assert.equal(result.options_count, 5);
    assert.equal(result.status, "PASS");
    assert.ok(result.warnings.some((item) => item.code === "DATE_MISSING"));
  });
});

describe("adl_index", () => {
  it("reports duplicates, gaps, stale proposals and broken supersession", async () => {
    const { scanLog } = await load("skills/architecture-decision-log/scripts/adl_index.mjs");
    const dir = tempLog({
      "0001-use-postgresql.md": madr({ title: "Use PostgreSQL for sessions", status: "superseded by ADR-0003", date: "2026-01-10" }),
      "0002-use-rest.md": madr({ title: "Use REST for partners", status: "proposed", date: "2026-08-01" }),
      "0003-use-redis.md": madr({ title: "Use Redis for sessions", status: "accepted", date: "2026-09-01" }),
      "0003-duplicate.md": madr({ title: "Duplicate number", status: "accepted", date: "2026-09-02" }),
      "0005-use-kafka.md": madr({ title: "Use Kafka", status: "superseded by ADR-0009", date: "2026-09-03" }),
      "README.md": "# Decisions\n",
      "adr-template.md": "# {short title}\n"
    });
    try {
      const log = scanLog(dir, { today: "2026-10-07", staleDays: 30 });
      const codes = log.integrity.map((item) => item.code);
      assert.equal(log.status, "FAIL");
      for (const code of ["DUPLICATE_NUMBER", "NUMBER_GAP", "STALE_PROPOSAL", "SUPERSEDED_TARGET_MISSING", "SUPERSEDE_BACKLINK_MISSING"]) assert.ok(codes.includes(code), code);
      assert.deepEqual(log.ignored.sort(), ["README.md", "adr-template.md"]);
      assert.deepEqual(log.lifecycle.stale_proposals, ["ADR-0002"]);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it("detects supersession cycles", async () => {
    const { scanLog } = await load("skills/architecture-decision-log/scripts/adl_index.mjs");
    const dir = tempLog({
      "0001-a.md": madr({ title: "A", status: "superseded by ADR-0002", date: "2026-01-01", extra: "ADR-0002" }),
      "0002-b.md": madr({ title: "B", status: "superseded by ADR-0001", date: "2026-01-02", extra: "ADR-0001" })
    });
    try {
      assert.ok(scanLog(dir, { today: "2026-10-07" }).integrity.some((item) => item.code === "SUPERSESSION_CYCLE"));
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it("never reuses numbers and keeps the log's own naming convention", async () => {
    const { scanLog } = await load("skills/architecture-decision-log/scripts/adl_index.mjs");
    const dir = tempLog({
      "0001-a.md": madr({ title: "A", status: "accepted", date: "2026-01-01" }),
      "0004-d.md": madr({ title: "D", status: "accepted", date: "2026-01-04" })
    });
    try {
      const next = scanLog(dir, { today: "2026-10-07", nextTitle: "Adotar OpenTelemetry para tracing" }).next;
      assert.equal(next.id, "ADR-0005");
      assert.equal(next.file, "0005-adotar-opentelemetry-para-tracing.md");
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
    const workspace = scanLog(path.join(repoRoot, "aeos/docs/adr"), { today: "2026-10-07", nextTitle: "Architecture knowledge MCP" });
    assert.equal(workspace.status, "PASS");
    assert.equal(workspace.next.file, "ADR-0002-ARCHITECTURE-KNOWLEDGE-MCP.md");
  });

  it("rewrites only the marked index block, idempotently, inside the log directory", async () => {
    const { scanLog, writeIndex } = await load("skills/architecture-decision-log/scripts/adl_index.mjs");
    const dir = tempLog({
      "0001-a.md": madr({ title: "Use A | not B", status: "accepted", date: "2026-01-01" }),
      "README.md": "# Decisions\n\nHand-written intro.\n"
    });
    try {
      const index = path.join(dir, "README.md");
      const { index_markdown: markdown } = scanLog(dir, { today: "2026-10-07" });
      assert.match(markdown, /Use A \\\| not B/);
      assert.equal(writeIndex(dir, index, markdown).written, true);
      assert.equal(writeIndex(dir, index, markdown).written, false);
      const text = fs.readFileSync(index, "utf8");
      assert.match(text, /Hand-written intro\./);
      assert.match(text, /<!-- adl:index:start -->[\s\S]*\[ADR-0001\]\(0001-a\.md\)[\s\S]*<!-- adl:index:end -->/);
      assert.throws(() => writeIndex(dir, path.join(os.tmpdir(), "outside-index.md"), markdown), /inside the ADR directory/);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });
});

describe("asr_test", () => {
  it("reproduces the published ASR Test example bands", async () => {
    const { assessAsr } = await load("skills/architecturally-significant-requirement/scripts/asr_test.mjs");
    const none = { C1: "N", C2: "N", C3: "N", C4: "N", C5: "N", C6: "N", C7: "N" };
    const cases = [
      [{ ...none, C1: "Y", C2: "Y", C4: "Y", C5: "Y" }, "high", "significant"],
      [{ ...none, key_concern: "Y", new_qos: "H" }, "medium-high", "significant"],
      [{ ...none, cross_cutting: true }, "low-medium", "borderline"],
      [none, "low", "not-significant"]
    ];
    for (const [criteria, band, significance] of cases) {
      const result = assessAsr({ requirement: "example", criteria });
      assert.equal(result.band, band);
      assert.equal(result.significance, significance);
    }
  });

  it("keeps unknown criteria open and checks the six-part scenario", async () => {
    const { assessAsr } = await load("skills/architecturally-significant-requirement/scripts/asr_test.mjs");
    const result = assessAsr({
      requirement: "Partners call the pricing API at 10,000 requests per minute",
      criteria: { C1: "Y", C3: "?", C4: "?" },
      scenario: { source: "partner", stimulus: "burst", environment: "peak", artifact: "pricing API", response: "served", response_measure: "fast" }
    });
    assert.equal(result.significance, "open");
    assert.equal(result.open, true);
    assert.ok(result.unknown.includes("C3"));
    assert.equal(result.scenario.complete, true);
    assert.equal(result.scenario.measurable_response, false);
  });

  it("blocks malformed input instead of guessing", async () => {
    const { assessAsr } = await load("skills/architecturally-significant-requirement/scripts/asr_test.mjs");
    assert.equal(assessAsr({ criteria: { C1: "Y" } }).reason, "REQUIREMENT_REQUIRED");
    assert.equal(assessAsr({ requirement: "x" }).reason, "CRITERIA_REQUIRED");
    assert.equal(assessAsr({ requirement: "x", criteria: { C9: "Y" } }).reason, "UNKNOWN_CRITERION");
    assert.equal(assessAsr({ requirement: "x", criteria: { C1: "maybe" } }).reason, "INVALID_CRITERION_VALUE");
  });
});
