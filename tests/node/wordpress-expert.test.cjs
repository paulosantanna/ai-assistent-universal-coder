const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const repoRoot = path.resolve(__dirname, "../..");
function moduleUrl(relativePath) { return pathToFileURL(path.join(repoRoot, relativePath)).href; }

describe("AEOS WordPress Expert MCP and super skill", () => {
  let governance;
  let server;
  let router;
  const setup = typeof beforeAll === "function" ? beforeAll : before;

  setup(async () => {
    governance = await import(moduleUrl("scripts/aeos-wordpress-governance.mjs"));
    server = await import(moduleUrl("aeos/mcp-servers/wordpress-expert-mcp.mjs"));
    router = await import(moduleUrl("scripts/aeos-skill-router.mjs"));
  });

  it("classifies official WordPress sources as normative and Reddit as secondary", () => {
    assert.equal(governance.classifyKnowledgeUrl("https://developer.wordpress.org/rest-api/").authority, "normative");
    assert.equal(governance.classifyKnowledgeUrl("https://www.reddit.com/r/Wordpress/").authority, "community-secondary");
    assert.throws(() => governance.classifyKnowledgeUrl("https://example.com/wordpress"), /not allowlisted/);
  });

  it("creates the Beta map exactly once and reuses it afterwards", () => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), "aeos-wp-beta-"));
    try {
      const site = "https://example.org";
      const first = governance.persistBetaMapOnce(site, { beta_status: "CONSOLIDATED", discovery: { route_count: 10 } }, root);
      const second = governance.persistBetaMapOnce(site, { beta_status: "REPLACEMENT_SHOULD_NOT_WIN", discovery: { route_count: 999 } }, root);
      assert.equal(first.status, "CREATED");
      assert.equal(first.first_run, true);
      assert.equal(second.status, "REUSED");
      assert.equal(second.first_run, false);
      assert.equal(second.map.discovery.route_count, 10);
      assert.equal(second.map.beta_status, "CONSOLIDATED");
      assert.equal(governance.betaMapStatus(site, root).exists, true);
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
    }
  });

  it("defaults all WordPress mutations to denied", () => {
    const gate = governance.mutationGate("wordpress.content.upsert", { env: {} });
    assert.equal(gate.allowed, false);
    assert.equal(gate.reason, "WORDPRESS_MUTATION_MODE_READ_ONLY");
  });

  it("requires a double gate for permanent deletion", () => {
    const env = { AEOS_WORDPRESS_MUTATION_MODE: "approved-write", AEOS_WORDPRESS_ALLOW_PERMANENT_DELETE: "false" };
    assert.equal(governance.mutationGate("wordpress.content.delete_permanent", { env, permanent: true, confirmation: "PERMANENT_DELETE" }).allowed, false);
    const opened = { ...env, AEOS_WORDPRESS_ALLOW_PERMANENT_DELETE: "true" };
    assert.equal(governance.mutationGate("wordpress.content.delete_permanent", { env: opened, permanent: true, confirmation: "WRONG" }).allowed, false);
    assert.equal(governance.mutationGate("wordpress.content.delete_permanent", { env: opened, permanent: true, confirmation: "PERMANENT_DELETE" }).allowed, true);
  });

  it("redacts WordPress runtime credentials", () => {
    const env = { AEOS_WORDPRESS_APP_PASSWORD: "abcd-efgh-ijkl" };
    const text = governance.redactSensitive("password=abcd-efgh-ijkl Authorization: Basic ZXhhbXBsZQ==", env);
    assert.equal(text.includes("abcd-efgh-ijkl"), false);
    assert.match(text, /\[REDACTED\]/);
  });

  it("builds accessible compact external icon links", () => {
    const plan = governance.buildExternalLinkPlan({ service: "iFood", href: "https://www.ifood.com.br/", label: "Pedir no iFood", icon_url: "https://www.ifood.com.br/favicon.ico" });
    assert.equal(plan.presentation, "COMPACT_ICON_LINK");
    assert.equal(plan.icon_policy.favicon_ico_fallback, true);
    assert.equal(plan.accessibility.aria_label, "Pedir no iFood");
    assert.match(plan.html_attributes.rel, /noopener/);
  });

  it("exposes the complete governed WordPress MCP tool surface", () => {
    const names = new Set(server.toolsForWordPress().map((entry) => entry.name));
    for (const required of [
      "wordpress.knowledge.search",
      "wordpress.site.map_beta",
      "wordpress.site.map_get",
      "wordpress.content.upsert",
      "wordpress.design.update",
      "wordpress.media.import_url",
      "wordpress.integrations.link_plan",
      "wordpress.admin.session_plan"
    ]) assert.equal(names.has(required), true, `missing tool ${required}`);
    assert.equal(names.has("shell.exec"), false);
    assert.equal(names.has("wordpress.database.write"), false);
  });

  it("loads wordpress-expert from active overlay skill fragments", () => {
    const skills = router.loadActiveSkills();
    const wordpress = skills.find((skill) => skill.id === "wordpress-expert");
    assert.ok(wordpress);
    assert.equal(wordpress.ownerAgent, "codenavi-agent");
    assert.equal(wordpress.riskLevel, "critical");
    assert.equal(wordpress.registryFragment, "skills.wordpress-expert.additions.yaml");
  });

  it("keeps WordPress secrets out of declarative config and tracked skill files", () => {
    const files = [
      "aeos/mcps/wordpress-expert.mcp.yaml",
      "skills/wordpress-expert/SKILL.md",
      "skills/wordpress-expert/POLICY.md",
      "skills/wordpress-expert/PERMISSIONS.yaml"
    ];
    for (const relative of files) {
      const text = fs.readFileSync(path.join(repoRoot, relative), "utf8");
      assert.equal(/AEOS_WORDPRESS_APP_PASSWORD:\s*[^e\n]/.test(text), false);
      assert.equal(/wordpress_app_password:\s*\S+/i.test(text), false);
    }
  });
});
