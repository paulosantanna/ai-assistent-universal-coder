export class JudgeEngine {
    judge(task, evidence) {
        const deductions = [];
        const missingEvidence = [];
        const risks = [];
        if (task.acceptanceCriteria.length === 0)
            deductions.push("Task has no acceptance criteria.");
        if (task.specialistTasks.length === 0)
            deductions.push("Task has no specialist decomposition.");
        if (evidence.length === 0) {
            deductions.push("No evidence registered in evidence ledger.");
            missingEvidence.push("At least one evidence item is required before acceptance.");
        }
        const pendingSpecialists = task.specialistTasks.filter((item) => item.status !== "done");
        if (pendingSpecialists.length > 0) {
            deductions.push(`${pendingSpecialists.length} specialist task(s) are not completed.`);
            risks.push("Specialist execution is incomplete.");
        }
        const score = Math.max(0, 10 - deductions.length * 2);
        const decision = deductions.length === 0 ? "accept" : score <= 4 ? "reject" : "needs_rework";
        return { judge: "AEOS Runtime MVP JudgeAgent", taskId: task.taskId, decision, score, deductions, missingEvidence, risks, timestamp: new Date().toISOString() };
    }
}
//# sourceMappingURL=JudgeEngine.js.map