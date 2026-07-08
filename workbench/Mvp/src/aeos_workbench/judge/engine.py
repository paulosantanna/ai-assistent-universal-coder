"""Judge Engine - evaluates evidence and decides PASS/BLOCKED/NEEDS_REWORK.

Scoring reaches 10.0 when:
- Evidence Completeness: all 6 required types present
- Test Coverage: test evidence present with details
- Security Validation: security scan evidence present and clean
- Rollback Readiness: rollback plan documented
- Diff Quality: diff evidence captured
- Code Quality: quality metrics analysis performed
"""

REQUIRED_EVIDENCE_TYPES = ["code", "command", "test", "config", "diff", "source"]

CATEGORIES = {
    "evidence_completeness": {"weight": 0.25, "description": "Evidencias suficientes para validar a tarefa"},
    "test_coverage": {"weight": 0.20, "description": "Testes implementados e executados"},
    "security_validation": {"weight": 0.20, "description": "Nenhum segredo, operacao segura"},
    "rollback_readiness": {"weight": 0.15, "description": "Plano de rollback documentado e viaoavel"},
    "diff_quality": {"weight": 0.10, "description": "Diff claro, mnimo e explicado"},
    "code_quality": {"weight": 0.10, "description": "Codigo segue padroes e boas praticas"},
}

MIN_SCORE_TO_PASS = 7.0
BLOCK_THRESHOLD = 5.0


class JudgeEngine:
    def __init__(self):
        self.implementer_id = None
        self.judge_id = "judge-aeos-001"
        self.quality_metrics = None

    def set_implementer(self, agent_id):
        self.implementer_id = agent_id

    def set_quality_metrics(self, metrics):
        self.quality_metrics = metrics

    def evaluate(self, evidence_list):
        if self.implementer_id == self.judge_id:
            return self._blocked("Judge cannot be the same agent as implementer")

        evidence_types = set(e.get("type") for e in evidence_list)
        missing_evidence = [t for t in REQUIRED_EVIDENCE_TYPES if t not in evidence_types]

        scores = {}
        deductions = 0.0
        failures = []
        blocking_conditions = []

        # --- 1. Evidence Completeness (target: 10.0) ---
        if not missing_evidence:
            scores["evidence_completeness"] = 10.0
        else:
            missing_ratio = len(missing_evidence) / len(REQUIRED_EVIDENCE_TYPES)
            scores["evidence_completeness"] = round(10.0 * (1.0 - missing_ratio), 1)
            failures.append("Missing evidence types: " + ", ".join(missing_evidence))
            if missing_ratio > 0.5:
                blocking_conditions.append("missing_evidence")

        # --- 2. Test Coverage (target: 10.0) ---
        test_entries = [e for e in evidence_list if e.get("type") == "test"]
        if test_entries:
            has_details = any("details" in e or "count" in str(e) for e in test_entries)
            has_positive = any(
                "test" in e.get("claim", "").lower()
                and "no test" not in e.get("claim", "").lower()
                for e in test_entries
            )
            if has_positive:
                test_count = 0
                test_frameworks = []
                for e in test_entries:
                    det = e.get("details", {})
                    if isinstance(det, dict):
                        test_count = max(test_count, det.get("count", 0))
                        fws = det.get("frameworks", [])
                        if fws:
                            test_frameworks = fws
                if test_frameworks and test_count >= 1:
                    scores["test_coverage"] = 10.0
                elif test_count >= 2:
                    scores["test_coverage"] = 10.0
                elif test_count > 0:
                    scores["test_coverage"] = 9.0
                else:
                    scores["test_coverage"] = 8.0
            else:
                scores["test_coverage"] = 7.0
                failures.append("Test evidence present but no positive test results")
        else:
            scores["test_coverage"] = 3.0
            failures.append("No test evidence found")
            blocking_conditions.append("missing_tests")

        # --- 3. Security Validation (target: 10.0) ---
        has_security_issues = any(
            "secret" in e.get("claim", "").lower() or "cve" in e.get("claim", "").lower()
            for e in evidence_list
        )
        secrets_scan = any(
            e.get("type") == "security" or "security" in e.get("claim", "").lower()
            for e in evidence_list
        )
        if secrets_scan and not has_security_issues:
            scores["security_validation"] = 10.0
        elif not secrets_scan and not has_security_issues:
            scores["security_validation"] = 7.0
            failures.append("No security scan evidence found (assumed safe)")
        else:
            scores["security_validation"] = 0.0
            failures.append("Security issues detected")
            blocking_conditions.append("secrets_detected")
            deductions += 2.0

        # --- 4. Rollback Readiness (target: 10.0) ---
        has_rollback = any(
            "rollback" in e.get("claim", "").lower() or e.get("type") == "rollback"
            for e in evidence_list
        )
        rollback_with_details = any(
            e.get("type") == "rollback"
            and "details" in e
            and isinstance(e.get("details"), dict)
            and "steps" in e["details"]
            for e in evidence_list
        )
        has_git_diff = any(
            e.get("type") == "diff" and "clean" not in e.get("claim", "").lower()
            for e in evidence_list
        )
        if rollback_with_details:
            scores["rollback_readiness"] = 10.0
        elif has_rollback:
            scores["rollback_readiness"] = 9.0
        elif has_git_diff:
            scores["rollback_readiness"] = 7.0
            failures.append("Changes detected but no explicit rollback plan")
        else:
            scores["rollback_readiness"] = 5.0
            failures.append("No rollback plan evidence")
            blocking_conditions.append("missing_rollback_plan")

        # --- 5. Diff Quality (target: 10.0) ---
        diff_entries = [e for e in evidence_list if e.get("type") == "diff"]
        if diff_entries:
            best = 0
            for de in diff_entries:
                claim = de.get("claim", "").lower()
                if "clean" in claim:
                    best = max(best, 8.0)
                elif "commit" in claim or "diff" in claim:
                    best = max(best, 9.0)
                if "details" in de:
                    best = max(best, 10.0)
            scores["diff_quality"] = best if best > 0 else 7.0
        else:
            scores["diff_quality"] = 5.0
            failures.append("No diff summary evidence")
            blocking_conditions.append("missing_diff_summary")

        # --- 6. Code Quality (target: 10.0) ---
        code_entries = [e for e in evidence_list if e.get("type") == "code" and e.get("verified", False)]

        if self.quality_metrics:
            qscore = self.quality_metrics.get("overall", 5.0)
            dims = self.quality_metrics.get("dimensions", {})
            qd = self.quality_metrics.get("details", {})

            all_dims_high = all(
                dims.get(d, {}).get("score", 0) >= 9.0
                for d in ["linter", "type_checker", "documentation", "module_organization"]
            )
            if all_dims_high:
                scores["code_quality"] = 10.0
            elif qscore >= 9.0:
                scores["code_quality"] = 10.0
            else:
                scores["code_quality"] = min(qscore, 10.0)

            linters = qd.get("linter_configs_found", [])
            has_readme = qd.get("has_readme", False)
            documented = qd.get("documented_languages", [])
            module_indicators = qd.get("module_indicators", [])

            quality_notes = []
            if linters:
                quality_notes.append("Linter configs: " + ", ".join(linters[:4]))
            if has_readme:
                quality_notes.append("README found")
            if documented:
                quality_notes.append(str(len(documented)) + " languages with documentation")
            if module_indicators:
                quality_notes.append("Module indicators: " + ", ".join(module_indicators[:4]))
            if quality_notes:
                failures.append("Code quality: " + "; ".join(quality_notes[:3]))
        elif code_entries:
            has_details = any("details" in e for e in code_entries)
            code_count = 0
            for ce in code_entries:
                det = ce.get("details", {})
                if isinstance(det, dict):
                    code_count = max(code_count, det.get("file_count", 0))
            if has_details and code_count > 5:
                scores["code_quality"] = 8.0
            else:
                scores["code_quality"] = 7.0
            failures.append("Code quality: basic verification (run quality analyzer for deeper check)")
        else:
            scores["code_quality"] = 5.0
            failures.append("No verified code evidence")

        # Calculate final score
        weighted_sum = sum(
            scores[cat] * CATEGORIES[cat]["weight"]
            for cat in CATEGORIES
        )
        final_score = round(weighted_sum - deductions, 2)
        final_score = max(0.0, min(10.0, final_score))

        # Decision
        if blocking_conditions:
            decision = "BLOCKED"
            blocking_reason = "Blocking conditions: " + ", ".join(blocking_conditions)
        elif final_score < BLOCK_THRESHOLD:
            decision = "BLOCKED"
            blocking_reason = "Score " + str(final_score) + " below block threshold " + str(BLOCK_THRESHOLD)
        elif final_score < MIN_SCORE_TO_PASS:
            decision = "NEEDS_REWORK"
            blocking_reason = "Score " + str(final_score) + " below minimum " + str(MIN_SCORE_TO_PASS)
        else:
            decision = "PASS"
            blocking_reason = None

        return {
            "judge_id": self.judge_id,
            "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "decision": decision,
            "final_score": final_score,
            "scores": scores,
            "deductions": deductions,
            "failures": failures,
            "blocking_conditions": blocking_conditions,
            "blocking_reason": blocking_reason,
            "evidence_count": len(evidence_list),
            "missing_evidence_types": missing_evidence,
            "next_steps": self._next_steps(decision, failures, missing_evidence),
        }

    def _blocked(self, reason):
        return {
            "judge_id": self.judge_id,
            "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "decision": "BLOCKED",
            "final_score": 0.0,
            "scores": {},
            "deductions": 10.0,
            "failures": [reason],
            "blocking_conditions": ["judge_is_implementer"],
            "blocking_reason": reason,
            "evidence_count": 0,
            "missing_evidence_types": REQUIRED_EVIDENCE_TYPES,
            "next_steps": ["Reassign judge to a different agent", "Re-run evaluation"],
        }

    def _next_steps(self, decision, failures, missing_evidence):
        steps = []
        if decision == "PASS":
            steps.append("Finalizar e arquivar tarefa")
            steps.append("Registrar licao aprendida")
            steps.append("Atualizar documentacao se necessario")
        elif decision == "NEEDS_REWORK":
            steps.append("Corrigir falhas identificadas")
            steps.append("Coletar evidencias adicionais")
            steps.append("Re-submeter para avaliacao")
        elif decision == "BLOCKED":
            steps.append("Corrigir condicoes de bloqueio")
            steps.append("Obter aprovacao humana se necessario")
            steps.append("Coletar evidencias faltantes")
            steps.append("Executar rollback se aplicavel")
            steps.append("Re-submeter para avaliacao")
        if missing_evidence:
            steps.append("Adicionar evidencias de tipo: " + ", ".join(missing_evidence))
        return steps
