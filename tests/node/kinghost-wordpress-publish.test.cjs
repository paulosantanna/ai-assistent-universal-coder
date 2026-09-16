const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const repoRoot = path.resolve(__dirname, "../..");
function moduleUrl(relativePath) {
  return pathToFileURL(path.join(repoRoot, relativePath)).href;
}

function makeWordpressTree() {
  const tree = fs.mkdtempSync(path.join(os.tmpdir(), "kinghost-publish-"));
  fs.mkdirSync(path.join(tree, "wp-content", "themes", "demo"), { recursive: true });
  fs.mkdirSync(path.join(tree, "wp-content", "plugins", "woocommerce"), { recursive: true });
  fs.writeFileSync(path.join(tree, "wp-content", "plugins", "woocommerce", "woocommerce.php"), "<?php");
  fs.writeFileSync(path.join(tree, "wp-content", "themes", "demo", "style.css"), "/* theme */");
  return tree;
}

describe("KingHost WordPress one-command publish", () => {
  it("registers the publish playbook and npm script", () => {
    const overlay = fs.readFileSync(path.join(repoRoot, "aeos/registries/playbooks.kinghost-expert.additions.yaml"), "utf8");
    assert.match(overlay, /id: kinghost-wordpress-publish/);
    assert.match(overlay, /kinghost-wordpress-publish\.playbook\.md/);
    const playbook = fs.readFileSync(path.join(repoRoot, "aeos/playbooks/kinghost-wordpress-publish.playbook.md"), "utf8");
    assert.match(playbook, /npm run aeos:kinghost:publish/);
    assert.match(playbook, /preserve_on_production|orders/);
    assert.match(playbook, /WooCommerce/);
    const pkg = JSON.parse(fs.readFileSync(path.join(repoRoot, "package.json"), "utf8"));
    assert.equal(pkg.scripts["aeos:kinghost:publish"], "node scripts/aeos-kinghost-publish.mjs");
  });

  it("dry-runs preflight against a local WooCommerce tree without FTP", async () => {
    const { runKinghostPublish } = await import(moduleUrl("scripts/aeos-kinghost-publish.mjs"));
    const tree = makeWordpressTree();
    process.env.KINGHOST_DOMAINS = "loja.example.com.br";
    try {
      const result = await runKinghostPublish(["--local-dir", tree, "--domain", "loja.example.com.br"]);
      assert.equal(result.success, true);
      assert.equal(result.data.playbook_id, "kinghost-wordpress-publish");
      assert.equal(result.data.status, "DRY_RUN");
      assert.equal(result.data.ftp_bound, false);
      assert.equal(result.data.inspection.woocommerce_plugin_present, true);
      assert.equal(result.data.apply_requested, false);
      assert.ok(result.data.next.some((item) => /KINGHOST_FTP_USER/i.test(item)));
    } finally {
      fs.rmSync(tree, { recursive: true, force: true });
      delete process.env.KINGHOST_DOMAINS;
    }
  });

  it("blocks --apply without AEOS_KINGHOST_APPROVED and blocks database replace", async () => {
    const { runKinghostPublish } = await import(moduleUrl("scripts/aeos-kinghost-publish.mjs"));
    const tree = makeWordpressTree();
    process.env.KINGHOST_DOMAINS = "loja.example.com.br";
    process.env.KINGHOST_FTP_USER = "ftp-user";
    process.env.KINGHOST_FTP_PASSWORD = "ftp-secret-do-not-leak";
    process.env.KINGHOST_FTP_HOST = "ftp.loja.example.com.br";
    delete process.env.AEOS_KINGHOST_APPROVED;
    const fakeDispatch = async (action) => {
      if (action === "kinghost_control.publish.preflight") {
        const { dispatch } = await import(moduleUrl("kinghost-control-mcp/index.mjs"));
        return dispatch(action, { workspace_root: tree, domain: "loja.example.com.br" });
      }
      if (action === "kinghost_control.domain.list") {
        return { success: true, data: { domains: [{ domain: "loja.example.com.br" }] } };
      }
      if (action === "kinghost_control.domain.select") {
        return { success: true, data: { domain: "loja.example.com.br", change_id: "chg-1", fsm_state: "ENV_SELECTED" } };
      }
      if (action === "kinghost_control.credential.bind") {
        return { success: true, data: { credential_ref: "cred_test", username: "ftp-user", has_secret: true } };
      }
      if (action === "kinghost_control.ftp.session.open") {
        return { success: true, data: { session_ref: "ftp_test", remote_root: "wp-content" } };
      }
      if (action === "kinghost_control.deploy.workspace_to_production") {
        return { success: true, data: { status: "APPLIED" } };
      }
      return { success: false, error: `unexpected ${action}` };
    };
    try {
      const apply = await runKinghostPublish(
        ["--local-dir", tree, "--domain", "loja.example.com.br", "--apply", "--change-id", "chg-1", "--rollback-ref", "rb-1"],
        { dispatch: fakeDispatch }
      );
      assert.equal(apply.success, false);
      assert.match(String(apply.error), /AEOS_KINGHOST_APPROVED/);
      assert.equal(JSON.stringify(apply).includes("ftp-secret-do-not-leak"), false);

      const replaceDb = await runKinghostPublish(
        ["--local-dir", tree, "--replace-database"],
        { dispatch: fakeDispatch }
      );
      assert.equal(replaceDb.success, false);
      assert.match(String(replaceDb.error), /replace-database/);
    } finally {
      fs.rmSync(tree, { recursive: true, force: true });
      delete process.env.KINGHOST_DOMAINS;
      delete process.env.KINGHOST_FTP_USER;
      delete process.env.KINGHOST_FTP_PASSWORD;
      delete process.env.KINGHOST_FTP_HOST;
    }
  });
});
