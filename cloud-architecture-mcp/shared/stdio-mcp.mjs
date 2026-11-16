// MCP server over stdio: newline-delimited JSON-RPC 2.0, with no SDK dependency.
// Same convention as the other governed Node servers in this workspace (no silent new dependency).
import { createInterface } from "node:readline";

// Latest MCP revision this server implements; older clients are answered with this revision too.
export const PROTOCOL_VERSION = "2025-11-25";

export function createMcpServer({ name, version, tools, handlers }) {
  const known = new Map(tools.map((tool) => [tool.name, tool]));
  return {
    async handle(line) {
      let message;
      try {
        message = JSON.parse(line);
      } catch {
        return rpcError(null, -32700, "Parse error");
      }
      if (message === null || typeof message !== "object" || Array.isArray(message)) {
        return rpcError(null, -32600, "Invalid Request");
      }
      const { id, method, params = {} } = message;
      if (method === undefined) return null; // a response from the client; this server sends no requests
      const isNotification = id === undefined;
      try {
        switch (method) {
          case "initialize":
            return rpcResult(id, { protocolVersion: PROTOCOL_VERSION, capabilities: { tools: { listChanged: false } }, serverInfo: { name, version } });
          case "notifications/initialized":
            return null;
          case "ping":
            return rpcResult(id, {});
          case "tools/list":
            return rpcResult(id, { tools });
          case "tools/call": {
            const tool = known.get(params.name);
            if (!tool) return rpcError(id, -32602, `Unknown tool: ${params.name}`);
            try {
              const structured = await handlers[params.name](params.arguments ?? {});
              return rpcResult(id, { content: [{ type: "text", text: JSON.stringify(structured, null, 2) }], structuredContent: structured, isError: false });
            } catch (toolError) {
              // Tool failures are reported inside the result (MCP convention), never as a silent empty answer.
              return rpcResult(id, { content: [{ type: "text", text: toolError.message }], isError: true });
            }
          }
          default:
            return isNotification ? null : rpcError(id, -32601, `Method not found: ${method}`);
        }
      } catch (unexpected) {
        return isNotification ? null : rpcError(id, -32603, unexpected.message);
      }
    },
  };
}

export function serveStdio(server, { input = process.stdin, output = process.stdout } = {}) {
  const lines = createInterface({ input, crlfDelay: Infinity });
  lines.on("line", async (line) => {
    if (!line.trim()) return;
    const response = await server.handle(line);
    if (response) output.write(`${JSON.stringify(response)}\n`);
  });
  return lines;
}

function rpcResult(id, result) {
  return { jsonrpc: "2.0", id, result };
}

function rpcError(id, code, message) {
  return { jsonrpc: "2.0", id, error: { code, message } };
}
