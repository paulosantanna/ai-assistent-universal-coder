import type { JudgeReport, Task, Evidence } from "../types.js";
export declare class JudgeEngine {
    judge(task: Task, evidence: Evidence[]): JudgeReport;
}
