import { writeFileSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { paths, getBrainRoot } from "./paths.mjs";
import { corpusStats } from "./corpus.mjs";
import { getModelContract } from "./config.mjs";

export function writeIngestManifest({ source, counts, notes } = {}) {
  const root = getBrainRoot();
  const p = paths(root);
  const contract = getModelContract(root);
  const manifest = {
    schema_version: 1,
    dataset_id: `wb-${new Date().toISOString().replace(/[:.]/g, "-")}`,
    created_at: new Date().toISOString(),
    model_contract: contract,
    stats: { ...corpusStats(), ...counts },
    source: source ?? null,
    notes: notes ?? [],
  };
  const latest = join(p.manifests, "manifest-latest.json");
  writeFileSync(latest, JSON.stringify(manifest, null, 2) + "\n", "utf8");
  writeFileSync(join(p.manifests, `${manifest.dataset_id}.json`), JSON.stringify(manifest, null, 2) + "\n", "utf8");
  return manifest;
}

export function readLatestManifest() {
  const latest = join(paths().manifests, "manifest-latest.json");
  if (!existsSync(latest)) return null;
  return JSON.parse(readFileSync(latest, "utf8"));
}
