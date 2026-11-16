import { writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join } from "node:path";
import { paths, ensureLayout } from "./paths.mjs";
import { packageRoot } from "./config.mjs";

function mcpEntry() {
  const root = packageRoot();
  const brainRoot = paths().root;
  const cmd = process.platform === "win32" ? "node" : "node";
  const server = join(root, "src", "mcp-server.mjs").replace(/\\/g, "/");
  return {
    command: cmd,
    args: [server],
    env: {
      WORKSPACE_BRAIN_ROOT: brainRoot,
    },
  };
}

const SNIPPETS = {
  "mcp.cursor.json": {
    mcpServers: {
      "workspace-brain": mcpEntry(),
    },
  },
  "mcp.claude_desktop.json": {
    mcpServers: {
      "workspace-brain": mcpEntry(),
    },
  },
  "mcp.opencode.json": {
    servers: {
      workspace_brain: {
        ...mcpEntry(),
        description: "CodENavi workspace brain — RAG DeepSeek + corpus em disco",
      },
    },
  },
  "mcp.codex.json": {
    mcp_servers: {
      workspace_brain: mcpEntry(),
    },
  },
};

export function installAgentSnippets() {
  ensureLayout();
  const { config } = paths();
  if (!existsSync(config)) mkdirSync(config, { recursive: true });
  const written = [];
  for (const [name, body] of Object.entries(SNIPPETS)) {
    const target = join(config, name);
    writeFileSync(target, JSON.stringify(body, null, 2) + "\n", "utf8");
    written.push(target);
  }
  return {
    written,
    instructions: [
      "Cursor: mescle config/mcp.cursor.json em .cursor/mcp.json (ou Settings → MCP).",
      "Claude Desktop: mescle config/mcp.claude_desktop.json no ficheiro de config do Claude.",
      "OpenCode: use config/mcp.opencode.json conforme documentação do OpenCode.",
      "Codex / outros: use o snippet equivalente em config/.",
      `Servidor: node ${join(packageRoot(), "src", "mcp-server.mjs")}`,
      `WORKSPACE_BRAIN_ROOT=${paths().root}`,
    ],
  };
}
