import {
  LanguageClient,
  ServerOptions,
  LanguageClientOptions,
  CloseAction,
  ErrorAction,
  Message,
  RevealOutputChannelOn,
  State,
} from 'vscode-languageclient/node';
import * as vscode from 'vscode';
import { getAEOSConfig } from './configuration';

const outputChannel = vscode.window.createOutputChannel('AEOS Language Server', { log: true });

export function createClient(context: vscode.ExtensionContext): LanguageClient {
  const config = getAEOSConfig();

  const serverOptions: ServerOptions = {
    command: config.command,
    args: buildArgs(config),
    transport: 'stdio',
    options: {
      env: {
        ...process.env,
        AEOS_LSP_LOG_LEVEL: config.logLevel,
      },
    },
  };

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
      fileEvents: vscode.workspace.createFileSystemWatcher(
        '**/*.{aeos,aeos.yaml,aeos.yml,aeos.json,aeos.jsonc,aeos.toml,agent.md,skill.md,playbook.md}'
      ),
    },
    initializationOptions: {
      maxDiagnosticsPerFile: config.maxDiagnosticsPerFile,
      maxWorkspaceDiagnostics: config.maxWorkspaceDiagnostics,
      enableExperimentalFeatures: config.enableExperimentalFeatures,
      logLevel: config.logLevel,
      debounceMilliseconds: vscode.workspace.getConfiguration('aeos-lsp').get('debounceMilliseconds', 300),
      indexingConcurrency: vscode.workspace.getConfiguration('aeos-lsp').get('indexingConcurrency', 4),
      backgroundIndexing: vscode.workspace.getConfiguration('aeos-lsp').get('backgroundIndexing', true),
      diagnosticProfile: vscode.workspace.getConfiguration('aeos-lsp').get('diagnosticProfile', 'editor'),
    },
    outputChannel,
    traceOutputChannel: outputChannel,
    revealOutputChannelOn: RevealOutputChannelOn.Never,
    progressOnInitialization: true,
    markdown: {
      isTrusted: true,
      supportHtml: true,
    },
    errorHandler: {
      error(error: Error, message: Message, count: number): ErrorAction {
        outputChannel.error(`LSP error (count=${count}): ${error.message}`);
        if (count < 3) {
          return ErrorAction.Continue;
        }
        return ErrorAction.Shutdown;
      },
      closed(): CloseAction {
        outputChannel.warn('LSP connection closed unexpectedly — restarting...');
        return CloseAction.Restart;
      },
    },
  };

  const client = new LanguageClient('aeos-lsp', 'AEOS Language Server', serverOptions, clientOptions);

  client.onDidChangeState((event) => {
    const oldState = stateToString(event.oldState);
    const newState = stateToString(event.newState);
    outputChannel.info(`State change: ${oldState} -> ${newState}`);

    if (event.newState === State.Starting) {
      vscode.window.setStatusBarMessage('$(sync~spin) AEOS Language Server starting...');
    } else if (event.newState === State.Running) {
      vscode.window.setStatusBarMessage('$(check) AEOS Language Server ready', 3000);
    } else if (event.newState === State.Stopped) {
      vscode.window.setStatusBarMessage('$(error) AEOS Language Server stopped', 3000);
    }
  });

  return client;
}

function buildArgs(config: ReturnType<typeof getAEOSConfig>): string[] {
  const args: string[] = [...config.args];
  if (config.profile) {
    args.push('--profile', config.profile);
  }
  return args;
}

function stateToString(state: State): string {
  switch (state) {
    case State.Starting: return 'Starting';
    case State.Running: return 'Running';
    case State.Stopped: return 'Stopped';
    default: return 'Unknown';
  }
}

export { outputChannel };
