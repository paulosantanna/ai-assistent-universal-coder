export type RiskLevel = "low" | "medium" | "high" | "critical";
export type TaskStatus = "received" | "planned" | "scheduled" | "running" | "blocked" | "verifying" | "judging" | "accepted" | "rejected" | "complete";
export type EvidenceType = "code" | "command" | "test" | "config" | "diff" | "source" | "benchmark" | "security" | "clinical" | "regulatory";

export interface AeosModuleStatus {
  agentFileExists: boolean;
  foundationFiles: string[];
  executionFiles: string[];
  reasoningFiles: string[];
  knowledgeFiles: string[];
  engineeringFiles: string[];
  verificationFiles: string[];
  governanceFiles: string[];
  operationsFiles: string[];
}

export interface RuntimeState {
  projectPath: string;
  initializedAt: string;
  updatedAt: string;
  version: string;
  moduleStatus: AeosModuleStatus;
}

export interface SpecialistTask {
  specialistId: string;
  role: string;
  objective: string;
  expectedOutput: string;
  evidenceRequired: string[];
  status: "pending" | "running" | "done" | "blocked";
}

export interface Task {
  taskId: string;
  objective: string;
  status: TaskStatus;
  riskLevel: RiskLevel;
  createdAt: string;
  updatedAt: string;
  acceptanceCriteria: string[];
  specialistTasks: SpecialistTask[];
  evidenceIds: string[];
  notes: string[];
}

export interface Evidence {
  evidenceId: string;
  type: EvidenceType;
  claim: string;
  reference: string;
  verified: boolean;
  timestamp: string;
  limitations: string[];
}

export interface Checkpoint {
  checkpointId: string;
  timestamp: string;
  projectPath: string;
  summary: string;
  nextAction: string;
  taskIds: string[];
}

export interface JudgeReport {
  judge: string;
  taskId: string;
  decision: "accept" | "reject" | "block" | "needs_rework";
  score: number;
  deductions: string[];
  missingEvidence: string[];
  risks: string[];
  timestamp: string;
}
