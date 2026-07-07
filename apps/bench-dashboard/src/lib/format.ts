export function label(value: string): string {
  return value
    .replace(/-/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase())
    .replace(/\bAde\b/g, "ADE");
}

export function readinessLabel(value: string): string {
  const labels: Record<string, string> = {
    "manual-ready": "Manual ready",
    "needs-install": "Needs install",
    "enterprise-gated": "Enterprise gated",
    "owned-reference": "Owned reference",
    "research-only": "Research only",
  };
  return labels[value] ?? label(value);
}

export function classLabel(value: string): string {
  const labels: Record<string, string> = {
    "A-local-ade": "Class A",
    "B-enterprise-agentic-platform": "Class B",
  };
  return labels[value] ?? value;
}
