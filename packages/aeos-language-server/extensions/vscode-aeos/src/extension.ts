import * as vscode from 'vscode';
import { LanguageClient, ServerOptions, LanguageClientOptions } from 'vscode-languageclient/node';
import { getAEOSConfig } from './configuration';
import { registerCommands } from './commands';

let client: LanguageClient | undefined;

const outputChannel = vscode.window.createOutputChannel('AEOS Language Server');

export function activate(context: vscode.ExtensionContext): void {
  outputChannel.appendLine('AEOS Language Server extension activating...');

  const config = getAEOSConfig();
  const serverOptions = buildServerOptions(config);

  const clientOptions: LanguageClientOptions = {
    documentSelector: [
      { scheme: 'file', language: 'aeos' },
      { scheme: 'file', language: 'aeos-markdown' },
      { scheme: 'file', language: 'aeos-yaml' },
      { scheme: 'file', language: 'aeos-json' },
      { scheme: 'file', language: 'aeos-jsonc' },
      { scheme: 'file', language: 'aeos-toml' },
    ],
    synchronize: {
      fileEvents: vscode.workspace.createFileSystemWatcher('**/*.{aeos,aeos.yaml,aeos.yml,aeos.json,aeos.jsonc,aeos.toml,agent.md,skill.md,playbook.md}'),
    },
    initializationOptions: {
      maxDiagnosticsPerFile: config.maxDiagnosticsPerFile,
      maxWorkspaceDiagnostics: config.maxWorkspaceDiagnostics,
      enableExperimentalFeatures: config.enableExperimentalFeatures,
      logLevel: config.logLevel,
    },
    outputChannel,
    traceOutputChannel: outputChannel,
    progressOnInitialization: true,
    markdown: {
      isTrusted: true,
      supportHtml: true,
    },
  };

  client = new LanguageClient('aeos-lsp', 'AEOS Language Server', serverOptions, clientOptions);

  client.registerProposedFeatures();

  const disposable = client.start();
  context.subscriptions.push(disposable);

  client.onReady().then(() => {
    outputChannel.appendLine('AEOS Language Server started successfully.');
    registerCommands(context, client!);
    showIndexStatus(client!);
  }).catch((err: unknown) => {
    const message = err instanceof Error ? err.message : String(err);
    outputChannel.appendLine(`AEOS Language Server failed to start: ${message}`);
    vscode.window.showErrorMessage(`AEOS Language Server failed to start: ${message}`);
  });

  context.subscriptions.push(
    vscode.commands.registerCommand('aeos-lsp.restart', () => restartServer(context))
  );

  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration('aeos-lsp')) {
        outputChannel.appendLine('Configuration changed, restarting server...');
        restartServer(context);
      }
    })
  );

  outputChannel.appendLine('AEOS Language Server extension activated.');
}

function buildServerOptions(config: ReturnType<typeof getAEOSConfig>): ServerOptions {
  const args: string[] = [...config.args];

  if (config.profile) {
    args.push('--profile', config.profile);
  }

  const command = config.command;

  return {
    command,
    args,
    transport: 'stdio',
    options: {
      env: {
        ...process.env,
        AEOS_LSP_LOG_LEVEL: config.logLevel,
      },
    },
  };
}

async function restartServer(context: vscode.ExtensionContext): Promise<void> {
  if (client) {
    try {
      await client.stop();
    } catch (err) {
      outputChannel.appendLine(`Error stopping client: ${err}`);
    }
    client = undefined;
  }

  const idx = context.subscriptions.findIndex(
    (s) => s.toString().includes('aeos-lsp')
  );
  if (idx >= 0) {
    context.subscriptions.splice(idx, 1);
  }

  activate(context);
}

async function showIndexStatus(client: LanguageClient): Promise<void> {
  try {
    const status = await client.sendRequest<{ [key: string]: unknown }>('workspace/executeCommand', {
      command: 'aeos.refreshIndex',
      arguments: {},
    });
    outputChannel.appendLine(`Index status: ${JSON.stringify(status)}`);
  } catch {
    // Index may not be ready yet; this is non-critical
  }
}

export function deactivate(): Thenable<void> | undefined {
  outputChannel.appendLine('AEOS Language Server extension deactivating...');
  if (!client) {
    return undefined;
  }
  return client.stop();
}
