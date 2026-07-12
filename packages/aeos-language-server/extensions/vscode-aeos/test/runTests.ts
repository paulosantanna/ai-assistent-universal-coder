import * as path from 'path';
import * as cp from 'child_process';

async function runTests(): Promise<void> {
  const testRunnerPath = path.resolve(__dirname, '../../node_modules/vscode-test/out/runTest.js');

  try {
    require.resolve(testRunnerPath);
  } catch {
    console.error(
      'vscode-test not found. Install with: npm install --save-dev @vscode/test-electron'
    );
    process.exit(1);
  }

  const { runTests } = require(testRunnerPath) as {
    runTests: (options: {
      extensionDevelopmentPath: string;
      extensionTestsPath: string;
      launchArgs?: string[];
      version?: string;
    }) => Promise<void>;
  };

  const extensionDevelopmentPath = path.resolve(__dirname, '../..');
  const extensionTestsPath = path.resolve(__dirname, './suite/index');

  try {
    await runTests({
      extensionDevelopmentPath,
      extensionTestsPath,
      launchArgs: [
        '--disable-extensions',
        '--skip-welcome',
        '--skip-release-notes',
      ],
      version: 'stable',
    });
  } catch (err) {
    console.error('VS Code extension tests failed:', err);
    process.exit(1);
  }
}

void runTests();
