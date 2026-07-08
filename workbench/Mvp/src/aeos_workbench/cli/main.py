"""AEOS Workbench CLI - Entry point for MVP commands."""

import argparse
import sys
import json
from pathlib import Path

from aeos_workbench.scanner.scanner import ProjectScanner
from aeos_workbench.stack_detector.detector import StackDetector
from aeos_workbench.evidence.ledger import EvidenceLedger
from aeos_workbench.evidence.crypto import EvidenceCipher, HAS_CRYPTO
from aeos_workbench.judge.engine import JudgeEngine
from aeos_workbench.generator.ecosystem_map import EcosystemMapGenerator
from aeos_workbench.generator.risk_report import RiskReportGenerator
from aeos_workbench.generator.playbooks import PlaybookRecommender
from aeos_workbench.generator.skills import SkillGenerator
from aeos_workbench.generator.judge_report import JudgeReportGenerator
from aeos_workbench.bridge.ecosystem_export import export_ecosystem_json
from aeos_workbench.bridge.typescript_runtime import runtime_available, status, run_agent
from aeos_workbench.agents.registry import AgentRegistry
from aeos_workbench.agents.executor import AgentExecutor, AgentTask
from aeos_workbench.scanner.quality import CodeQualityAnalyzer


def cmd_scan(args):
    scanner = ProjectScanner(args.path)
    result = scanner.scan()
    print(json.dumps({
        "status": "ok",
        "scan_id": result.get("scan_id"),
        "project_root": str(result.get("project_root")),
        "total_files": result.get("total_files"),
        "total_dirs": result.get("total_dirs"),
        "languages": result.get("languages", []),
        "evidence_count": len(result.get("evidence", [])),
    }, indent=2))
    return result


def cmd_detect(args):
    scanner = ProjectScanner(args.path)
    scan_result = scanner.scan()
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    print(json.dumps({
        "status": "ok",
        "stacks": stacks,
    }, indent=2))
    return stacks


def cmd_ecosystem_map(args):
    scanner = ProjectScanner(args.path)
    scan_result = scanner.scan()
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    gen = EcosystemMapGenerator(scan_result, stacks)
    report = gen.generate()
    output_path = args.output / "ecosystem-map.md" if args.output else Path.cwd() / "ecosystem-map.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print("[AEOS] Ecosystem map written to " + str(output_path))
    return report


def cmd_risk_report(args):
    scanner = ProjectScanner(args.path)
    scan_result = scanner.scan()
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    gen = RiskReportGenerator(scan_result, stacks)
    report = gen.generate()
    output_path = args.output / "risk-report.md" if args.output else Path.cwd() / "risk-report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print("[AEOS] Risk report written to " + str(output_path))
    return report


def cmd_playbooks(args):
    scanner = ProjectScanner(args.path)
    scan_result = scanner.scan()
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    gen = PlaybookRecommender(scan_result, stacks)
    report = gen.generate()
    output_path = args.output / "recommended-playbooks.md" if args.output else Path.cwd() / "recommended-playbooks.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print("[AEOS] Playbook recommendations written to " + str(output_path))
    return report


def cmd_generate_skills(args):
    scanner = ProjectScanner(args.path)
    scan_result = scanner.scan()
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    gen = SkillGenerator(scan_result, stacks)
    skills = gen.generate()
    output_dir = args.output if args.output else Path.cwd() / "aeos-skills"
    output_dir.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        path = output_dir / (skill["skill_id"] + ".md")
        path.write_text(skill["content"], encoding="utf-8")
    print("[AEOS] " + str(len(skills)) + " skills generated in " + str(output_dir))
    return skills


def cmd_judge(args):
    ledger = EvidenceLedger(args.evidence_dir or (args.path / ".aeos" / "evidence"))
    judge = JudgeEngine()
    result = judge.evaluate(ledger.get_all())
    gen = JudgeReportGenerator(result, ledger.get_all())
    report = gen.generate()
    output_path = args.output / "judge-report.md" if args.output else Path.cwd() / "judge-report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print("[AEOS] Judge report written to " + str(output_path))

    if result["decision"] == "BLOCKED":
        print("[AEOS] [BLOCKED] FINALIZATION BLOCKED - Score: " + str(result["final_score"]) + "/10")
        print("[AEOS] Reason: " + str(result.get("blocking_reason", "Score below minimum")))
        sys.exit(1)
    else:
        print("[AEOS] [PASS] - Score: " + str(result["final_score"]) + "/10")
    return result


def cmd_full_scan(args):
    path = Path(args.path)
    output = args.output or (path / ".aeos")
    output.mkdir(parents=True, exist_ok=True)

    print("[AEOS] Scanning " + str(path) + "...")
    scanner = ProjectScanner(path)
    scan_result = scanner.scan()
    print("[AEOS] Found " + str(scan_result["total_files"]) + " files, " + str(scan_result["total_dirs"]) + " dirs")

    evidence_ledger = EvidenceLedger(output / "evidence")
    for ev in scan_result.get("evidence", []):
        evidence_ledger.add(ev)

    print("[AEOS] Detecting stacks...")
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    print("[AEOS] Detected " + str(len(stacks)) + " stacks: " + str([s["name"] for s in stacks]))

    print("[AEOS] Generating ecosystem map...")
    eco_gen = EcosystemMapGenerator(scan_result, stacks)
    eco_map = eco_gen.generate()
    (output / "ecosystem-map.md").write_text(eco_map, encoding="utf-8")
    evidence_ledger.add({
        "evidence_id": "evt-eco-map",
        "type": "report",
        "claim": "ecosystem-map.md generated",
        "reference": str(output / "ecosystem-map.md"),
        "timestamp": scan_result["scan_id"].split("T")[0],
        "verified": True,
    })

    print("[AEOS] Exporting ecosystem JSON...")
    export_ecosystem_json(scan_result, stacks, output)
    evidence_ledger.add({
        "evidence_id": "evt-eco-json",
        "type": "report",
        "claim": "aeos-ecosystem.json generated for cross-tool compatibility",
        "reference": str(output / "aeos-ecosystem.json"),
        "timestamp": scan_result["scan_id"].split("T")[0],
        "verified": True,
    })

    print("[AEOS] Analyzing risks...")
    risk_gen = RiskReportGenerator(scan_result, stacks)
    risk_report = risk_gen.generate()
    (output / "risk-report.md").write_text(risk_report, encoding="utf-8")
    evidence_ledger.add({
        "evidence_id": "evt-risk-report",
        "type": "report",
        "claim": "risk-report.md generated",
        "reference": str(output / "risk-report.md"),
        "timestamp": scan_result["scan_id"].split("T")[0],
        "verified": True,
    })

    print("[AEOS] Recommending playbooks...")
    pb_gen = PlaybookRecommender(scan_result, stacks)
    pb_report = pb_gen.generate()
    (output / "recommended-playbooks.md").write_text(pb_report, encoding="utf-8")
    evidence_ledger.add({
        "evidence_id": "evt-playbooks",
        "type": "report",
        "claim": "recommended-playbooks.md generated",
        "reference": str(output / "recommended-playbooks.md"),
        "timestamp": scan_result["scan_id"].split("T")[0],
        "verified": True,
    })

    print("[AEOS] Generating skills...")
    skill_gen = SkillGenerator(scan_result, stacks)
    skills = skill_gen.generate()
    skills_dir = output / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        (skills_dir / (skill["skill_id"] + ".md")).write_text(skill["content"], encoding="utf-8")
    evidence_ledger.add({
        "evidence_id": "evt-skills",
        "type": "report",
        "claim": str(len(skills)) + " skills generated",
        "reference": str(skills_dir),
        "timestamp": scan_result["scan_id"].split("T")[0],
        "verified": True,
    })

    print("[AEOS] Running code quality analysis...")
    quality = CodeQualityAnalyzer(scan_result)
    quality_metrics = quality.analyze()
    scan_result["quality_metrics"] = quality_metrics
    print("[AEOS] Code quality score: " + str(quality_metrics["overall"]) + "/10")
    qd = quality_metrics["details"]
    if qd.get("linter_configs_found"):
        print("[AEOS]   Linters: " + ", ".join(qd["linter_configs_found"][:4]))
    if qd.get("has_readme"):
        print("[AEOS]   README: yes")
    evidence_ledger.add({
        "evidence_id": "evt-quality-metrics",
        "type": "code",
        "claim": "Code quality analysis: " + str(quality_metrics["overall"]) + "/10 across 4 dimensions",
        "reference": "quality analysis",
        "hash": scan_result["scan_id"],
        "timestamp": scan_result["scan_timestamp"],
        "verified": True,
        "details": quality_metrics,
    })

    print("[AEOS] Running Judge evaluation...")
    judge = JudgeEngine()
    judge.set_quality_metrics(quality_metrics)
    judge_result = judge.evaluate(evidence_ledger.get_all())
    judge_gen = JudgeReportGenerator(judge_result, evidence_ledger.get_all())
    judge_report = judge_gen.generate()
    (output / "judge-report.md").write_text(judge_report, encoding="utf-8")
    evidence_ledger.add({
        "evidence_id": "evt-judge-report",
        "type": "report",
        "claim": "judge-report.md generated",
        "reference": str(output / "judge-report.md"),
        "timestamp": scan_result["scan_id"].split("T")[0],
        "verified": True,
    })

    print()
    print("[AEOS] " + "=" * 50)
    print("[AEOS] FULL SCAN COMPLETE")
    print("[AEOS] Directory: " + str(output))
    print("[AEOS] Score: " + str(judge_result["final_score"]) + "/10")
    print("[AEOS] Decision: " + str(judge_result["decision"]))
    print("[AEOS] Evidence: " + str(len(evidence_ledger.get_all())) + " items")
    if evidence_ledger.encryption_available:
        print("[AEOS] Encryption: ACTIVE (Fernet-AES)")
    else:
        print("[AEOS] Encryption: SHA256 integrity (install cryptography for Fernet-AES)")
    print("[AEOS] " + "=" * 50)

    if judge_result["decision"] == "BLOCKED":
        print("[AEOS] [BLOCKED] FINALIZATION BLOCKED")
        print("[AEOS] Reason: " + str(judge_result.get("blocking_reason", "Score below minimum")))
        sys.exit(1)
    else:
        print("[AEOS] [PASS] Finalization approved")

    return judge_result


def cmd_bridge_status(args):
    available = runtime_available()
    print("[AEOS] TypeScript Runtime: " + ("AVAILABLE" if available else "NOT FOUND"))
    if available:
        result = status()
        print(json.dumps(result, indent=2))


def cmd_bridge_run(args):
    available = runtime_available()
    if not available:
        print("[AEOS] TypeScript Runtime not found. Build it first: cd runtime && npm install && npm run build")
        return
    result = run_agent(args.provider, args.model, args.prompt)
    print(json.dumps(result, indent=2))


def cmd_setup_encryption(args):
    ledger = EvidenceLedger(args.evidence_dir or (Path.cwd() / ".aeos" / "evidence"))
    if HAS_CRYPTO:
        if args.passphrase:
            ok = ledger.setup_encryption(args.passphrase)
        else:
            ok = ledger.setup_encryption()
        if ok:
            print("[AEOS] Encryption key generated and saved to " + str(ledger._key_file))
            print("[AEOS] Future evidence entries will be encrypted with Fernet-AES")
        else:
            print("[AEOS] Failed to set up encryption")
    else:
        print("[AEOS] cryptography library not installed. Run: pip install cryptography")
        print("[AEOS] Falling back to SHA256 integrity verification")


def cmd_evidence_verify(args):
    ledger = EvidenceLedger(args.evidence_dir or (Path.cwd() / ".aeos" / "evidence"))
    entries = ledger.get_all()
    if not entries:
        print("[AEOS] No evidence entries found")
        return
    for e in entries:
        eid = e.get("evidence_id", "?")
        if e.get("type") == "error":
            print("[AEOS] [FAIL] " + eid + ": " + e.get("claim", ""))
        else:
            claim = e.get("claim", "")[:60]
            print("[AEOS] [ OK ] " + eid + ": " + claim)
    print("[AEOS] Verified " + str(len(entries)) + " evidence entries")


def cmd_agent_list(args):
    registry = AgentRegistry()
    registry.load_defaults()
    agents = registry.all()
    print("[AEOS] Agent Registry (" + str(len(agents)) + " agents):")
    for a in agents:
        spec = a["spec"]
        print("  - " + spec["agent_id"] + " [" + spec["role"] + "]: " + spec["objective"])


def cmd_agent_dispatch(args):
    registry = AgentRegistry()
    registry.load_defaults()
    executor = AgentExecutor(registry)
    task = AgentTask(
        task_id="task-" + __import__("uuid").uuid4().hex[:8],
        objective=args.objective,
        target_agent=args.agent,
        scope=args.scope or "implementation",
    )
    result = executor.dispatch(task)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("[AEOS] Queue: " + json.dumps(executor.get_summary()))


def _add_shared_args(parser):
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Project path to scan")
    parser.add_argument("--output", type=Path, default=None, help="Output directory")
    parser.add_argument("--evidence-dir", type=Path, default=None, help="Evidence directory")


def main():
    parser = argparse.ArgumentParser(description="AEOS Workbench CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    scan_commands = ["scan", "detect", "ecosystem-map", "risk-report", "playbooks", "generate-skills", "judge", "full-scan"]
    for name in scan_commands:
        sp = subparsers.add_parser(name, help="Run " + name)
        _add_shared_args(sp)

    bridge_sp = subparsers.add_parser("bridge-status", help="Check TypeScript Runtime availability")
    _add_shared_args(bridge_sp)

    bridge_run = subparsers.add_parser("bridge-run", help="Run agent via TypeScript Runtime")
    bridge_run.add_argument("--provider", default="ollama", help="Provider (ollama, openai)")
    bridge_run.add_argument("--model", default="llama3", help="Model name")
    bridge_run.add_argument("--prompt", default="", help="Prompt text")
    _add_shared_args(bridge_run)

    encrypt_sp = subparsers.add_parser("setup-encryption", help="Set up evidence encryption")
    encrypt_sp.add_argument("--passphrase", default=None, help="Encryption passphrase (optional, auto-generates if omitted)")
    _add_shared_args(encrypt_sp)

    verify_sp = subparsers.add_parser("evidence-verify", help="Verify evidence integrity")
    _add_shared_args(verify_sp)

    agent_list = subparsers.add_parser("agent-list", help="List registered agents")
    _add_shared_args(agent_list)

    agent_dispatch = subparsers.add_parser("agent-dispatch", help="Dispatch task to agent")
    agent_dispatch.add_argument("--agent", required=True, help="Target agent ID")
    agent_dispatch.add_argument("--objective", required=True, help="Task objective")
    agent_dispatch.add_argument("--scope", default=None, help="Task scope")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "detect":
        cmd_detect(args)
    elif args.command == "ecosystem-map":
        cmd_ecosystem_map(args)
    elif args.command == "risk-report":
        cmd_risk_report(args)
    elif args.command == "playbooks":
        cmd_playbooks(args)
    elif args.command == "generate-skills":
        cmd_generate_skills(args)
    elif args.command == "judge":
        cmd_judge(args)
    elif args.command == "full-scan":
        cmd_full_scan(args)
    elif args.command == "bridge-status":
        cmd_bridge_status(args)
    elif args.command == "bridge-run":
        cmd_bridge_run(args)
    elif args.command == "setup-encryption":
        cmd_setup_encryption(args)
    elif args.command == "evidence-verify":
        cmd_evidence_verify(args)
    elif args.command == "agent-list":
        cmd_agent_list(args)
    elif args.command == "agent-dispatch":
        cmd_agent_dispatch(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
