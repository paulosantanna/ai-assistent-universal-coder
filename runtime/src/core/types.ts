export type EvidenceType =
  | "code"
  | "command"
  | "test"
  | "config"
  | "diff"
  | "source"
  | "benchmark"
  | "security"
  | "clinical"
  | "regulatory";

export type MemoryType =
  | "observation"
  | "evidence"
  | "finding"
  | "lesson"
  | "validated_lesson"
  | "golden_knowledge"
  | "principle";

export type ArtifactType =
  | "prompt"
  | "subagents"
  | "adr"
  | "lesson"
  | "bridge"
  | "context"
  | "remediation"
  | "backlog"
  | "workflow"
  | "runbook"
  | "policy"
  | "ci"
  | "release"
  | "provider"
  | "snapshot"
  | "checklist"
  | "delivery"
  | "agent_run";

export type AgentObjective = "audit" | "judge" | "remediate";

export interface RuntimeState {
  projectPath: string;
  runtimePath: string;
  initializedAt: string;
  updatedAt: string;
  version: string;
  aeosInstalled: boolean;
  loadedAeosFiles: number;
  missingCriticalFiles: string[];
}

export interface ProjectScan {
  projectPath: string;
  scannedAt: string;
  fileCount: number;
  directoryCount: number;
  detectedLanguages: string[];
  detectedBuildTools: string[];
  manifests: string[];
  testIndicators: string[];
  ciIndicators: string[];
  dockerIndicators: string[];
  aeosInstalled: boolean;
  packageJson: {
    exists: boolean;
    scripts: string[];
  };
}

export interface GateDefinition {
  gateId: string;
  title: string;
  command: string;
  args: string[];
  timeoutMs: number;
}

export interface GateRunResult {
  gateId: string;
  command: string;
  args: string[];
  cwd: string;
  exitCode: number | null;
  timedOut: boolean;
  stdout: string;
  stderr: string;
  startedAt: string;
  finishedAt: string;
  resultFile?: string;
}

export interface Task {
  taskId: string;
  objective: string;
  status: "planned" | "running" | "blocked" | "complete";
  createdAt: string;
  updatedAt: string;
  acceptanceCriteria: string[];
  specialistTasks: Array<{
    specialistId: string;
    role: string;
    objective: string;
    status: "pending" | "running" | "done" | "blocked";
  }>;
}

export interface GeneratedArtifact {
  artifactId: string;
  type: ArtifactType;
  path: string;
  createdAt: string;
}

export type ProviderName = "ollama" | "deepseek" | "openai-compatible" | "opencode";

export interface ProviderConfig {
  provider: ProviderName;
  baseUrl: string;
  model: string;
  apiKeyEnv?: string;
  maxInputChars?: number;
  maxOutputTokens?: number;
  temperature?: number;
  economyMode?: boolean;
  updatedAt: string;
}

export interface AgentRun {
  runId: string;
  objective: AgentObjective;
  provider: ProviderName;
  model: string;
  projectPath: string;
  promptPath: string;
  responsePath: string;
  startedAt: string;
  finishedAt: string;
  success: boolean;
  error?: string;
}
