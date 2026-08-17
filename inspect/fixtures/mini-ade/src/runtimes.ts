export const guestRuntimes = [
  "claude-code",
  "codex-cli",
  "grok-build",
];

export function launchGuest(runtime: string, prompt: string): string[] {
  if (runtime === "claude-code") return ["claude", prompt];
  if (runtime === "codex-cli") return ["codex", "exec", prompt];
  if (runtime === "grok-build") return ["grok", prompt];
  throw new Error(`unsupported runtime: ${runtime}`);
}
