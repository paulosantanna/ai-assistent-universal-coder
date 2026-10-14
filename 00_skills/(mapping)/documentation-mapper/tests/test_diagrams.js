const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SRC_DIR = path.resolve(__dirname, '../diagrams/src');

function test() {
  let passed = 0;
  let failed = 0;

  // Check that the generate script produces valid .mmd files
  console.log('Test: generate_diagrams.js produces output files');

  const testDir = fs.mkdtempSync('diagrams-test-');
  try {
    execSync(`node ${__dirname}/../scripts/generate_diagrams.js ${testDir}`, { stdio: 'pipe' });
    const srcDir = path.join(testDir, 'src');
    const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.mmd'));

    if (files.length === 0) {
      console.error('  FAIL: No diagram files generated');
      failed++;
    } else {
      console.log(`  PASS: ${files.length} diagram files generated`);
      passed++;
    }

    // Validate all .mmd files have content
    files.forEach(file => {
      const content = fs.readFileSync(path.join(srcDir, file), 'utf-8');
      if (content.trim().length === 0) {
        console.error(`  FAIL: Empty diagram file: ${file}`);
        failed++;
      } else {
        // Check for basic Mermaid syntax
        const hasGraph = /graph\s+(TB|LR|RL|BT)/.test(content);
        const hasErDiagram = content.includes('erDiagram');
        const hasSequence = content.includes('sequenceDiagram');
        const hasFlowchart = content.includes('flowchart');
        const hasGantt = content.includes('gantt');
        const hasMindmap = content.includes('mindmap');

        if (!hasGraph && !hasErDiagram && !hasSequence && !hasFlowchart && !hasGantt && !hasMindmap) {
          console.error(`  FAIL: ${file} has no recognizable Mermaid diagram type`);
          failed++;
        } else {
          console.log(`  PASS: ${file} has valid Mermaid syntax`);
          passed++;
        }
      }
    });
  } catch (e) {
    console.error(`  FAIL: Script execution error: ${e.message}`);
    failed++;
  } finally {
    fs.rmSync(testDir, { recursive: true, force: true });
  }

  // Check that 14 expected diagram types are generated
  console.log('Test: All 14 diagram types present');
  const expectedTypes = [
    'system-architecture', 'infrastructure', 'data-flow', 'entity-relationship',
    'mongodb-schema', 'chromadb-collections', 'api-route-map', 'component-diagram',
    'sequence-diagram', 'deployment', 'security-architecture', 'integration-map',
    'improvement-roadmap', 'project-mindmap'
  ];

  const tempDir2 = fs.mkdtempSync('diagrams-test2-');
  try {
    execSync(`node ${__dirname}/../scripts/generate_diagrams.js ${tempDir2}`, { stdio: 'pipe' });
    const srcDir = path.join(tempDir2, 'src');
    const generatedFiles = fs.readdirSync(srcDir).filter(f => f.endsWith('.mmd'));

    expectedTypes.forEach(type => {
      if (generatedFiles.includes(`${type}.mmd`)) {
        console.log(`  PASS: ${type}.mmd generated`);
        passed++;
      } else {
        console.error(`  FAIL: ${type}.mmd missing`);
        failed++;
      }
    });
  } catch (e) {
    console.error(`  FAIL: ${e.message}`);
    failed++;
  } finally {
    fs.rmSync(tempDir2, { recursive: true, force: true });
  }

  // Summary
  console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
  process.exit(failed > 0 ? 1 : 0);
}

test();
