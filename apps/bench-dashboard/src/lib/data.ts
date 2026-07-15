import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import type {
  AcquisitionAdRow,
  AcquisitionBoardData,
  AcquisitionCampaignRow,
  AcquisitionCoverageRow,
  AcquisitionReviewItem,
  AcquisitionResult,
  AcquisitionScanHistoryRow,
  CapabilityAxis,
  Competitor,
  CompetitorSummary,
  IntelligenceBattlecard,
  IntelligenceBoardData,
  IntelligenceCategory,
  IntelligenceConfidence,
  IntelligenceFreshness,
  IntelligenceSignal,
  MarketingCampaign,
  MarketingCurrentAd,
  MarketingManifest,
  StrategyPressureAxis,
  StrategyPressureRow,
  TaskMeta,
} from "./types";
import { CAPABILITY_AXES } from "./types";

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
const marketingDir = resolve(repoRoot, "marketing");
const intelligenceDir = resolve(repoRoot, "intelligence");

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

/** Soft-cap feature-list length into a 0–100 surface score (8 listed items ≈ 100). */
export function capabilityScoreFromCount(count: number): number {
  return Math.max(0, Math.min(100, Math.round(count * 12.5)));
}

export function capabilityScoresFor(
  features: Competitor["research"]["features"],
): Record<CapabilityAxis, number> {
  return CAPABILITY_AXES.reduce(
    (scores, axis) => {
      scores[axis] = capabilityScoreFromCount(features[axis].length);
      return scores;
    },
    {} as Record<CapabilityAxis, number>,
  );
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
    capabilityScores: capabilityScoresFor(features),
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

interface CurrentAdsFile {
  ads: MarketingCurrentAd[];
  generated_at: string;
  schema_version: string;
}

interface CurrentCampaignsFile {
  campaigns: MarketingCampaign[];
  generated_at: string;
  schema_version: string;
}

interface IntelligenceSignalsFile {
  schema_version: string;
  signals: IntelligenceSignal[];
  updated_at: string;
}

function readJsonIfExists<T>(path: string, fallback: T): T {
  if (!existsSync(path)) {
    return fallback;
  }
  return readJson<T>(path);
}

function productNameMap(): Map<string, string> {
  return new Map(getCompetitors().map((competitor) => [competitor.id, competitor.name]));
}

function evidenceRefsFromNotes(notes: string | null): string[] {
  if (!notes) {
    return [];
  }
  const refs = new Set<string>();
  const pattern = /marketing\/[A-Za-z0-9_./-]+/g;
  for (const match of notes.matchAll(pattern)) {
    refs.add(match[0].replace(/[.)]+$/, ""));
  }
  return Array.from(refs);
}

function getMarketingManifests(): MarketingManifest[] {
  const scansDir = join(marketingDir, "scans");
  if (!existsSync(scansDir)) {
    return [];
  }
  return readdirSync(scansDir)
    .map((dir) => join(scansDir, dir, "manifest.json"))
    .filter((path) => existsSync(path))
    .map((path) => readJson<MarketingManifest>(path))
    .sort((a, b) => a.scan_id.localeCompare(b.scan_id));
}

function latestCoverageRows(manifest: MarketingManifest | null): AcquisitionCoverageRow[] {
  if (!manifest) {
    return [];
  }
  const names = productNameMap();
  return manifest.queries.map((query) => ({
    ...query,
    product_name: names.get(query.product_id) ?? query.product_id,
    result: query.result as AcquisitionResult,
    scan_id: manifest.scan_id,
  }));
}

function scanHistoryRows(manifests: MarketingManifest[]): AcquisitionScanHistoryRow[] {
  return manifests
    .map((manifest) => {
      const counts = manifest.queries.reduce<Record<AcquisitionResult, number>>(
        (accumulator, query) => {
          accumulator[query.result] = (accumulator[query.result] ?? 0) + 1;
          return accumulator;
        },
        { found: 0, partial: 0, blocked: 0, "not-found": 0 },
      );
      return {
        blocked: counts.blocked,
        completed_at: manifest.completed_at,
        found: counts.found,
        not_found: counts["not-found"],
        partial: counts.partial,
        platform_count: new Set(manifest.queries.map((query) => query.platform)).size,
        query_count: manifest.queries.length,
        scan_id: manifest.scan_id,
        started_at: manifest.started_at,
      };
    })
    .sort((a, b) => b.scan_id.localeCompare(a.scan_id));
}

function reviewQueueRows(rows: AcquisitionCoverageRow[]): AcquisitionReviewItem[] {
  return rows
    .filter((row) => {
      if (row.result === "partial" || row.result === "blocked") {
        return true;
      }
      return row.product_id === "kandev" && row.query === "github.com";
    })
    .map((row) => ({
      ...row,
      reason:
        row.product_id === "kandev" && row.query === "github.com"
          ? "generic-domain"
          : row.result === "blocked"
            ? "blocked-source"
            : "partial-result",
    }));
}

export function getAcquisitionBoardData(): AcquisitionBoardData {
  const manifests = getMarketingManifests();
  const latestScan = manifests.at(-1) ?? null;
  const adsFile = readJsonIfExists<CurrentAdsFile>(
    join(marketingDir, "current", "ads.json"),
    { ads: [], generated_at: "", schema_version: "0.1" },
  );
  const campaignsFile = readJsonIfExists<CurrentCampaignsFile>(
    join(marketingDir, "current", "campaigns.json"),
    { campaigns: [], generated_at: "", schema_version: "0.1" },
  );
  const names = productNameMap();
  const ads: AcquisitionAdRow[] = adsFile.ads.map((ad) => ({
    ...ad,
    product_name: names.get(ad.product_id) ?? ad.product_id,
    evidence_refs: evidenceRefsFromNotes(ad.latest.notes),
  }));
  const campaigns: AcquisitionCampaignRow[] = campaignsFile.campaigns.map((campaign) => ({
    ...campaign,
    product_name: names.get(campaign.product_id) ?? campaign.product_id,
  }));
  const coverageRows = latestCoverageRows(latestScan);
  const reviewQueue = reviewQueueRows(coverageRows);
  const platforms = new Set([
    ...coverageRows.map((row) => row.platform),
    ...ads.map((ad) => ad.platform),
    ...campaigns.map((campaign) => campaign.platform),
  ]);
  const statusCounts = coverageRows.reduce<Partial<Record<AcquisitionResult, number>>>(
    (counts, row) => {
      counts[row.result] = (counts[row.result] ?? 0) + 1;
      return counts;
    },
    {},
  );

  return {
    ads,
    campaigns,
    coverageRows,
    generatedAt: adsFile.generated_at || campaignsFile.generated_at || null,
    latestScan,
    manifests,
    platformCount: platforms.size,
    queryCount: coverageRows.length,
    reviewQueue,
    scanCount: manifests.length,
    scanHistory: scanHistoryRows(manifests),
    statusCounts,
  };
}

function pressureAxes(competitor: Competitor, hasAcquisitionSignal: boolean): StrategyPressureAxis[] {
  const features = competitor.research.features;
  const text = [
    competitor.research.positioning,
    competitor.license,
    ...competitor.research.stack.runtime,
    ...competitor.research.stack.frontend,
    ...competitor.research.stack.backend,
    ...features.orchestration,
    ...features.review_shipping,
    ...features.remote_mobile,
    ...features.integrations,
  ].join(" ").toLowerCase();
  const axes = new Set<StrategyPressureAxis>();
  if (text.includes("visual") || text.includes("cockpit") || text.includes("mobile") || text.includes("remote")) {
    axes.add("ux");
  }
  if (features.orchestration.length >= 4 || text.includes("multi-agent") || text.includes("worktree")) {
    axes.add("orchestration");
  }
  if (text.includes("review") || text.includes("diff") || text.includes("evidence") || text.includes("snapshot")) {
    axes.add("evidence");
  }
  if (competitor.class === "B-enterprise-agentic-platform" || text.includes("enterprise") || text.includes("governance")) {
    axes.add("enterprise");
  }
  if (competitor.source_url || /mit|agpl|busl|open-source|open source/i.test(competitor.license)) {
    axes.add("community");
  }
  if (hasAcquisitionSignal) {
    axes.add("acquisition");
  }
  return Array.from(axes);
}

export function getStrategyPressureRows(): StrategyPressureRow[] {
  const acquisitionProducts = new Set(
    getAcquisitionBoardData().campaigns.map((campaign) => campaign.product_id),
  );
  return getCompetitors()
    .filter((competitor) => competitor.id !== "tachyon")
    .map((competitor) => {
      const hasAcquisitionSignal = acquisitionProducts.has(competitor.id);
      const axes = pressureAxes(competitor, hasAcquisitionSignal);
      return {
        acquisitionSignal: hasAcquisitionSignal,
        axes,
        class: competitor.class,
        id: competitor.id,
        name: competitor.name,
        pressure:
          axes.length >= 5 || competitor.id === "orca" || competitor.id === "augment-code"
            ? "high"
            : axes.length >= 3
              ? "medium"
              : "focused",
        readiness: competitor.research.benchmarking.readiness,
        summary: competitor.research.positioning,
      };
    });
}

function increment<T extends string>(counts: Partial<Record<T, number>>, key: T): void {
  counts[key] = (counts[key] ?? 0) + 1;
}

function topTags(signals: IntelligenceSignal[]): string[] {
  const counts = new Map<string, number>();
  for (const signal of signals) {
    for (const tag of signal.tags) {
      counts.set(tag, (counts.get(tag) ?? 0) + 1);
    }
  }
  return Array.from(counts.entries())
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([tag]) => tag)
    .slice(0, 8);
}

function uniqueInOrder<T>(values: T[]): T[] {
  return Array.from(new Set(values));
}

export function getIntelligenceBoardData(): IntelligenceBoardData {
  const file = readJsonIfExists<IntelligenceSignalsFile>(
    join(intelligenceDir, "current", "signals.json"),
    { schema_version: "0.1", signals: [], updated_at: "" },
  );
  const competitors = getCompetitors();
  const signalsByProduct = new Map<string, IntelligenceSignal[]>();
  for (const signal of file.signals) {
    const current = signalsByProduct.get(signal.product_id) ?? [];
    current.push(signal);
    signalsByProduct.set(signal.product_id, current);
  }
  const battlecards: IntelligenceBattlecard[] = competitors
    .filter((competitor) => competitor.id !== "tachyon")
    .map((competitor) => {
      const signals = (signalsByProduct.get(competitor.id) ?? []).sort((a, b) =>
        a.category.localeCompare(b.category) || a.id.localeCompare(b.id),
      );
      const confidence: Partial<Record<IntelligenceConfidence, number>> = {};
      const freshness: Partial<Record<IntelligenceFreshness, number>> = {};
      for (const signal of signals) {
        increment(confidence, signal.confidence);
        increment(freshness, signal.freshness);
      }
      return {
        categories: uniqueInOrder(signals.map((signal) => signal.category)) as IntelligenceCategory[],
        class: competitor.class,
        confidence,
        freshness,
        homepage: competitor.homepage,
        id: competitor.id,
        name: competitor.name,
        objections: uniqueInOrder(signals.map((signal) => signal.objection).filter(Boolean) as string[]),
        positioning: competitor.research.positioning,
        readiness: competitor.research.benchmarking.readiness,
        responses: uniqueInOrder(signals.map((signal) => signal.tachyon_response)),
        signals,
        sourceCount: competitor.research.sources.length,
        sourceUrl: competitor.source_url,
        tags: topTags(signals),
      };
    })
    .sort((a, b) => b.signals.length - a.signals.length || a.name.localeCompare(b.name));
  return {
    battlecards,
    categoryCount: new Set(file.signals.map((signal) => signal.category)).size,
    generatedAt: file.updated_at || null,
    importReadyCount: file.signals.filter((signal) =>
      ["traffic", "seo", "paid_search", "backlink", "share_of_search"].includes(signal.category),
    ).length,
    pricingWatchCount: file.signals.filter((signal) =>
      signal.category === "pricing" || signal.category === "packaging",
    ).length,
    signalCount: file.signals.length,
  };
}
