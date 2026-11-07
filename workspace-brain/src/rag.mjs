import { searchCorpus } from "./corpus.mjs";
import { deepseekChat } from "./deepseek.mjs";
import { loadOpenCodeHints } from "./opencode.mjs";

export async function brainAsk(question, { topK = 6 } = {}) {
  const hits = searchCorpus(question, { topK });
  const opencode = loadOpenCodeHints();
  const contextBlocks = hits.map(
    (h, i) =>
      `[${i + 1}] source=${h.source} path=${h.sourcePath ?? h.url ?? "?"} sha256=${h.sha256}\n${h.text}`,
  );
  const system = [
    "Você responde usando apenas o CONTEXTO fornecido do workspace brain.",
    "Cite trechos como [n]. Se o contexto for insuficiente, diga explicitamente.",
    "Não invente caminhos nem APIs.",
    opencode.path ? `OpenCode config detectado: ${opencode.path}` : "",
  ]
    .filter(Boolean)
    .join("\n");

  const messages = [
    { role: "system", content: system },
    {
      role: "user",
      content: `CONTEXTO:\n${contextBlocks.join("\n\n---\n\n") || "(vazio)"}\n\nPERGUNTA:\n${question}`,
    },
  ];

  const llm = await deepseekChat(messages);
  return {
    answer: llm.content,
    model: llm.model,
    citations: hits.map((h, i) => ({
      ref: i + 1,
      id: h.id,
      source: h.source,
      sourcePath: h.sourcePath,
      url: h.url,
      score: h.score,
    })),
    usage: llm.usage,
  };
}
