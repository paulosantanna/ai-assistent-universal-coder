// Tool catalogue shared by the AWS and Azure servers. Every tool is read-only: no cloud credentials,
// no remote writes, no deployment. Tool results are JSON objects (structuredContent).
import { estimateMonthlyCost, getPattern, listPatterns, listPitfalls, mapLocalApi, reviewArchitecture } from "./engine.mjs";

const READ_ONLY = { readOnlyHint: true, openWorldHint: false };

export function createTools(kb, provider) {
  const label = provider.toUpperCase();
  const tools = [
    {
      name: "list_patterns",
      description: `Lista padroes de arquitetura ${label} verificados (id, titulo, categoria, quando usar).`,
      inputSchema: { type: "object", properties: { category: { type: "string" } }, additionalProperties: false },
      annotations: READ_ONLY,
    },
    {
      name: "get_pattern",
      description: `Detalha um padrao ${label}: componentes, alavancas de custo e claims com URL de origem e rotulo final.`,
      inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"], additionalProperties: false },
      annotations: READ_ONLY,
    },
    {
      name: "list_pitfalls",
      description: `Lista erros conhecidos de ${label} (armadilhas): premissa errada, fato correto, regra que detecta e claims rejeitados.`,
      inputSchema: { type: "object", properties: {}, additionalProperties: false },
      annotations: READ_ONLY,
    },
    {
      name: "review_architecture",
      description: `Revisa um modelo de arquitetura ${label} (JSON, provider=${provider}) com regras deterministicas; devolve achados com severidade e fontes.`,
      inputSchema: { type: "object", properties: { model: { type: "object" } }, required: ["model"], additionalProperties: true },
      annotations: READ_ONLY,
    },
    {
      name: "map_local_api",
      description: `Mapeia uma API ou componente local para servicos ${label}, com restricoes, proibicoes e fontes. Tipos desconhecidos falham.`,
      inputSchema: { type: "object", properties: { api: { type: "object" } }, required: ["api"], additionalProperties: true },
      annotations: READ_ONLY,
    },
    {
      name: "estimate_monthly_cost",
      description: `Estima custo mensal ${label} a partir do snapshot versionado de precos. SKU desconhecido falha: nenhum preco e inventado.`,
      inputSchema: {
        type: "object",
        properties: {
          items: {
            type: "array",
            items: {
              type: "object",
              properties: {
                sku: { type: "string" },
                units_per_month: { type: "number" },
                factor: { type: "number" },
                note: { type: "string" },
              },
              required: ["sku", "units_per_month"],
              additionalProperties: false,
            },
          },
        },
        required: ["items"],
        additionalProperties: false,
      },
      annotations: READ_ONLY,
    },
  ];

  const handlers = {
    list_patterns: (args) => ({ provider, patterns: listPatterns(kb, provider, args) }),
    get_pattern: (args) => getPattern(kb, provider, args.id),
    list_pitfalls: () => ({ provider, pitfalls: listPitfalls(kb, provider) }),
    review_architecture: (args) => {
      if (args.model?.provider !== provider) {
        throw new Error(`Model provider "${args.model?.provider}" does not match this server (${provider}).`);
      }
      return reviewArchitecture(kb, args.model);
    },
    map_local_api: (args) => mapLocalApi(args.api, provider),
    estimate_monthly_cost: (args) => {
      for (const item of args.items ?? []) {
        if (!String(item.sku).startsWith(`${provider}.`)) {
          throw new Error(`SKU ${item.sku} does not belong to ${provider}.`);
        }
      }
      return estimateMonthlyCost(kb.prices[provider], args.items ?? []);
    },
  };

  return { tools, handlers };
}
