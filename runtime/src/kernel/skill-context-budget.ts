import { createHash } from "node:crypto";
import { existsSync, readFileSync, statSync } from "node:fs";
import { dirname, resolve, sep } from "node:path";

export interface SkillContextDocument {
  path: string;
  bytes: number;
  sha256: string;
  content: string;
  reason: string;
}

export interface SkillContextBudgetResult {
  skillPath: string;
  skillBytes: number;
  indexBytes: number;
  referenceBytesLoaded: number;
  candidateReferenceBytes: number;
  bytesAvoided: number;
  referencesSelected: number;
  referencesAvailable: number;
  documents: SkillContextDocument[];
}

interface IndexedReference {
  path: string;
  line: string;
  score: number;
  bytes: number;
}

const HIGH_RISK = new Set(["high", "critical"]);

function sha256(value: string): string {
  return createHash("sha256").update(value).digest("hex");
}

function bytes(value: string): number {
  return Buffer.byteLength(value, "utf8");
}

function terms(value: string): string[] {
  return [...new Set(value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .split(/[^a-z0-9_.+-]+/)
    .filter((term) => term.length >= 3))];
}

function score(line: string, requestTerms: string[]): number {
  const normalized = line.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  return requestTerms.reduce((total, term) => total + (normalized.includes(term) ? Math.max(1, term.length) : 0), 0);
}

function safeChild(base: string, relativePath: string): string | null {
  const target = resolve(base, relativePath);
  const root = resolve(base) + sep;
  return target.startsWith(root) ? target : null;
}

export class SkillContextBudgetLoader {
  private readonly workspaceRoot: string;

  constructor(workspaceRoot: string) {
    this.workspaceRoot = resolve(workspaceRoot);
  }

  load(skillPath: string, request: string, riskLevel = "medium"): SkillContextBudgetResult {
    const absoluteSkill = resolve(this.workspaceRoot, skillPath);
    if (!existsSync(absoluteSkill)) throw new Error(`Skill file not found: ${skillPath}`);

    const skillContent = readFileSync(absoluteSkill, "utf8");
    const skillBytes = bytes(skillContent);
    const documents: SkillContextDocument[] = [{
      path: skillPath.replaceAll("\\", "/"),
      bytes: skillBytes,
      sha256: sha256(skillContent),
      content: skillContent,
      reason: "skill-contract"
    }];

    const referenceDir = resolve(dirname(absoluteSkill), "references");
    const indexPath = resolve(referenceDir, "INDEX.md");
    if (!existsSync(indexPath)) {
      return {
        skillPath,
        skillBytes,
        indexBytes: 0,
        referenceBytesLoaded: 0,
        candidateReferenceBytes: 0,
        bytesAvoided: 0,
        referencesSelected: 0,
        referencesAvailable: 0,
        documents
      };
    }

    const indexContent = readFileSync(indexPath, "utf8");
    const indexBytes = bytes(indexContent);
    documents.push({
      path: this.relative(indexPath),
      bytes: indexBytes,
      sha256: sha256(indexContent),
      content: indexContent,
      reason: "reference-index"
    });

    const requestTerms = terms(request);
    const candidates: IndexedReference[] = [];
    const linkPattern = /\[[^\]]+\]\(([^)]+\.md)\)/g;
    for (const line of indexContent.split(/\r?\n/)) {
      for (const match of line.matchAll(linkPattern)) {
        const relativeReference = match[1].trim();
        if (relativeReference === "INDEX.md") continue;
        const absoluteReference = safeChild(referenceDir, relativeReference);
        if (!absoluteReference || !existsSync(absoluteReference) || !statSync(absoluteReference).isFile()) continue;
        candidates.push({
          path: absoluteReference,
          line,
          score: score(line, requestTerms),
          bytes: statSync(absoluteReference).size
        });
      }
    }

    const uniqueCandidates = [...new Map(candidates.map((candidate) => [candidate.path, candidate])).values()];
    uniqueCandidates.sort((left, right) => right.score - left.score || left.bytes - right.bytes || left.path.localeCompare(right.path));

    const maxReferences = HIGH_RISK.has(riskLevel.toLowerCase()) ? 5 : 3;
    const scored = uniqueCandidates.filter((candidate) => candidate.score > 0);
    const selected = (scored.length > 0 ? scored : uniqueCandidates).slice(0, maxReferences);
    const seenHashes = new Set<string>();
    let referenceBytesLoaded = 0;

    for (const candidate of selected) {
      const content = readFileSync(candidate.path, "utf8");
      const digest = sha256(content);
      if (seenHashes.has(digest)) continue;
      seenHashes.add(digest);
      const size = bytes(content);
      referenceBytesLoaded += size;
      documents.push({
        path: this.relative(candidate.path),
        bytes: size,
        sha256: digest,
        content,
        reason: candidate.score > 0 ? `matched:${candidate.score}` : "fallback-smallest-reference"
      });
    }

    const candidateReferenceBytes = uniqueCandidates.reduce((total, candidate) => total + candidate.bytes, 0);
    return {
      skillPath,
      skillBytes,
      indexBytes,
      referenceBytesLoaded,
      candidateReferenceBytes,
      bytesAvoided: Math.max(0, candidateReferenceBytes - referenceBytesLoaded),
      referencesSelected: documents.length - 2,
      referencesAvailable: uniqueCandidates.length,
      documents
    };
  }

  private relative(path: string): string {
    const normalizedRoot = this.workspaceRoot.endsWith(sep) ? this.workspaceRoot : `${this.workspaceRoot}${sep}`;
    return path.startsWith(normalizedRoot)
      ? path.slice(normalizedRoot.length).replaceAll("\\", "/")
      : path.replaceAll("\\", "/");
  }
}
