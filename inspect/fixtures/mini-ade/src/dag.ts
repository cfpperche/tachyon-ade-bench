export type TaskNode = {
  id: string;
  dependsOn: string[];
};

export function topologicalSchedule(nodes: TaskNode[]): string[] {
  const incoming = new Map<string, number>();
  const edges = new Map<string, string[]>();
  for (const node of nodes) {
    incoming.set(node.id, incoming.get(node.id) ?? 0);
    edges.set(node.id, []);
  }
  for (const node of nodes) {
    for (const parent of node.dependsOn) {
      edges.get(parent)?.push(node.id);
      incoming.set(node.id, (incoming.get(node.id) ?? 0) + 1);
    }
  }
  const ready = [...incoming.entries()].filter(([, n]) => n === 0).map(([id]) => id);
  const ordered: string[] = [];
  while (ready.length) {
    const id = ready.pop() as string;
    ordered.push(id);
    for (const child of edges.get(id) ?? []) {
      const next = (incoming.get(child) ?? 1) - 1;
      incoming.set(child, next);
      if (next === 0) ready.push(child);
    }
  }
  if (ordered.length !== nodes.length) {
    throw new Error("cycle detect: taskGraph is not a DAG");
  }
  return ordered;
}
