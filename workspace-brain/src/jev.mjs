import { getTypesafeApiKey } from "./config.mjs";

const DOC_HOSTS = /\.(gov|edu)(\.|$)/i;
const CODE_HOSTS = /github\.com|gitlab\.com|bitbucket\.org|docs\./i;

/** Heurística determinística quando Jev/TypeSafe não está configurado. */
function heuristicUrlGate(url, title = "") {
  let score = 0;
  const u = url.toLowerCase();
  if (CODE_HOSTS.test(u)) score += 2;
  if (DOC_HOSTS.test(u)) score += 1;
  if (/\.(pdf|zip|exe|dmg)$/i.test(u)) score -= 3;
  if (title && title.length > 3) score += 0.5;
  const include = score >= 1;
  return {
    include,
    confidence: include ? Math.min(0.95, 0.5 + score * 0.15) : Math.max(0.1, 0.4 + score * 0.1),
    choice: include ? "include" : "skip",
    mode: "heuristic",
    reason: include ? "host/conteúdo alinhado a código ou documentação" : "baixa prioridade ou tipo de ficheiro arriscado",
  };
}

/** Julgamento Jev (TypeSafe) ou fallback heurístico. */
export async function assessUrlForIngest(url, context = {}) {
  const key = getTypesafeApiKey();
  if (!key) return heuristicUrlGate(url, context.title);

  try {
    const { TypeSafeClient, choice } = await import("@typesafe-ai/sdk");
    const client = new TypeSafeClient({ apiKey: key });
    const response = await client.systemOne({
      state: {
        url,
        title: context.title ?? "",
        snippet: (context.snippet ?? "").slice(0, 1500),
        purpose: "workspace-brain corpus ingest",
      },
      questions: {
        ingest: choice("Should this URL be ingested into the workspace brain corpus?", {
          include: null,
          skip: null,
          review_later: null,
        }),
      },
    });
    const ans = response.answers?.ingest;
    const picked = ans?.choice ?? "skip";
    return {
      include: picked === "include",
      choice: picked,
      confidence: ans?.confidence ?? 0.5,
      mode: "jev",
      reason: `TypeSafe choice: ${picked}`,
    };
  } catch (err) {
    const fallback = heuristicUrlGate(url, context.title);
    fallback.mode = "heuristic_after_jev_error";
    fallback.jev_error = err instanceof Error ? err.message : String(err);
    return fallback;
  }
}
