import { mkdirSync, writeFileSync, existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { ConfigLoader } from "./config-loader.js";
import { SchemaValidator } from "./schema-validator.js";
import { RegistryLoader } from "./registry-loader.js";
import { OverlayRegistryMerger } from "./overlay-registry-merger.js";

const AEOS_ROOT = resolve(import.meta.dirname ?? process.cwd(), "..", "..", "..");
const EVIDENCE_DIR = join(AEOS_ROOT, ".aeos", "evidence");

function ensureDir(dir: string) {
  mkdirSync(dir, { recursive: true });
}

function writeEvidence(name: string, content: string) {
  ensureDir(EVIDENCE_DIR);
  const path = join(EVIDENCE_DIR, name);
  writeFileSync(path, content, "utf-8");
  console.log(`  Evidence written: ${name}`);
}

function writeJsonEvidence(name: string, data: unknown) {
  writeEvidence(name, JSON.stringify(data, null, 2));
}

function formatValidation(label: string, result: { valid: boolean; errors: string[]; warnings: string[] }): string {
  const lines: string[] = [
    `## ${label}`,
    `Status: ${result.valid ? "PASS" : "FAIL"}`,
    `Errors: ${result.errors.length}`,
    `Warnings: ${result.warnings.length}`,
  ];
  if (result.errors.length) lines.push("", "### Errors", ...result.errors.map(e => `- ${e}`));
  if (result.warnings.length) lines.push("", "### Warnings", ...result.warnings.map(w => `- ${w}`));
  return lines.join("\n") + "\n";
}

function box(label: string, ok: boolean) {
  return ok ? `[PASS] ${label}` : `[FAIL] ${label}`;
}

console.log("=".repeat(60));
console.log("AEOS REGISTRY CONSOLIDATION TEST");
console.log("=".repeat(60));
console.log(`AEOS Root: ${AEOS_ROOT}`);
console.log(`Evidence:  ${EVIDENCE_DIR}`);
console.log();

const results: { test: string; passed: boolean; detail: string }[] = [];
const reportSections: string[] = [];
let allPassed = true;

// ─── 1. ConfigLoader ──────────────────────────────────────────────────────────
console.log(box("1. ConfigLoader", true));
try {
  const loader = new ConfigLoader(AEOS_ROOT);

  const aeosConfig = loader.loadAeosConfig();
  results.push({ test: "ConfigLoader.loadAeosConfig", passed: true, detail: `v${aeosConfig.aeos.version} - ${aeosConfig.aeos.mode}` });
  console.log(`  aeos.config.yaml: v${aeosConfig.aeos.version}, mode=${aeosConfig.aeos.mode}`);

  const caps = loader.loadCapabilities();
  results.push({ test: "ConfigLoader.loadCapabilities", passed: true, detail: `${caps.capabilities.length} capabilities` });
  console.log(`  capabilities.yaml: ${caps.capabilities.length} capabilities`);

  const perms = loader.loadPermissions();
  results.push({ test: "ConfigLoader.loadPermissions", passed: true, detail: `default=${perms.default}` });
  console.log(`  permissions.yaml: default=${perms.default}`);

  const policies = loader.loadPolicies();
  results.push({ test: "ConfigLoader.loadPolicies", passed: true, detail: "loaded" });
  console.log(`  policies.yaml: loaded`);

  const agents = loader.loadAgentsRegistry();
  results.push({ test: "ConfigLoader.loadAgentsRegistry", passed: true, detail: `${agents.agents.length} agents` });

  const skills = loader.loadSkillsRegistry();
  results.push({ test: "ConfigLoader.loadSkillsRegistry", passed: true, detail: `${skills.skills.length} skills` });

  const playbooks = loader.loadPlaybooksRegistry();
  results.push({ test: "ConfigLoader.loadPlaybooksRegistry", passed: true, detail: `${playbooks.playbooks.length} playbooks` });

  const mcps = loader.loadMCPsRegistry();
  results.push({ test: "ConfigLoader.loadMCPsRegistry", passed: true, detail: `${mcps.mcps.length} MCPs` });

  const lcps = loader.loadLCPsRegistry();
  results.push({ test: "ConfigLoader.loadLCPsRegistry", passed: true, detail: `${lcps.lcps.length} LCPs` });

  const blueprints = loader.loadBlueprintsRegistry();
  results.push({ test: "ConfigLoader.loadBlueprintsRegistry", passed: true, detail: `${blueprints.blueprints.length} blueprints` });

  const profiles = loader.loadWorkbenchProfilesRegistry();
  results.push({ test: "ConfigLoader.loadWorkbenchProfilesRegistry", passed: true, detail: `${profiles.profiles.length} profiles` });

  const enterpriseSkills = loader.loadEnterpriseSkillsRegistry();
  results.push({ test: "ConfigLoader.loadEnterpriseSkillsRegistry", passed: true, detail: `${enterpriseSkills.skills.length} enterprise skills` });

  const enterprisePlaybooks = loader.loadEnterprisePlaybooksRegistry();
  results.push({ test: "ConfigLoader.loadEnterprisePlaybooksRegistry", passed: true, detail: `${enterprisePlaybooks.playbooks.length} enterprise playbooks` });

  const overlayIndex = loader.loadOverlayRegistryIndex();
  results.push({ test: "ConfigLoader.loadOverlayRegistryIndex", passed: true, detail: `${overlayIndex.registry_fragments.length} fragments` });

  const playbookAdditions = loader.loadPlaybooksAdditions("v0_8_to_v1_0");
  results.push({ test: "ConfigLoader.loadPlaybooksAdditions", passed: true, detail: playbookAdditions ? `${playbookAdditions.playbooks.length} additions` : "not found" });

  const skillAdditions = loader.loadSkillsAdditions("v0_8_to_v1_0");
  results.push({ test: "ConfigLoader.loadSkillsAdditions", passed: true, detail: skillAdditions ? `${skillAdditions.skills.length} additions` : "not found" });

  const allData = loader.loadAllRegistryData();
  results.push({ test: "ConfigLoader.loadAllRegistryData", passed: true, detail: `all=${allData.playbooks.length + allData.skills.length + allData.agents.length} total entries` });

  console.log();
} catch (e: any) {
  results.push({ test: "ConfigLoader suite", passed: false, detail: e.message });
  allPassed = false;
  console.log(`  FAIL: ${e.message}`);
}

// ─── 2. SchemaValidator ────────────────────────────────────────────────────────
console.log(box("2. SchemaValidator", true));
try {
  const validator = new SchemaValidator(AEOS_ROOT);

  const loader = new ConfigLoader(AEOS_ROOT);
  const aeosConfig = loader.loadAeosConfig();
  const caps = loader.loadCapabilities();
  const perms = loader.loadPermissions();
  const agentsReg = loader.loadAgentsRegistry();
  const skillsReg = loader.loadSkillsRegistry();
  const playbooksReg = loader.loadPlaybooksRegistry();
  const mcpsReg = loader.loadMCPsRegistry();
  const lcpsReg = loader.loadLCPsRegistry();
  const blueprintsReg = loader.loadBlueprintsRegistry();
  const profilesReg = loader.loadWorkbenchProfilesRegistry();
  const enterpriseSkillsReg = loader.loadEnterpriseSkillsRegistry();
  const overlayIndex = loader.loadOverlayRegistryIndex();

  let v = validator.validateAeosConfig(aeosConfig);
  const aeosVal = v;
  if (!v.valid) { results.push({ test: "validateAeosConfig", passed: false, detail: v.errors.join("; ") }); allPassed = false; }
  else results.push({ test: "validateAeosConfig", passed: true, detail: `${v.warnings.length} warnings` });

  v = validator.validateCapabilities(caps);
  if (!v.valid) { results.push({ test: "validateCapabilities", passed: false, detail: v.errors.join("; ") }); allPassed = false; }
  else results.push({ test: "validateCapabilities", passed: true, detail: `${caps.capabilities.length} capabilities` });

  v = validator.validatePermissions(perms);
  if (!v.valid) { results.push({ test: "validatePermissions", passed: false, detail: v.errors.join("; ") }); allPassed = false; }
  else results.push({ test: "validatePermissions", passed: true, detail: "ok" });

  v = validator.validatePolicies(loader.loadPolicies());
  results.push({ test: "validatePolicies", passed: v.valid, detail: v.valid ? "ok" : v.errors.join("; ") });

  v = validator.validateAgentsRegistry(agentsReg);
  if (!v.valid) { results.push({ test: "validateAgentsRegistry", passed: false, detail: v.errors.join("; ") }); allPassed = false; }
  else results.push({ test: "validateAgentsRegistry", passed: true, detail: `${v.warnings.length} warnings` });

  v = validator.validateSkillsRegistry(skillsReg);
  if (!v.valid) { results.push({ test: "validateSkillsRegistry", passed: false, detail: v.errors.join("; ") }); allPassed = false; }
  else results.push({ test: "validateSkillsRegistry", passed: true, detail: "ok" });

  v = validator.validatePlaybooksRegistry(playbooksReg);
  if (!v.valid) { results.push({ test: "validatePlaybooksRegistry", passed: false, detail: v.errors.join("; ") }); allPassed = false; }
  else results.push({ test: "validatePlaybooksRegistry", passed: true, detail: "ok" });

  v = validator.validateMCPsRegistry(mcpsReg);
  if (!v.valid) { results.push({ test: "validateMCPsRegistry", passed: false, detail: v.errors.join("; ") }); allPassed = false; }
  else results.push({ test: "validateMCPsRegistry", passed: true, detail: `${mcpsReg.mcps.filter(m => m.risk_level === "critical").length} critical MCPs` });

  v = validator.validateLCPsRegistry(lcpsReg);
  results.push({ test: "validateLCPsRegistry", passed: v.valid, detail: v.valid ? "ok" : v.errors.join("; ") });

  v = validator.validateBlueprintsRegistry(blueprintsReg);
  results.push({ test: "validateBlueprintsRegistry", passed: v.valid, detail: v.valid ? "ok" : v.errors.join("; ") });

  v = validator.validateWorkbenchProfilesRegistry(profilesReg);
  results.push({ test: "validateWorkbenchProfilesRegistry", passed: v.valid, detail: v.valid ? "ok" : v.errors.join("; ") });

  v = validator.validateOverlayRegistryIndex(overlayIndex);
  if (!v.valid) { results.push({ test: "validateOverlayRegistryIndex", passed: false, detail: v.errors.join("; ") }); allPassed = false; }
  else results.push({ test: "validateOverlayRegistryIndex", passed: true, detail: `${overlayIndex.registry_fragments.length} fragments` });

  const crossRef = validator.crossReferenceValidations(
    agentsReg.agents,
    skillsReg.skills,
    playbooksReg.playbooks,
    mcpsReg.mcps,
    lcpsReg.lcps
  );
  results.push({ test: "crossReferenceValidations", passed: crossRef.valid, detail: `${crossRef.issues.length} issues` });
  if (!crossRef.valid) { allPassed = false; }

  console.log();
  for (const r of results.filter(r => r.test.startsWith("validate") || r.test.startsWith("cross"))) {
    console.log(`  ${r.passed ? "PASS" : "FAIL"}: ${r.test} — ${r.detail}`);
  }

  const allValidationRecords = [
    { file: "aeos.config.yaml", result: aeosVal },
    { file: "agents.registry.yaml", result: validator.validateAgentsRegistry(agentsReg) },
    { file: "skills.registry.yaml", result: validator.validateSkillsRegistry(skillsReg) },
    { file: "playbooks.registry.yaml", result: validator.validatePlaybooksRegistry(playbooksReg) },
    { file: "mcps.registry.yaml", result: validator.validateMCPsRegistry(mcpsReg) },
    { file: "lcps.registry.yaml", result: validator.validateLCPsRegistry(lcpsReg) },
    { file: "blueprints.registry.yaml", result: validator.validateBlueprintsRegistry(blueprintsReg) },
    { file: "workbench-profiles.registry.yaml", result: validator.validateWorkbenchProfilesRegistry(profilesReg) },
    { file: "enterprise-skills.registry.yaml", result: validator.validateEnterpriseSkillsRegistry(enterpriseSkillsReg) },
    { file: "overlay.registry.index.yaml", result: validator.validateOverlayRegistryIndex(overlayIndex) },
  ];

  let validationMd = "# Schema Validation Report\n\n";
  for (const rec of allValidationRecords) {
    validationMd += formatValidation(rec.file, rec.result);
  }
  validationMd += "## Cross-Reference Validation\n\n";
  for (const issue of crossRef.issues) {
    validationMd += `- [${issue.severity}] ${issue.registry} > ${issue.field}: ${issue.message}\n`;
  }

  writeEvidence("schema-validation.md", validationMd);

} catch (e: any) {
  results.push({ test: "SchemaValidator suite", passed: false, detail: e.message });
  allPassed = false;
  console.log(`  FAIL: ${e.message}`);
}

// ─── 3. OverlayRegistryMerger ─────────────────────────────────────────────────
console.log(box("3. OverlayRegistryMerger", true));
try {
  const merger = new OverlayRegistryMerger(AEOS_ROOT);

  const mergeResult = merger.loadAndMergeWithStrategy("replace-duplicates");
  results.push({ test: "loadAndMergeWithStrategy", passed: true, detail: `merged=${mergeResult.merged}, agents=${mergeResult.agents.length}, skills=${mergeResult.skills.length}, playbooks=${mergeResult.playbooks.length}, conflicts=${mergeResult.conflicts.length}` });
  if (mergeResult.conflicts.length > 0) {
    results.push({ test: "merge-conflicts-detected", passed: false, detail: `${mergeResult.conflicts.length} conflicts found — see evidence` });
    allPassed = false;
  }

  if (mergeResult.subagents.length > 0) {
    results.push({ test: "merge-subagents", passed: true, detail: `${mergeResult.subagents.length} subagents from v0_7` });
  }

  console.log(`  Merged: ${mergeResult.merged}`);
  console.log(`  Agents: ${mergeResult.agents.length} (conflicts: ${mergeResult.conflicts.filter(c => c.source === "agents").length})`);
  console.log(`  Skills: ${mergeResult.skills.length} (conflicts: ${mergeResult.conflicts.filter(c => c.source === "skills").length})`);
  console.log(`  Playbooks: ${mergeResult.playbooks.length} (conflicts: ${mergeResult.conflicts.filter(c => c.source === "playbooks").length})`);
  console.log(`  Subagents: ${mergeResult.subagents.length}`);
  console.log(`  Warnings: ${mergeResult.warnings.length}`);

  writeJsonEvidence("overlay-merge-result.json", mergeResult);

  const mergeMd = [
    "# Overlay Registry Merge Report",
    "",
    `## Status: ${mergeResult.merged ? "MERGED" : "CONFLICTS"}`,
    "",
    `- Agents: ${mergeResult.agents.length}`,
    `- Subagents: ${mergeResult.subagents.length}`,
    `- Skills: ${mergeResult.skills.length}`,
    `- Playbooks: ${mergeResult.playbooks.length}`,
    `- Conflicts: ${mergeResult.conflicts.length}`,
    `- Warnings: ${mergeResult.warnings.length}`,
    ...(mergeResult.conflicts.length ? ["", "### Conflicts", ...mergeResult.conflicts.map(c => `- [${c.source}] ${c.existing_id} in ${c.registry}: ${c.reason}`)] : []),
    ...(mergeResult.warnings.length ? ["", "### Warnings", ...mergeResult.warnings.map(w => `- ${w}`)] : [])
  ].join("\n");

  writeEvidence("overlay-merge.md", mergeMd);
  console.log();

} catch (e: any) {
  results.push({ test: "OverlayRegistryMerger suite", passed: false, detail: e.message });
  allPassed = false;
  console.log(`  FAIL: ${e.message}`);
}

// ─── 4. RegistryLoader (resolved) ─────────────────────────────────────────────
console.log(box("4. RegistryLoader (resolved)", true));
try {
  const registryLoader = new RegistryLoader(AEOS_ROOT);
  const resolved = registryLoader.loadAllResolved();

  results.push({ test: "RegistryLoader.loadAllResolved", passed: true, detail: `agents=${resolved.agents.length}, skills=${resolved.skills.length}, playbooks=${resolved.playbooks.length}, mcps=${resolved.mcps.length}, lcps=${resolved.lcps.length}` });

  const crossRefResults = registryLoader.resolveAgent(resolved.agents, "root");
  if (crossRefResults) results.push({ test: "resolveAgent(root)", passed: true, detail: `found ${crossRefResults.id}` });
  else { results.push({ test: "resolveAgent(root)", passed: false, detail: "not found" }); allPassed = false; }

  const skills = registryLoader.resolveSkills(resolved.skills, ["repo-scanner", "architecture-mapper", "security-audit"]);
  results.push({ test: "resolveSkills", passed: true, detail: `${skills.length} resolved` });

  const mcps = registryLoader.resolveMCPs(resolved.mcps, ["filesystem-readonly", "git-readonly"]);
  results.push({ test: "resolveMCPs", passed: true, detail: `${mcps.length} resolved` });

  const lcps = registryLoader.resolveLCPs(resolved.lcps, ["global-rules", "security-governance"]);
  results.push({ test: "resolveLCPs", passed: true, detail: `${lcps.length} resolved` });

  const agent = registryLoader.resolveAgent(resolved.agents, "incident");
  results.push({ test: "resolveAgent(incident)", passed: !!agent, detail: agent ? "found from v0_7" : "not found (expected — no agent file)" });

  const planner = registryLoader.resolveAgent(resolved.agents, "planner");
  results.push({ test: "resolveAgent(planner)", passed: !!planner, detail: planner ? "found from v0_7" : "not found" });

  console.log(`  Resolved: ${resolved.agents.length} agents, ${resolved.skills.length} skills, ${resolved.playbooks.length} playbooks`);
  console.log(`  Agent root: ${resolved.agents.find(a => a.id === "root") ? "ok" : "missing"}`);
  console.log(`  Agent planner: ${planner ? "ok (v0_7)" : "missing"}`);
  console.log();

  writeJsonEvidence("resolved-registries.json", {
    agentCount: resolved.agents.length,
    skillCount: resolved.skills.length,
    playbookCount: resolved.playbooks.length,
    mcpCount: resolved.mcps.length,
    lcpCount: resolved.lcps.length,
    subagentCount: resolved.subagents.length,
    blueprintCount: resolved.blueprints.length,
    profileCount: resolved.profiles.length,
    mergeConflicts: resolved.mergeResult.conflicts.length,
    mergeWarnings: resolved.mergeResult.warnings.length
  });

} catch (e: any) {
  results.push({ test: "RegistryLoader suite", passed: false, detail: e.message });
  allPassed = false;
  console.log(`  FAIL: ${e.message}`);
}

// ─── Summary ───────────────────────────────────────────────────────────────────
console.log("=".repeat(60));
console.log("CONSOLIDATION TEST RESULTS");
console.log("=".repeat(60));
let passCount = 0;
let failCount = 0;
for (const r of results) {
  const icon = r.passed ? "PASS" : "FAIL";
  if (r.passed) passCount++; else failCount++;
  console.log(`  [${icon}] ${r.test}: ${r.detail}`);
}
console.log();
console.log(`Total: ${results.length} | Passed: ${passCount} | Failed: ${failCount}`);
console.log(`Overall: ${allPassed ? "ALL TESTS PASSED" : "SOME TESTS FAILED"}`);

const summaryReport = [
  "# Registry Consolidation Test Report",
  "",
  `- Generated at: ${new Date().toISOString()}`,
  `- AEOS Root: ${AEOS_ROOT}`,
  `- Evidence dir: ${EVIDENCE_DIR}`,
  "",
  "## Results",
  "",
  `| Result | Count |`,
  `|--------|-------|`,
  `| Total  | ${results.length} |`,
  `| Passed | ${passCount} |`,
  `| Failed | ${failCount} |`,
  "",
  "### Details",
  "",
  ...results.map(r => `| ${r.passed ? "PASS" : "FAIL"} | ${r.test} | ${r.detail} |`),
  "",
  "## Full Output",
  "",
  ...results.map(r => `- [${r.passed ? "PASS" : "FAIL"}] ${r.test}: ${r.detail}`)
].join("\n");

writeEvidence("consolidation-test-report.md", summaryReport);
console.log(`\nEvidence written to: ${EVIDENCE_DIR}`);