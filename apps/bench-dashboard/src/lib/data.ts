import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import type { Competitor, CompetitorSummary, TaskMeta } from "./types";

function findRepoRoot(start: string): string {
  let current = resolve(start);
  while (current !== dirname(current)) {
    if (
      existsSync(join(current, "competitors")) &&
      existsSync(join(current, "tasks")) &&
      existsSync(join(current, "harness"))
    ) {
      return current;
    }
    current = dirname(current);
  }
  throw new Error(`Unable to locate repository root from ${start}`);
}

const repoRoot = findRepoRoot(process.env.INIT_CWD ?? process.cwd());
const competitorsDir = resolve(repoRoot, "competitors");
const tasksDir = resolve(repoRoot, "tasks");

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf-8")) as T;
}

export function getCompetitors(): Competitor[] {
  return readdirSync(competitorsDir)
    .filter((file) => file.endsWith(".json"))
    .map((file) => readJson<Competitor>(join(competitorsDir, file)))
    .sort((a, b) => {
      if (a.id === "tachyon") return -1;
      if (b.id === "tachyon") return 1;
      return a.name.localeCompare(b.name);
    });
}

export function getCompetitor(id: string): Competitor | undefined {
  return getCompetitors().find((competitor) => competitor.id === id);
}

export function getTasks(): TaskMeta[] {
  return readdirSync(tasksDir)
    .filter((dir) => dir.startsWith("T"))
    .map((dir) => readJson<TaskMeta>(join(tasksDir, dir, "task.json")))
    .sort((a, b) => a.id.localeCompare(b.id));
}

export function summarizeCompetitor(competitor: Competitor): CompetitorSummary {
  const features = competitor.research.features;
  const featureCount = Object.values(features).reduce(
    (total, values) => total + values.length,
    0,
  );
  const stack = [
    ...competitor.research.stack.runtime,
    ...competitor.research.stack.frontend,
    ...competitor.research.stack.backend,
    ...competitor.research.stack.packaging,
  ];
  const localSignals = [
    competitor.research.positioning,
    ...competitor.research.infrastructure,
    ...stack,
  ].join(" ").toLowerCase();
  const enterpriseSignals = ["enterprise", "saas", "hosted", "cloud"];
  const localTerms = ["local", "offline", "desktop", "worktree", "127.0.0.1", "self-host"];
  const localHits = localTerms.filter((term) => localSignals.includes(term)).length;
  const enterpriseHits = enterpriseSignals.filter((term) => localSignals.includes(term)).length;
  const localScore =
    competitor.class === "B-enterprise-agentic-platform"
      ? 24
      : Math.max(35, Math.min(92, 46 + localHits * 9 - enterpriseHits * 8));
  const orchestrationScore = Math.max(
    25,
    Math.min(
      96,
      28 +
        features.orchestration.length * 7 +
        features.agent_support.length * 3 +
        features.workspace_isolation.length * 4,
    ),
  );

  return {
    id: competitor.id,
    name: competitor.name,
    class: competitor.class,
    license: competitor.license,
    sourceUrl: competitor.source_url,
    homepage: competitor.homepage,
    positioning: competitor.research.positioning,
    readiness: competitor.research.benchmarking.readiness,
    confidence: competitor.research.confidence,
    sourceCount: competitor.research.sources.length,
    featureCount,
    taskCount: competitor.research.benchmarking.suggested_first_tasks.length,
    localScore,
    orchestrationScore,
    stack: Array.from(new Set(stack)).slice(0, 8),
    integrations: competitor.research.features.integrations,
    suggestedTasks: competitor.research.benchmarking.suggested_first_tasks,
  };
}

export function getSummaries(): CompetitorSummary[] {
  return getCompetitors().map(summarizeCompetitor);
}

export function countBy<T extends string>(values: T[]): Record<T, number> {
  return values.reduce(
    (counts, value) => {
      counts[value] = (counts[value] ?? 0) + 1;
      return counts;
    },
    {} as Record<T, number>,
  );
}
