import * as vscode from 'vscode';

export interface AEOSConfig {
  command: string;
  args: string[];
  profile: string;
  logLevel: string;
  maxDiagnosticsPerFile: number;
  maxWorkspaceDiagnostics: number;
  enableExperimentalFeatures: boolean;
}

const VALID_LOG_LEVELS = new Set(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']);

const DEFAULTS: AEOSConfig = {
  command: 'aeos-lsp',
  args: [],
  profile: '',
  logLevel: 'WARNING',
  maxDiagnosticsPerFile: 100,
  maxWorkspaceDiagnostics: 500,
  enableExperimentalFeatures: false,
};

export function getAEOSConfig(): AEOSConfig {
  const config = vscode.workspace.getConfiguration('aeos-lsp');

  const command = config.get<string>('command', DEFAULTS.command);
  const args = config.get<string[]>('args', DEFAULTS.args);
  const profile = config.get<string>('profile', DEFAULTS.profile);
  const logLevel = normalizeLogLevel(config.get<string>('logLevel', DEFAULTS.logLevel));
  const maxDiagnosticsPerFile = validatePositiveInt(
    config.get<number>('maxDiagnosticsPerFile', DEFAULTS.maxDiagnosticsPerFile),
    DEFAULTS.maxDiagnosticsPerFile,
  );
  const maxWorkspaceDiagnostics = validatePositiveInt(
    config.get<number>('maxWorkspaceDiagnostics', DEFAULTS.maxWorkspaceDiagnostics),
    DEFAULTS.maxWorkspaceDiagnostics,
  );
  const enableExperimentalFeatures = config.get<boolean>(
    'enableExperimentalFeatures',
    DEFAULTS.enableExperimentalFeatures,
  );

  return {
    command,
    args,
    profile,
    logLevel,
    maxDiagnosticsPerFile,
    maxWorkspaceDiagnostics,
    enableExperimentalFeatures,
  };
}

function normalizeLogLevel(level: string): string {
  const upper = level.toUpperCase();
  if (VALID_LOG_LEVELS.has(upper)) {
    return upper;
  }
  return DEFAULTS.logLevel;
}

function validatePositiveInt(value: number, fallback: number): number {
  if (Number.isFinite(value) && value >= 1) {
    return Math.floor(value);
  }
  return fallback;
}
