import * as vscode from 'vscode';
import { LanguageClient } from 'vscode-languageclient/node';

const COMMAND_PREFIX = 'aeos-lsp.';

interface CommandDescriptor {
  readonly id: string;
  readonly serverCommand: string;
  readonly title: string;
  readonly requiresDocument?: boolean;
  readonly requiresWorkspace?: boolean;
}

const COMMANDS: CommandDescriptor[] = [
  { id: 'validateDocument', serverCommand: 'aeos.validateDocument', title: 'Validate Current Document', requiresDocument: true },
  { id: 'validateWorkspace', serverCommand: 'aeos.validateWorkspace', title: 'Validate Entire Workspace', requiresWorkspace: true },
  { id: 'refreshIndex', serverCommand: 'aeos.refreshIndex', title: 'Refresh Workspace Index', requiresWorkspace: true },
  { id: 'explainDiagnostic', serverCommand: 'aeos.explainDiagnostic', title: 'Explain Diagnostic at Cursor', requiresDocument: true },
  { id: 'showDependencyGraph', serverCommand: 'aeos.showDependencyGraph', title: 'Show Dependency Graph', requiresDocument: true },
  { id: 'showInheritanceGraph', serverCommand: 'aeos.showInheritanceGraph', title: 'Show Inheritance Graph', requiresDocument: true },
  { id: 'estimateTokens', serverCommand: 'aeos.estimateTokens', title: 'Estimate Token Count', requiresDocument: true },
  { id: 'judgeArtifact', serverCommand: 'aeos.judgeArtifact', title: 'Judge Current Artifact', requiresDocument: true },
  { id: 'dryRunSkill', serverCommand: 'aeos.dryRunSkill', title: 'Dry-Run Skill', requiresDocument: false },
  { id: 'dryRunPlaybook', serverCommand: 'aeos.dryRunPlaybook', title: 'Dry-Run Playbook', requiresDocument: false },
  { id: 'openEvidence', serverCommand: 'aeos.openEvidence', title: 'Open Evidence Artifact', requiresDocument: false },
  { id: 'showIndexStatus', serverCommand: 'aeos.refreshIndex', title: 'Show Index Status', requiresWorkspace: true },
];

export function registerCommands(context: vscode.ExtensionContext, client: LanguageClient): void {
  for (const cmd of COMMANDS) {
    const disposable = vscode.commands.registerCommand(
      `${COMMAND_PREFIX}${cmd.id}`,
      async () => {
        await executeCommand(cmd, client);
      }
    );
    context.subscriptions.push(disposable);
  }
}

async function executeCommand(cmd: CommandDescriptor, client: LanguageClient): Promise<void> {
  try {
    switch (cmd.serverCommand) {
      case 'aeos.validateDocument':
        return await validateDocument(client);
      case 'aeos.validateWorkspace':
        return await withProgress('Validating workspace...', () => executeServerCommand(client, cmd.serverCommand, {}));
      case 'aeos.refreshIndex':
        return await withProgress('Refreshing index...', () => executeServerCommand(client, cmd.serverCommand, {}));
      case 'aeos.explainDiagnostic':
        return await explainDiagnostic(client);
      case 'aeos.showDependencyGraph':
        return await showGraph(client, cmd.serverCommand, 'Dependency Graph');
      case 'aeos.showInheritanceGraph':
        return await showGraph(client, cmd.serverCommand, 'Inheritance Graph');
      case 'aeos.estimateTokens':
        return await estimateTokens(client);
      case 'aeos.judgeArtifact':
        return await withProgress('Judging artifact...', () => judgeArtifact(client));
      case 'aeos.dryRunSkill':
        return await dryRun('skill');
      case 'aeos.dryRunPlaybook':
        return await dryRun('playbook');
      case 'aeos.openEvidence':
        return await openEvidence();
      default:
        return await withProgress(`Running ${cmd.title}...`, () => executeServerCommand(client, cmd.serverCommand, {}));
    }
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    vscode.window.showErrorMessage(`AEOS command failed: ${message}`);
  }
}

async function executeServerCommand(client: LanguageClient, command: string, args: unknown): Promise<unknown> {
  return client.sendRequest('workspace/executeCommand', {
    command,
    arguments: args,
  });
}

function getActiveDocumentUri(): string | undefined {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage('No active editor found.');
    return undefined;
  }
  return editor.document.uri.toString();
}

function getDocumentText(): string | undefined {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    return undefined;
  }
  return editor.document.getText();
}

async function validateDocument(client: LanguageClient): Promise<void> {
  const uri = getActiveDocumentUri();
  if (!uri) return;

  const result = await withProgress('Validating document...', () =>
    executeServerCommand(client, 'aeos.validateDocument', { uri })
  );

  const count = typeof result === 'object' && result !== null && 'diagnostics' in result
    ? (result as { diagnostics: unknown[] }).diagnostics.length
    : 0;

  vscode.window.showInformationMessage(`Validation complete — ${count} diagnostic(s) found.`);
}

async function explainDiagnostic(client: LanguageClient): Promise<void> {
  const uri = getActiveDocumentUri();
  if (!uri) return;

  const editor = vscode.window.activeTextEditor;
  if (!editor) return;

  const line = editor.selection.active.line;
  const diagnostics = vscode.languages.getDiagnostics(editor.document.uri);
  const diagnostic = diagnostics.find((d) => d.range.start.line === line);

  if (!diagnostic) {
    vscode.window.showInformationMessage('No diagnostic on the current line.');
    return;
  }

  const result = await withProgress('Fetching explanation...', () =>
    executeServerCommand(client, 'aeos.explainDiagnostic', {
      uri,
      code: typeof diagnostic.code === 'object' && diagnostic.code !== null
        ? (diagnostic.code as { value: string }).value
        : String(diagnostic.code ?? 'unknown'),
    })
  );

  if (typeof result === 'string') {
    const doc = await vscode.workspace.openTextDocument({
      content: result,
      language: 'markdown',
    });
    vscode.window.showTextDocument(doc, { preview: true, viewColumn: vscode.ViewColumn.Beside });
  } else {
    const text = JSON.stringify(result, null, 2);
    const doc = await vscode.workspace.openTextDocument({
      content: text,
      language: 'json',
    });
    vscode.window.showTextDocument(doc, { preview: true, viewColumn: vscode.ViewColumn.Beside });
  }
}

async function showGraph(client: LanguageClient, command: string, title: string): Promise<void> {
  const uri = getActiveDocumentUri();
  if (!uri) return;

  const result = await withProgress(`Generating ${title}...`, () =>
    executeServerCommand(client, command, { uri })
  );

  const text = typeof result === 'string' ? result : JSON.stringify(result, null, 2);
  const doc = await vscode.workspace.openTextDocument({
    content: text,
    language: 'markdown',
  });
  vscode.window.showTextDocument(doc, { preview: true, viewColumn: vscode.ViewColumn.Beside });
}

async function estimateTokens(client: LanguageClient): Promise<void> {
  const uri = getActiveDocumentUri();
  const text = getDocumentText();
  if (!uri) return;

  const result = await withProgress('Estimating tokens...', () =>
    executeServerCommand(client, 'aeos.estimateTokens', { uri, text })
  );

  const count = typeof result === 'object' && result !== null
    ? (result as { token_count?: number }).token_count ?? result
    : result;

  vscode.window.showInformationMessage(`Estimated token count: ${count}`);
}

async function judgeArtifact(client: LanguageClient): Promise<void> {
  const uri = getActiveDocumentUri();
  if (!uri) return;

  const result = await executeServerCommand(client, 'aeos.judgeArtifact', { uri });

  const text = typeof result === 'string' ? result : JSON.stringify(result, null, 2);
  const doc = await vscode.workspace.openTextDocument({
    content: text,
    language: 'json',
  });
  vscode.window.showTextDocument(doc, { preview: true, viewColumn: vscode.ViewColumn.Beside });
}

async function dryRun(kind: 'skill' | 'playbook'): Promise<void> {
  const ref = await vscode.window.showInputBox({
    prompt: `Enter the ${kind} reference (e.g., my-${kind}:1.0.0)`,
    placeHolder: `my-${kind}:version`,
  });

  if (!ref) return;

  const serverCommand = kind === 'skill' ? 'aeos.dryRunSkill' : 'aeos.dryRunPlaybook';

  const client = getClient();
  if (!client) return;

  const result = await withProgress(`Dry-running ${kind}...`, () =>
    executeServerCommand(client, serverCommand, { [`${kind}_ref`]: ref, inputs: {} })
  );

  const text = typeof result === 'string' ? result : JSON.stringify(result, null, 2);
  const doc = await vscode.workspace.openTextDocument({
    content: text,
    language: 'json',
  });
  vscode.window.showTextDocument(doc, { preview: true, viewColumn: vscode.ViewColumn.Beside });
}

async function openEvidence(): Promise<void> {
  const artifactId = await vscode.window.showInputBox({
    prompt: 'Enter evidence artifact ID',
    placeHolder: 'artifact-uuid-or-path',
  });

  if (!artifactId) return;

  const client = getClient();
  if (!client) return;

  const result = await withProgress('Opening evidence...', () =>
    executeServerCommand(client, 'aeos.openEvidence', { artifact_id: artifactId })
  );

  const text = typeof result === 'string' ? result : JSON.stringify(result, null, 2);
  const doc = await vscode.workspace.openTextDocument({
    content: text,
    language: 'json',
  });
  vscode.window.showTextDocument(doc, { preview: true, viewColumn: vscode.ViewColumn.Beside });
}

function getClient(): LanguageClient | undefined {
  const ext = vscode.extensions.getExtension('AEOS.vscode-aeos');
  if (!ext) return undefined;
  return (ext.exports as { client?: LanguageClient }).client;
}

async function withProgress<T>(title: string, task: () => Thenable<T>): Promise<T> {
  return vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title,
      cancellable: false,
    },
    task
  );
}
