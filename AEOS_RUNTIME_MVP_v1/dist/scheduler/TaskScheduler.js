import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
export class TaskScheduler {
    createPlan(projectPath, objective) {
        const dir = join(projectPath, ".aeos-runtime", "tasks");
        mkdirSync(dir, { recursive: true });
        const now = new Date().toISOString();
        const task = {
            taskId: crypto.randomUUID(),
            objective,
            status: "planned",
            riskLevel: "medium",
            createdAt: now,
            updatedAt: now,
            acceptanceCriteria: [
                "Objective is restated and scoped.",
                "Repository context is inspected before claims.",
                "Execution plan is decomposed into specialist tasks.",
                "Evidence requirements are defined.",
                "Verification strategy is defined.",
                "Judge review is performed before completion."
            ],
            specialistTasks: [
                { specialistId: crypto.randomUUID(), role: "Architecture Specialist", objective: "Identify architecture impact and required ADRs.", expectedOutput: "Architecture analysis report.", evidenceRequired: ["Relevant files inspected", "Architecture boundaries identified"], status: "pending" },
                { specialistId: crypto.randomUUID(), role: "Implementation Specialist", objective: "Identify implementation scope and likely affected files.", expectedOutput: "Implementation plan.", evidenceRequired: ["Files inspected", "Dependencies identified"], status: "pending" },
                { specialistId: crypto.randomUUID(), role: "Verification Specialist", objective: "Define tests, gates and validation commands.", expectedOutput: "Verification plan.", evidenceRequired: ["Build/test tooling identified"], status: "pending" },
                { specialistId: crypto.randomUUID(), role: "JudgeAgent", objective: "Review plan and evidence before completion.", expectedOutput: "Judge report.", evidenceRequired: ["Evidence ledger reviewed", "Acceptance criteria checked"], status: "pending" }
            ],
            evidenceIds: [],
            notes: []
        };
        writeFileSync(join(dir, `${task.taskId}.json`), `${JSON.stringify(task, null, 2)}\n`, "utf8");
        return task;
    }
    listTasks(projectPath) {
        const dir = join(projectPath, ".aeos-runtime", "tasks");
        if (!existsSync(dir))
            return [];
        return readdirSync(dir).filter((name) => name.endsWith(".json")).map((name) => JSON.parse(readFileSync(join(dir, name), "utf8")));
    }
    readTask(projectPath, taskId) {
        const file = join(projectPath, ".aeos-runtime", "tasks", `${taskId}.json`);
        if (!existsSync(file))
            return null;
        return JSON.parse(readFileSync(file, "utf8"));
    }
}
//# sourceMappingURL=TaskScheduler.js.map