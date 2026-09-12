const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const repoRoot = path.resolve(__dirname, "../..");
function moduleUrl(relativePath) { return pathToFileURL(path.join(repoRoot, relativePath)).href; }

const setup = typeof beforeAll === "function" ? beforeAll : before;

describe("AEOS universal runtime authentication", () => {
  let RuntimeAuthBroker;
  let ToolRouter;
  let EvidenceStore;

  setup(async () => {
    ({ RuntimeAuthBroker } = await import(moduleUrl("runtime/dist/kernel/runtime-auth-broker.js")));
    ({ ToolRouter } = await import(moduleUrl("runtime/dist/kernel/tool-router.js")));
    ({ EvidenceStore } = await import(moduleUrl("runtime/dist/kernel/evidence-store.js")));
  });

  it("opens an external Netscape cookie jar and returns only opaque metadata", () => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), "aeos-auth-"));
    const jar = path.join(temp, "cookies.txt");
    const secret = "wp-secret-cookie-value";
    fs.writeFileSync(jar, `# Netscape HTTP Cookie File\n.example.com\tTRUE\t/\tTRUE\t2147483647\twordpress_logged_in\t${secret}\n`);
    const broker = new RuntimeAuthBroker({ workspaceRoot: repoRoot });
    const info = broker.openCookieFile({ path: jar, allowedHosts: ["example.com"] });
    assert.equal(info.kind, "cookie_file");
    assert.equal(info.cookieCount, 1);
    assert.equal(JSON.stringify(info).includes(secret), false);
    assert.match(info.sessionRef, /^auth_/);
    assert.equal(broker.cookieHeader(info.sessionRef, "https://example.com/wp-admin/").includes(secret), true);
    broker.closeAll();
    fs.rmSync(temp, { recursive: true, force: true });
  });

  it("blocks cookie jars inside the configured workspace", () => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), "aeos-auth-workspace-"));
    const jar = path.join(temp, "cookies.txt");
    fs.writeFileSync(jar, ".example.com\tTRUE\t/\tTRUE\t2147483647\ta\tb\n");
    const broker = new RuntimeAuthBroker({ workspaceRoot: temp });
    assert.throws(() => broker.openCookieFile({ path: jar, allowedHosts: ["example.com"] }), /outside the tracked workspace/);
    fs.rmSync(temp, { recursive: true, force: true });
  });

  it("scopes cookie sessions to approved hosts", () => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), "aeos-auth-host-"));
    const jar = path.join(temp, "cookies.json");
    fs.writeFileSync(jar, JSON.stringify([{ name: "session", value: "abc123", domain: "example.com", path: "/", secure: true }]));
    const broker = new RuntimeAuthBroker({ workspaceRoot: repoRoot });
    const info = broker.openCookieFile({ path: jar, allowedHosts: ["example.com"] });
    assert.throws(() => broker.cookieHeader(info.sessionRef, "https://evil.example.net/"), /not scoped/);
    fs.rmSync(temp, { recursive: true, force: true });
  });

  it("redacts cookie references and values from Tool Router evidence", async () => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), "aeos-auth-router-"));
    const jar = path.join(temp, "cookies.txt");
    const secret = "never-persist-this-cookie";
    fs.writeFileSync(jar, `.example.com\tTRUE\t/\tTRUE\t2147483647\tsession\t${secret}\n`);
    const evidence = new EvidenceStore(path.join(temp, "evidence"));
    const broker = new RuntimeAuthBroker({ workspaceRoot: repoRoot });
    const router = new ToolRouter(evidence, broker);
    router.registerMCP({
      id: "runtime-auth", type: "runtime-auth", config: "aeos/mcps/runtime-auth.mcp.yaml", risk_level: "high",
      capabilities: ["auth.session.open_cookie_file", "auth.session.info", "auth.session.close"], governing_skill: "tool-adapter-governor", skill_enforced: true
    });
    router.setActiveSkill("test-skill");
    const opened = await router.callTool("runtime-auth", "auth.session.open_cookie_file", { cookie_file_path: jar, allowed_hosts: ["example.com"] });
    assert.equal(opened.success, true);
    const serialized = fs.readFileSync(path.join(temp, "evidence", "tool-calls.jsonl"), "utf8");
    assert.equal(serialized.includes(secret), false);
    assert.equal(serialized.includes(jar), false);
    assert.match(serialized, /REDACTED/);
    router.shutdownRuntimeAuth();
    fs.rmSync(temp, { recursive: true, force: true });
  });

  it("loads overlay skills, playbooks and MCPs including core runtime auth", async () => {
    const { RegistryLoader } = await import(moduleUrl("runtime/dist/kernel/registry-loader.js"));
    const loader = new RegistryLoader(repoRoot);
    const skills = loader.loadSkills().skills.map((item) => item.id);
    const playbooks = loader.loadPlaybooks().playbooks.map((item) => item.id);
    const mcps = loader.loadMCPs().mcps.map((item) => item.id);
    assert.equal(skills.includes("wordpress-expert"), true);
    assert.equal(skills.includes("kinghost-expert"), true);
    assert.equal(skills.includes("spec-driven"), true);
    assert.equal(skills.includes("spec-driven-lean"), true);
    assert.equal(skills.includes("not-your-babysitter"), true);
    assert.equal(skills.includes("the-jury"), true);
    assert.equal(skills.includes("ai-seo"), true);
    assert.equal(skills.includes("nx-workspace"), true);
    assert.equal(skills.includes("subagent-creator"), true);
    assert.equal(skills.includes("tlc-plan"), true);
    assert.equal(skills.includes("learning-opportunities"), true);
    assert.equal(skills.includes("perf-astro"), true);
    assert.equal(skills.includes("core-web-vitals"), true);
    assert.equal(skills.includes("perf-lighthouse"), true);
    assert.equal(skills.includes("perf-web-optimization"), true);
    assert.equal(skills.includes("security-best-practices"), true);
    assert.equal(skills.includes("security-ownership-map"), true);
    assert.equal(skills.includes("security-threat-model"), true);
    assert.equal(skills.includes("web-quality-audit"), true);
    assert.equal(playbooks.includes("wordpress-expert-site-lifecycle"), true);
    assert.equal(playbooks.includes("kinghost-expert-production-lifecycle"), true);
    assert.equal(playbooks.includes("spec-driven-feature-lifecycle"), true);
    assert.equal(playbooks.includes("spec-driven-lean-feature-lifecycle"), true);
    assert.equal(playbooks.includes("tlc-catalog-skills"), true);
    assert.equal(mcps.includes("wordpress-knowledge"), true);
    assert.equal(mcps.includes("kinghost-control"), true);
    assert.equal(mcps.includes("kinghost-commerce"), true);
    assert.equal(mcps.includes("runtime-auth"), true);
    assert.equal(mcps.includes("runtime-http"), true);
    const resolved = loader.resolveMCPs(loader.loadMCPs().mcps, ["filesystem-readonly"]).map((item) => item.id);
    assert.equal(resolved.includes("runtime-auth"), true);
    assert.equal(resolved.includes("runtime-http"), true);
  });
});
