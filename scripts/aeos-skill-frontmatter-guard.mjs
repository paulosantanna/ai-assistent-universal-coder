#!/usr/bin/env node
import { existsSync, lstatSync, readFileSync, readdirSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';

const skillsRoot = resolve(process.argv[2] || 'skills');
const skillFiles = [];
const errors = [];

function displayPath(filePath) {
  return relative(process.cwd(), filePath).replaceAll('\\', '/');
}

function walk(directory) {
  const entries = readdirSync(directory, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name));

  for (const entry of entries) {
    const fullPath = join(directory, entry.name);
    const stat = lstatSync(fullPath);
    if (stat.isSymbolicLink()) {
      if (entry.name === 'SKILL.md') errors.push(`${displayPath(fullPath)}: SKILL.md must not be a symbolic link`);
      continue;
    }
    if (entry.isDirectory()) {
      walk(fullPath);
      continue;
    }
    if (entry.isFile() && entry.name === 'SKILL.md') skillFiles.push(fullPath);
  }
}

function frontmatterValue(lines, key) {
  const prefix = new RegExp(`^${key}\\s*:\\s*(.*)$`);
  for (let index = 0; index < lines.length; index += 1) {
    const match = prefix.exec(lines[index]);
    if (!match) continue;
    const raw = match[1].trim();
    if (/^[|>]([+-])?$/.test(raw)) {
      const block = [];
      for (let next = index + 1; next < lines.length; next += 1) {
        if (!/^\s+/.test(lines[next])) break;
        if (lines[next].trim()) block.push(lines[next].trim());
      }
      return block.join(' ').trim();
    }
    return raw.replace(/^(["'])(.*)\1$/, '$2').trim();
  }
  return '';
}

function validateSkill(filePath) {
  const raw = readFileSync(filePath, 'utf8');
  const text = raw.replace(/^\uFEFF/, '').replace(/\r\n?/g, '\n');
  const lines = text.split('\n');
  const path = displayPath(filePath);

  if (lines[0] !== '---') {
    errors.push(`${path}: missing YAML frontmatter opening delimiter on line 1`);
    return;
  }

  const closing = lines.indexOf('---', 1);
  if (closing < 0) {
    errors.push(`${path}: missing YAML frontmatter closing delimiter`);
    return;
  }
  if (closing === 1) {
    errors.push(`${path}: YAML frontmatter is empty`);
    return;
  }

  const frontmatterLines = lines.slice(1, closing);
  const name = frontmatterValue(frontmatterLines, 'name');
  const description = frontmatterValue(frontmatterLines, 'description');

  if (!name || /^(null|~)$/i.test(name)) errors.push(`${path}: YAML frontmatter requires non-empty name`);
  if (!description || /^(null|~)$/i.test(description)) errors.push(`${path}: YAML frontmatter requires non-empty description`);
}

if (!existsSync(skillsRoot) || !lstatSync(skillsRoot).isDirectory()) {
  console.error(JSON.stringify({ status: 'FAIL', guard: 'skill-frontmatter', errors: [`skills root not found: ${skillsRoot}`] }, null, 2));
  process.exit(1);
}

walk(skillsRoot);
for (const filePath of skillFiles) validateSkill(filePath);

if (skillFiles.length === 0) errors.push(`no SKILL.md files found under ${displayPath(skillsRoot)}`);

if (errors.length > 0) {
  console.error(JSON.stringify({
    status: 'FAIL',
    guard: 'skill-frontmatter',
    scanned: skillFiles.length,
    invalid: errors.length,
    errors
  }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({
  status: 'PASS',
  guard: 'skill-frontmatter',
  scanned: skillFiles.length,
  invalid: 0,
  contract: ['opening --- on line 1', 'closing ---', 'non-empty name', 'non-empty description']
}, null, 2));
