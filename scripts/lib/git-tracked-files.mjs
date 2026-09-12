import { spawnSync } from "node:child_process";

const DEFAULT_MAX_BUFFER = 64 * 1024 * 1024;

/**
 * List tracked paths without the default 1 MiB execFileSync buffer.
 * After large vendor trees (for example `.work/`) `git ls-files -z` exceeds
 * that limit and CI fails with ENOBUFS.
 */
export function listGitTrackedFiles({
  cwd = process.cwd(),
  nullTerminated = true,
  maxBuffer = DEFAULT_MAX_BUFFER
} = {}) {
  const args = nullTerminated ? ["ls-files", "-z"] : ["ls-files"];
  const result = spawnSync("git", args, {
    cwd,
    encoding: "utf8",
    maxBuffer,
    windowsHide: true
  });

  if (result.error) {
    throw result.error;
  }
  if (result.status !== 0) {
    const detail = (result.stderr || "").trim() || `git ls-files exited ${result.status}`;
    throw new Error(detail);
  }

  const raw = result.stdout ?? "";
  const parts = nullTerminated ? raw.split("\0") : raw.split(/\r?\n/);
  return parts.filter(Boolean).map((path) => path.replaceAll("\\", "/"));
}
