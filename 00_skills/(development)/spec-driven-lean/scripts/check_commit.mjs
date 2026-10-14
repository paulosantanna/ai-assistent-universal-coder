#!/usr/bin/env node
import { readFileSync } from "node:fs";

const TYPES = ["feat", "fix", "refactor", "docs", "test", "style", "perf", "build", "ci", "chore"];
const HEADER_RE = /^(?<type>\w+)(?:\((?<scope>[^)]+)\))?(?<bang>!)?: (?<desc>.+)$/;

function parseArgs(argv) {
  const args = { message: null, msgfile: null };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--message") args.message = argv[++i] ?? "";
    else if (!argv[i].startsWith("-") && !args.msgfile) args.msgfile = argv[i];
  }
  return args;
}

function readMessage(args) {
  if (args.message !== null) return args.message;
  if (args.msgfile) return readFileSync(args.msgfile, "utf8");
  if (!process.stdin.isTTY) return readFileSync(0, "utf8");
  return "";
}

function check(message) {
  const errors = [];
  const warnings = [];
  const lines = message.split(/\r?\n/).filter((ln) => !ln.trimStart().startsWith("#"));
  while (lines.length && !lines[0].trim()) lines.shift();
  if (!lines.length) return { errors: ["empty commit message"], warnings };
  const header = lines[0].replace(/\s+$/, "");
  if (header.length > 72) warnings.push(`header is ${header.length} chars (>72): ${header.slice(0, 60)}...`);
  const match = HEADER_RE.exec(header);
  if (!match) {
    errors.push(`header does not match 'type(scope): description': ${JSON.stringify(header)}`);
    return { errors, warnings };
  }
  const { type, desc, bang } = match.groups;
  if (!TYPES.includes(type)) errors.push(`type '${type}' is not one of: ${TYPES.join(", ")}`);
  if (!desc.trim()) errors.push("description is empty");
  else {
    if (desc[0] === desc[0].toUpperCase() && desc[0] !== desc[0].toLowerCase()) {
      errors.push(`description should start lowercase: '${desc.slice(0, 30)}'`);
    }
    if (desc.trimEnd().endsWith(".")) errors.push("description should not end with a period");
  }
  const body = lines.slice(1).join("\n");
  if (bang && !/^BREAKING CHANGE:/m.test(body)) {
    errors.push("'!' breaking marker present but no 'BREAKING CHANGE:' footer");
  }
  return { errors, warnings };
}

const args = parseArgs(process.argv.slice(2));
const message = readMessage(args);
if (!message.trim()) {
  console.error("check_commit: no message provided (pass a file, --message, or pipe via stdin).");
  process.exit(2);
}
const { errors, warnings } = check(message);
for (const warning of warnings) console.log(`  WARN  ${warning}`);
for (const error of errors) console.log(`  ERROR ${error}`);
if (errors.length) {
  console.log("\ncheck_commit: FAIL - see https://www.conventionalcommits.org/en/v1.0.0/");
  process.exit(1);
}
console.log("check_commit: OK");
