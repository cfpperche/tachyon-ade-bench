import { execFileSync } from "node:child_process";

export function createWorktree(repo: string, path: string, branch: string): void {
  execFileSync("git", ["worktree", "add", "-b", branch, path], { cwd: repo });
}
