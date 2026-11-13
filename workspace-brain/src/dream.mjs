import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
import {
  ensureMemoryLayout,
  memoryPaths,
  rebuildSessionBootstrap,
  appendTranscript,
} from "./memory-layers.mjs";
import { wikiStats } from "./wiki.mjs";
import { listNotes } from "./memory-layers.mjs";
import { getDeepSeekApiKey } from "./config.mjs";
import { deepseekChat } from "./deepseek.mjs";

function readRecentEvents(eventsPath, maxLines = 80) {
  if (!existsSync(eventsPath)) return [];
  const lines = readFileSync(eventsPath, "utf8").trim().split("\n").filter(Boolean);
  return lines.slice(-maxLines).map((l) => {
    try {
      return JSON.parse(l);
    } catch {
      return null;
    }
  }).filter(Boolean);
}

function readRecentTranscriptLines(dir, maxLines = 60) {
  if (!existsSync(dir)) return [];
  const files = readdirSync(dir)
    .filter((f) => f.endsWith(".ndjson"))
    .sort()
    .reverse();
  const out = [];
  for (const f of files) {
    const lines = readFileSync(join(dir, f), "utf8").trim().split("\n").filter(Boolean);
    for (const l of lines.reverse()) {
      try {
        out.push(JSON.parse(l));
      } catch {
        /* skip */
      }
      if (out.length >= maxLines) return out.reverse();
    }
  }
  return out.reverse();
}

/** Consolidação offline: transcripts ↔ notas; bootstrap; alertas. Opcional LLM. */
export async function runDream({ useLlm = false } = {}) {
  const m = ensureMemoryLayout();
  const events = readRecentEvents(m.events);
  const transcripts = readRecentTranscriptLines(m.transcripts);
  const notes = listNotes();
  const wiki = wikiStats();

  const report = {
    ran_at: new Date().toISOString(),
    events_scanned: events.length,
    transcripts_scanned: transcripts.length,
    notes_count: notes.length,
    wiki,
    actions: [],
    llm: null,
  };

  if (wiki.bytes > 2_000_000) {
    report.actions.push({ type: "warn", message: "wiki oversized — resumir páginas ou apagar duplicatas do corpus" });
  }

  const pathsTouched = new Set(events.flatMap((e) => e.paths ?? []));
  if (pathsTouched.size > 0 && notes.length === 0) {
    report.actions.push({
      type: "hint",
      message: "há eventos sem notas preditivas; considere brain_note_upsert com regra+evidência",
    });
  }

  rebuildSessionBootstrap();
  report.actions.push({ type: "rebuild_bootstrap", path: m.sessionBootstrap });

  if (useLlm && getDeepSeekApiKey()) {
    const noteSnippets = notes
      .slice(0, 12)
      .map((p) => readFileSync(p, "utf8").slice(0, 800))
      .join("\n---\n");
    const evidence = JSON.stringify({ events: events.slice(-15), transcripts: transcripts.slice(-10) }, null, 0).slice(
      0,
      12_000,
    );
    const messages = [
      {
        role: "system",
        content:
          "Você consolida memória de agente (sonho/dream). Compare notas com evidência recente. " +
          "Liste contradições, notas obsoletas e 1-3 promoções wiki (título+resumo curto). " +
          "JSON: { contradictions: string[], obsolete_note_files: string[], wiki_candidates: {title, summary}[] }",
      },
      {
        role: "user",
        content: `NOTAS:\n${noteSnippets}\n\nEVIDÊNCIA:\n${evidence}`,
      },
    ];
    try {
      const llm = await deepseekChat(messages, { temperature: 0.1, max_tokens: 1200 });
      report.llm = { raw: llm.content.slice(0, 4000) };
      appendTranscript({ kind: "dream", model: llm.model, summary: llm.content.slice(0, 500) });
    } catch (err) {
      report.llm = { error: err instanceof Error ? err.message : String(err) };
    }
  }

  writeFileSync(m.dreamLog, JSON.stringify(report, null, 2) + "\n", "utf8");
  return report;
}
