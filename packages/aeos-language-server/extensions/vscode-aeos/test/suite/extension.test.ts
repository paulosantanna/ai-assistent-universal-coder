import * as assert from 'assert';
import * as vscode from 'vscode';

suite('AEOS Extension Tests', () => {
  test('Extension should be present', () => {
    const ext = vscode.extensions.getExtension('AEOS.vscode-aeos');
    assert.ok(ext, 'Extension AEOS.vscode-aeos is not available');
  });

  test('Extension should activate', async () => {
    const ext = vscode.extensions.getExtension('AEOS.vscode-aeos');
    if (!ext) {
      assert.fail('Extension not found');
      return;
    }
    await ext.activate();
    assert.ok(ext.isActive, 'Extension did not activate');
  });

  test('Language aeos should be registered', () => {
    const languages = vscode.languages.getLanguages();
    assert.ok(languages.includes('aeos'), 'aeos language not registered');
  });

  test('Language aeos-markdown should be registered', () => {
    const languages = vscode.languages.getLanguages();
    assert.ok(languages.includes('aeos-markdown'), 'aeos-markdown language not registered');
  });

  test('Language aeos-yaml should be registered', () => {
    const languages = vscode.languages.getLanguages();
    assert.ok(languages.includes('aeos-yaml'), 'aeos-yaml language not registered');
  });

  test('Commands should be registered', async () => {
    const commands = await vscode.commands.getCommands();
    const aeosCommands = commands.filter((c) => c.startsWith('aeos-lsp.'));
    assert.ok(aeosCommands.length > 0, 'No aeos-lsp commands registered');
    assert.ok(aeosCommands.includes('aeos-lsp.validateDocument'), 'validateDocument command not registered');
    assert.ok(aeosCommands.includes('aeos-lsp.refreshIndex'), 'refreshIndex command not registered');
    assert.ok(aeosCommands.includes('aeos-lsp.restart'), 'restart command not registered');
  });
});
