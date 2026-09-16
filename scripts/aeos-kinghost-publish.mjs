#!/usr/bin/env node
import { resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { randomUUID } from "node:crypto";

const PLAYBOOK_ID = "kinghost-wordpress-publish";
const USAGE = "Usage: npm run aeos:kinghost:publish -- --local-dir <wordpress-tree> --domain <existing-kinghost-domain> [--environment production] [--apply] [--include-uploads] [--replace-database] [--change-id id] [--rollback-ref ref]";

function parseArgs(argv) {
  const out = {
    localDir: process.cwd(),
    domain: "",
    environment: "production",
    apply: false,
    includeUploads: false,
    replaceDatabase: false,
    changeId: "",
    rollbackRef: ""
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = argv[i + 1];
    if (arg === "--local-dir" && next) {
      out.localDir = next;
      i += 1;
    } else if (arg === "--domain" && next) {
      out.domain = next;
      i += 1;
    } else if ((arg === "--environment" || arg === "--env") && next) {
      out.environment = next;
      i += 1;
    } else if (arg === "--change-id" && next) {
      out.changeId = next;
      i += 1;
    } else if (arg === "--rollback-ref" && next) {
      out.rollbackRef = next;
      i += 1;
    } else if (arg === "--apply") {
      out.apply = true;
    } else if (arg === "--include-uploads") {
      out.includeUploads = true;
    } else if (arg === "--replace-database") {
      out.replaceDatabase = true;
    } else if (arg === "--help" || arg === "-h") {
      out.help = true;
    } else if (arg.startsWith("-")) {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  out.localDir = resolve(out.localDir);
  return out;
}

function approvedFromEnv() {
  const raw = String(process.env.AEOS_KINGHOST_APPROVED || "").trim().toLowerCase();
  return raw === "true" || raw === "1" || raw === "yes";
}

export async function runKinghostPublish(rawArgs = [], options = {}) {
  const args = parseArgs(rawArgs);
  if (args.help) {
    return { success: true, data: { usage: USAGE, playbook_id: PLAYBOOK_ID } };
  }
  if (args.replaceDatabase) {
    return {
      success: false,
      error: "--replace-database is blocked in the one-command path; use kinghost-expert-production-lifecycle with high_risk_approved",
      code: "BLOCKED",
      playbook_id: PLAYBOOK_ID
    };
  }

  const dispatch = options.dispatch || (await loadDispatch());
  const preflight = await dispatch("kinghost_control.publish.preflight", {
    workspace_root: args.localDir,
    domain: args.domain,
    environment_id: args.environment,
    include_uploads: args.includeUploads,
    replace_database: args.replaceDatabase
  });
  if (!preflight.success) {
    return { success: false, error: preflight.error, code: preflight.code || "PREFLIGHT_FAILED", playbook_id: PLAYBOOK_ID };
  }
  if (preflight.data.status === "BLOCKED") {
    return failClosed(
      (preflight.data.blocking_conditions || []).join("; ") || "publish preflight blocked",
      preflight,
      [{ action: "kinghost_control.publish.preflight", status: "BLOCKED" }],
      preflight
    );
  }

  const steps = [
    { action: "kinghost_control.publish.preflight", status: preflight.data.status }
  ];

  let changeId = args.changeId || preflight.data.change_id || "";
  if (args.domain) {
    const listed = await dispatch("kinghost_control.domain.list", {});
    steps.push({ action: "kinghost_control.domain.list", status: listed.success ? "OK" : "FAILED" });
    if (!listed.success) return failClosed("domain.list failed", listed, steps, preflight);
    const selected = await dispatch("kinghost_control.domain.select", {
      domain: args.domain,
      environment_id: args.environment,
      change_id: changeId || undefined
    });
    steps.push({ action: "kinghost_control.domain.select", status: selected.success ? "OK" : "FAILED" });
    if (!selected.success) return failClosed(selected.error || "domain.select failed", selected, steps, preflight);
    changeId = selected.data.change_id || changeId;
  } else {
    const env = await dispatch("kinghost_control.environment.select", {
      environment_id: args.environment,
      change_id: changeId || undefined
    });
    steps.push({ action: "kinghost_control.environment.select", status: env.success ? "OK" : "FAILED" });
    if (!env.success) return failClosed(env.error || "environment.select failed", env, steps, preflight);
    changeId = env.data.change_id || changeId;
  }

  const ftpBound = Boolean(process.env.KINGHOST_FTP_USER && process.env.KINGHOST_FTP_PASSWORD && process.env.KINGHOST_FTP_HOST);
  let deploy = null;
  if (ftpBound) {
    const bound = await dispatch("kinghost_control.credential.bind", {
      kind: "ftp",
      source_class: "env_reference",
      username_env: "KINGHOST_FTP_USER",
      password_env: "KINGHOST_FTP_PASSWORD",
      host_env: "KINGHOST_FTP_HOST",
      port_env: "KINGHOST_FTP_PORT",
      environment_id: args.environment
    });
    steps.push({ action: "kinghost_control.credential.bind", status: bound.success ? "OK" : "FAILED" });
    if (!bound.success) return failClosed(bound.error || "credential.bind failed", bound, steps, preflight);

    const ftp = await dispatch("kinghost_control.ftp.session.open", {
      credential_ref: bound.data.credential_ref,
      remote_root: preflight.data.inspection?.remote_root || "wp-content"
    });
    steps.push({ action: "kinghost_control.ftp.session.open", status: ftp.success ? "OK" : "FAILED" });
    if (!ftp.success) return failClosed(ftp.error || "ftp.session.open failed", ftp, steps, preflight);

    const rollbackRef = args.rollbackRef || `dry-run-${changeId || randomUUID()}`;
    const deployParams = {
      session_ref: ftp.data.session_ref,
      workspace_root: args.localDir,
      local_dir: preflight.data.inspection?.local_dir || args.localDir,
      remote_root: preflight.data.inspection?.remote_root || "wp-content",
      include_uploads: args.includeUploads,
      dry_run: !args.apply,
      change_id: changeId,
      rollback_ref: rollbackRef,
      approved: args.apply ? approvedFromEnv() : true
    };
    if (args.apply) {
      if (!approvedFromEnv()) {
        return failClosed("AEOS_KINGHOST_APPROVED=true is required for --apply", { error: "approval missing" }, steps, preflight);
      }
      if (args.replaceDatabase) {
        return failClosed("--replace-database is blocked in the one-command path; use kinghost-expert-production-lifecycle with high_risk_approved", { error: "replace-database blocked" }, steps, preflight);
      }
      deployParams.approved = true;
    }
    deploy = await dispatch("kinghost_control.deploy.workspace_to_production", deployParams);
    steps.push({
      action: "kinghost_control.deploy.workspace_to_production",
      status: deploy.success ? deploy.data.status : "FAILED"
    });
    if (!deploy.success) return failClosed(deploy.error || "deploy failed", deploy, steps, preflight);
  }

  const status = args.apply
    ? (deploy?.data?.status === "APPLIED" ? "APPLIED" : "BLOCKED")
    : "DRY_RUN";

  return {
    success: true,
    data: {
      playbook_id: PLAYBOOK_ID,
      status,
      domain: args.domain || null,
      environment_id: args.environment,
      change_id: changeId || null,
      apply_requested: args.apply,
      ftp_bound: ftpBound,
      inspection: preflight.data.inspection,
      woocommerce: preflight.data.woocommerce,
      credential_presence: preflight.data.credential_presence,
      deploy: deploy?.data || preflight.data.deploy_plan,
      steps,
      next: nextActions({ ftpBound, apply: args.apply, domain: args.domain, status }),
      one_command: preflight.data.inspection?.one_command
    }
  };
}

function nextActions({ ftpBound, apply, domain, status }) {
  if (!domain) return ["Pass --domain for an existing KingHost Hospedagem domain."];
  if (!ftpBound) {
    return [
      "Bind already-created FTP credentials via KINGHOST_FTP_USER / KINGHOST_FTP_PASSWORD / KINGHOST_FTP_HOST.",
      "Re-run the same command for DRY_RUN FTP evidence."
    ];
  }
  if (!apply && status === "DRY_RUN") {
    return [
      "Review the dry-run file list.",
      "CREATE a rollback_ref snapshot.",
      "Re-run with --apply, --change-id, --rollback-ref and AEOS_KINGHOST_APPROVED=true."
    ];
  }
  if (status === "APPLIED") {
    return ["VERIFY homepage and WooCommerce routes with cookie/Playwright.", "CLOSE FTP/MySQL/panel sessions."];
  }
  return ["Follow kinghost-wordpress-publish blocking conditions."];
}

function failClosed(error, result, steps, preflight) {
  return {
    success: false,
    error,
    code: result?.code || "BLOCKED",
    playbook_id: PLAYBOOK_ID,
    data: {
      playbook_id: PLAYBOOK_ID,
      status: "BLOCKED",
      steps,
      inspection: preflight?.data?.inspection || null,
      woocommerce: preflight?.data?.woocommerce || null
    }
  };
}

async function loadDispatch() {
  const url = pathToFileURL(resolve(process.cwd(), "kinghost-control-mcp/index.mjs")).href;
  const mod = await import(url);
  return mod.dispatch;
}

const isMain = process.argv[1]
  ? resolve(process.argv[1]).toLowerCase() === fileURLToPath(import.meta.url).toLowerCase()
  : false;

if (isMain) {
  try {
    const result = await runKinghostPublish(process.argv.slice(2));
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.success ? 0 : 2);
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error instanceof Error ? error.message : String(error),
      usage: USAGE,
      playbook_id: PLAYBOOK_ID
    }, null, 2));
    process.exit(1);
  }
}
