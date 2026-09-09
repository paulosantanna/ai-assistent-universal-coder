import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";

const repoRoot = process.cwd();
const registryPath = path.join(repoRoot, "aeos", "registries", "skills.registry.yaml");
const source = fs.readFileSync(registryPath, "utf8");
const document = yaml.load(source);

if (!document || !Array.isArray(document.skills)) {
  throw new Error("skills.registry.yaml must contain a skills array");
}

let changed = 0;
for (const skill of document.skills) {
  if (!skill || typeof skill !== "object" || typeof skill.id !== "string") {
    throw new Error("invalid skill registry entry");
  }
  if (skill.owner_agent !== "codenavi-agent") {
    skill.owner_agent = "codenavi-agent";
    changed += 1;
  }
}

const rendered = yaml.dump(document, {
  noRefs: true,
  noCompatMode: true,
  lineWidth: -1,
  sortKeys: false,
  quotingType: "'",
  forceQuotes: false,
});

fs.writeFileSync(registryPath, rendered, "utf8");
process.stdout.write(`${JSON.stringify({ status: "PASS", registry: "aeos/registries/skills.registry.yaml", skills: document.skills.length, normalizedOwners: changed })}\n`);
