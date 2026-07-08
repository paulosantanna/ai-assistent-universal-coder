import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { AeosRuntime } from "../runtime/AeosRuntime.js";
import { TaskScheduler } from "../scheduler/TaskScheduler.js";
import { EvidenceLedger } from "../evidence/EvidenceLedger.js";
import { MemoryStore } from "../memory/MemoryStore.js";
import { JudgeEngine } from "../judge/JudgeEngine.js";
export class AeosKernel {
    runtime = new AeosRuntime();
    scheduler = new TaskScheduler();
    evidence = new EvidenceLedger();
    memory = new MemoryStore();
    judgeEngine = new JudgeEngine();
    init(projectPath) {
        const state = this.runtime.ensureInitialized(projectPath);
        this.memory.append(projectPath, { type: "observation", summary: `AEOS runtime initialized for ${projectPath}`, evidenceIds: [] });
        console.log("AEOS initialized.");
        console.log(JSON.stringify(state, null, 2));
    }
    status(projectPath) {
        const state = this.runtime.readState(projectPath) ?? this.runtime.ensureInitialized(projectPath);
        const tasks = this.scheduler.listTasks(projectPath);
        const evidence = this.evidence.list(projectPath);
        const memory = this.memory.list(projectPath);
        console.log(JSON.stringify({ projectPath, runtimeVersion: state.version, initializedAt: state.initializedAt, updatedAt: state.updatedAt, modules: state.moduleStatus, counts: { tasks: tasks.length, evidence: evidence.length, memory: memory.length } }, null, 2));
    }
    plan(projectPath, objective) {
        this.runtime.ensureInitialized(projectPath);
        const task = this.scheduler.createPlan(projectPath, objective);
        this.memory.append(projectPath, { type: "finding", summary: `Created plan for objective: ${objective}`, evidenceIds: [] });
        console.log("Plan created.");
        console.log(JSON.stringify(task, null, 2));
    }
    checkpoint(projectPath, summary) {
        this.runtime.ensureInitialized(projectPath);
        const dir = join(projectPath, ".aeos-runtime", "checkpoints");
        mkdirSync(dir, { recursive: true });
        const tasks = this.scheduler.listTasks(projectPath);
        const checkpoint = { checkpointId: crypto.randomUUID(), timestamp: new Date().toISOString(), projectPath, summary, nextAction: "Continue from the latest planned task and validate required evidence.", taskIds: tasks.map((task) => task.taskId) };
        writeFileSync(join(dir, `${checkpoint.checkpointId}.json`), `${JSON.stringify(checkpoint, null, 2)}\n`, "utf8");
        this.memory.append(projectPath, { type: "observation", summary: `Checkpoint created: ${summary}`, evidenceIds: [] });
        console.log("Checkpoint created.");
        console.log(JSON.stringify(checkpoint, null, 2));
    }
    addEvidence(projectPath, claim, type, reference) {
        this.runtime.ensureInitialized(projectPath);
        const evidence = this.evidence.add(projectPath, claim, type, reference);
        this.memory.append(projectPath, { type: "evidence", summary: `Evidence registered for claim: ${claim}`, evidenceIds: [evidence.evidenceId] });
        console.log("Evidence registered.");
        console.log(JSON.stringify(evidence, null, 2));
    }
    judge(projectPath, taskId) {
        this.runtime.ensureInitialized(projectPath);
        const task = this.scheduler.readTask(projectPath, taskId);
        if (task === null)
            throw new Error(`Task not found: ${taskId}`);
        const evidence = this.evidence.list(projectPath);
        const report = this.judgeEngine.judge(task, evidence);
        this.memory.append(projectPath, { type: "finding", summary: `Judge decision for task ${taskId}: ${report.decision} (${report.score}/10)`, evidenceIds: evidence.map((item) => item.evidenceId) });
        console.log(JSON.stringify(report, null, 2));
    }
}
//# sourceMappingURL=AeosKernel.js.map