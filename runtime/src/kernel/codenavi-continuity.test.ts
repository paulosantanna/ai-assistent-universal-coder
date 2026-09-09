import { describe, expect, it } from "vitest";
import {
  CODENAVI_CONTINUITY_FILES,
  CODENAVI_CONTINUITY_SKILLS,
  continuitySkillFacts,
  validateContinuityText
} from "./codenavi-continuity.js";

describe("CodENavi continuity runtime", () => {
  it("exposes five continuity skills and four canonical artifacts", () => {
    expect(CODENAVI_CONTINUITY_SKILLS.size).toBe(5);
    expect(CODENAVI_CONTINUITY_FILES).toHaveLength(4);
  });

  it("rejects obvious raw secrets", () => {
    expect(validateContinuityText('password = "supersecretvalue"')).toContain("potential raw secret detected in continuity payload");
  });

  it("returns deterministic governed facts for every continuity skill", () => {
    for (const id of CODENAVI_CONTINUITY_SKILLS) {
      expect(continuitySkillFacts(id)).not.toHaveLength(0);
    }
  });
});
