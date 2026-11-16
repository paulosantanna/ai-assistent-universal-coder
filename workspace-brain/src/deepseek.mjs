import { getDeepSeekApiKey, getModelContract } from "./config.mjs";
import { getBrainRoot } from "./paths.mjs";

export async function deepseekChat(messages, { temperature = 0.2, max_tokens = 4096 } = {}) {
  const key = getDeepSeekApiKey();
  if (!key) {
    throw new Error(
      "DEEPSEEK_API_KEY ausente. Defina variável de ambiente ou ficheiro em JEV_CONFIG_DIR (ex.: deepseek.key).",
    );
  }
  const contract = getModelContract(getBrainRoot());
  const base = (contract.base_url || "https://api.deepseek.com").replace(/\/$/, "");
  const model = contract.chat_model || "deepseek-chat";

  const res = await fetch(`${base}/v1/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${key}`,
    },
    body: JSON.stringify({
      model,
      messages,
      temperature,
      max_tokens,
    }),
  });

  const body = await res.text();
  if (!res.ok) {
    throw new Error(`DeepSeek HTTP ${res.status}: ${body.slice(0, 500)}`);
  }
  const json = JSON.parse(body);
  const content = json.choices?.[0]?.message?.content;
  if (typeof content !== "string") throw new Error("Resposta DeepSeek sem conteúdo");
  return { content, model, usage: json.usage ?? null, raw_id: json.id ?? null };
}
