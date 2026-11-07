import { mkdirSync, existsSync, writeFileSync, copyFileSync } from "node:fs";
import { join } from "node:path";
import { defaultBrainRoot, loadDotEnvFile, packageRoot } from "./config.mjs";

const LAYOUT = ["corpus", "corpus/chunks", "manifests", "events", "logs", "mcp", "skills", "playbooks", "config"];

export function getBrainRoot() {
  const root = defaultBrainRoot();
  loadDotEnvFile(root);
  return root;
}

export function ensureLayout(root = getBrainRoot()) {
  for (const part of LAYOUT) {
    const dir = join(root, part);
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  }
  const contractPath = join(root, "manifests", "model-contract.json");
  if (!existsSync(contractPath)) {
    writeFileSync(
      contractPath,
      JSON.stringify(
        {
          provider: "deepseek",
          chat_model: "deepseek-chat",
          embedding_model: null,
          opencode_profile: "default",
          base_url: "https://api.deepseek.com",
          note: "Ajuste chat_model quando o OpenCode expuser DeepSeek 4.1 pelo id oficial.",
        },
        null,
        2,
      ) + "\n",
      "utf8",
    );
  }
  const pkg = packageRoot();
  const skillSrc = join(pkg, "skills", "workspace-brain", "SKILL.md");
  const skillDst = join(root, "skills", "workspace-brain", "SKILL.md");
  if (existsSync(skillSrc) && !existsSync(skillDst)) {
    mkdirSync(join(root, "skills", "workspace-brain"), { recursive: true });
    copyFileSync(skillSrc, skillDst);
  }
  const pbSrc = join(pkg, "playbooks", "workspace-brain-operate.md");
  const pbDst = join(root, "playbooks", "workspace-brain-operate.md");
  if (existsSync(pbSrc) && !existsSync(pbDst)) {
    copyFileSync(pbSrc, pbDst);
  }
  return root;
}

export function paths(root = getBrainRoot()) {
  return {
    root,
    corpus: join(root, "corpus"),
    chunks: join(root, "corpus", "chunks"),
    index: join(root, "corpus", "index.json"),
    manifests: join(root, "manifests"),
    events: join(root, "events", "events.ndjson"),
    logs: join(root, "logs"),
    skills: join(root, "skills"),
    playbooks: join(root, "playbooks"),
    config: join(root, "config"),
  };
}
