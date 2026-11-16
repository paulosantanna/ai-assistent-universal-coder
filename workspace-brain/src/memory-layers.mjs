/**
 * Modelo em camadas (inspirado em consolidação tipo “dreaming” / memória de agente):
 * L1 transcripts → L2 notes → L3 wiki → L4 session bootstrap (≤200 linhas).
 */
import { readFileSync, writeFileSync, existsSync, readdirSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { paths, getBrainRoot } from "./paths.mjs";

export const SESSION_INDEX_MAX_LINES = 200;

export function memoryPaths(root = getBrainRoot()) {
  const p = paths(root);
  return {
    ...p,
    transcripts: join(root, "memory", "transcripts"),
    notes: join(root, "memory", "notes"),
    notesIndex: join(root, "memory", "notes", "INDEX.md"),
    wiki: join(root, "memory", "wiki"),
    wikiIndex: join(root, "memory", "wiki", "INDEX.md"),
    sessionBootstrap: join(root, "memory", "session", "BOOTSTRAP.md"),
    dreamLog: join(root, "memory", "dream", "last-run.json"),
    dreamDir: join(root, "memory", "dream"),
  };
}

export function ensureMemoryLayout(root = getBrainRoot()) {
  const m = memoryPaths(root);
  for (const dir of [m.transcripts, m.notes, m.wiki, join(root, "memory", "session"), m.dreamDir]) {
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  }
  if (!existsSync(m.notesIndex)) {
    writeFileSync(
      m.notesIndex,
      `# Notes index\n\n> Previsões curadas (regra + evidência + armadilhas). Detalhe em ficheiros nesta pasta.\n\n`,
      "utf8",
    );
  }
  if (!existsSync(m.wikiIndex)) {
    writeFileSync(
      m.wikiIndex,
      `# Wiki\n\n> Mapa ligado; não duplicar corpus inteiro. Ver [[../corpus]] via brain_search.\n\n`,
      "utf8",
    );
  }
  return m;
}

export function appendTranscript(entry, root = getBrainRoot()) {
  const m = ensureMemoryLayout(root);
  const day = new Date().toISOString().slice(0, 10);
  const file = join(m.transcripts, `${day}.ndjson`);
  const line = JSON.stringify({ ts: new Date().toISOString(), ...entry }) + "\n";
  writeFileSync(file, (existsSync(file) ? readFileSync(file, "utf8") : "") + line, "utf8");
  return file;
}

export function listNotes(root = getBrainRoot()) {
  const m = memoryPaths(root);
  if (!existsSync(m.notes)) return [];
  return readdirSync(m.notes)
    .filter((f) => f.endsWith(".md") && f !== "INDEX.md")
    .map((f) => join(m.notes, f));
}

/** Gera BOOTSTRAP.md: só o que entra em toda sessão (cap de linhas). */
export function rebuildSessionBootstrap(root = getBrainRoot()) {
  const m = ensureMemoryLayout(root);
  const lines = [
    "# Session bootstrap",
    "",
    "> Carregar automaticamente nas IAs. Máx. ~200 linhas; o resto fica em notes/wiki com links.",
    "",
    "## Propósito da memória",
    "Prever o que sessões futuras vão precisar (regras testadas, armadilhas), não espelhar estado observável do repo.",
    "",
  ];

  const index = existsSync(m.notesIndex) ? readFileSync(m.notesIndex, "utf8") : "";
  for (const row of index.split("\n").filter((l) => l.startsWith("- ["))) {
    lines.push(row);
    if (lines.length >= SESSION_INDEX_MAX_LINES - 20) break;
  }

  lines.push("", "## Wiki (entradas)", "");
  const wikiIdx = existsSync(m.wikiIndex) ? readFileSync(m.wikiIndex, "utf8") : "";
  for (const row of wikiIdx.split("\n").filter((l) => l.startsWith("- "))) {
    lines.push(row);
    if (lines.length >= SESSION_INDEX_MAX_LINES) break;
  }

  const body = lines.slice(0, SESSION_INDEX_MAX_LINES).join("\n") + "\n";
  writeFileSync(m.sessionBootstrap, body, "utf8");
  return { path: m.sessionBootstrap, lines: body.split("\n").length };
}

export function readSessionBootstrap(root = getBrainRoot()) {
  const m = memoryPaths(root);
  if (!existsSync(m.sessionBootstrap)) {
    return rebuildSessionBootstrap(root).path ? readFileSync(m.sessionBootstrap, "utf8") : "";
  }
  return readFileSync(m.sessionBootstrap, "utf8");
}
