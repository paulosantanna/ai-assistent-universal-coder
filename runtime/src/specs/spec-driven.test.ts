import assert from "node:assert/strict";
import { existsSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { addCriterion, addEvidence, addRequirement, approveSpec, initSpec, loadSpec, startImplementation, validateSpec, verifySpec } from "./spec-driven.js";

const project = (): string => mkdtempSync(join(tmpdir(), "aeos-spec-"));
const valid = (root: string, slug = "checkout"): void => {
  initSpec(root, slug, "Deliver checkout safely");
  addRequirement(root, slug, "Persist the order", "must");
  addCriterion(root, slug, ["REQ-001"], "Order is persisted once", "test");
};

test("creates the structured source of truth and generated artifacts", () => {
  const root = project(); initSpec(root, "checkout", "Deliver checkout safely");
  for (const name of ["spec.json", "SPECIFICATION.md", "IMPLEMENTATION_PLAN.md", "TRACEABILITY.json"]) assert.ok(existsSync(join(root, ".aeos-runtime/specs/checkout", name)));
});
test("blocks specifications with uncovered requirements", () => {
  const root = project(); initSpec(root, "checkout", "x"); addRequirement(root, "checkout", "One", "must");
  assert.equal(validateSpec(root, "checkout").valid, false);
});
test("approves and starts a valid specification", () => {
  const root = project(); valid(root); approveSpec(root, "checkout", "owner", "ticket-1");
  assert.equal(startImplementation(root, "checkout").status, "implementing");
});
test("normative mutation invalidates approval", () => {
  const root = project(); valid(root); approveSpec(root, "checkout", "owner", "ticket-1");
  const changed = addRequirement(root, "checkout", "Audit order", "should");
  assert.equal(changed.status, "draft"); assert.equal(changed.approval, undefined);
});
test("detects an external edit after approval", () => {
  const root = project(); valid(root); approveSpec(root, "checkout", "owner", "ticket-1");
  const path = join(root, ".aeos-runtime/specs/checkout/spec.json"); const spec = loadSpec(root, "checkout"); spec.objective = "tampered"; writeFileSync(path, JSON.stringify(spec), "utf8");
  assert.throws(() => startImplementation(root, "checkout"), /changed after approval/);
});
test("requires evidence for every acceptance criterion", () => {
  const root = project(); valid(root); approveSpec(root, "checkout", "owner", "ticket-1"); startImplementation(root, "checkout");
  assert.throws(() => verifySpec(root, "checkout"), /Missing passing evidence/);
  addEvidence(root, "checkout", "AC-001", true, "test-report.xml"); assert.equal(verifySpec(root, "checkout").status, "accepted");
});
test("failed evidence rejects the specification", () => {
  const root = project(); valid(root); approveSpec(root, "checkout", "owner", "ticket-1"); startImplementation(root, "checkout");
  assert.equal(addEvidence(root, "checkout", "AC-001", false, "failure.log").status, "rejected");
});
