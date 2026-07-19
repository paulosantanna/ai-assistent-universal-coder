export interface N8nConfig {
    baseUrl: string;
    webhookPath: string;
    allowedWorkflows: string[];
    dryRun: boolean;
    timeoutMs: number;
}
export interface N8nTriggerRequest {
    workflowId: string;
    payload: Record<string, unknown>;
    correlationId?: string;
}
export interface N8nTriggerResult {
    workflowId: string;
    correlationId: string;
    dryRun: boolean;
    accepted: boolean;
    status?: number;
    response?: unknown;
}
export declare const N8N_WORKFLOW_TEMPLATES: readonly [{
    readonly id: "aeos-quality-gates";
    readonly purpose: "Execute allowlisted AEOS quality gates";
}, {
    readonly id: "aeos-observability-bootstrap";
    readonly purpose: "Provision governed observability workflows";
}, {
    readonly id: "spec-driven-delivery";
    readonly purpose: "Orchestrate an approved specification delivery";
}];
export declare function configureN8n(projectPath: string, config: N8nConfig): N8nConfig;
export declare function readN8nConfig(projectPath: string): N8nConfig;
export declare function listN8nTemplates(): typeof N8N_WORKFLOW_TEMPLATES;
export declare function triggerN8n(projectPath: string, request: N8nTriggerRequest): Promise<N8nTriggerResult>;
