export type ProductClass = "A-local-ade" | "B-enterprise-agentic-platform";

export type BenchmarkReadiness =
  | "manual-ready"
  | "needs-install"
  | "enterprise-gated"
  | "owned-reference"
  | "research-only";

export type ResearchConfidence =
  | "owned"
  | "official-sourced"
  | "partial-official"
  | "seed";

export interface ResearchSource {
  url: string;
  kind: string;
  notes: string;
}

export interface CompetitorResearch {
  last_reviewed: string;
  confidence: ResearchConfidence;
  sources: ResearchSource[];
  positioning: string;
  stack: {
    runtime: string[];
    frontend: string[];
    backend: string[];
    packaging: string[];
    data: string[];
    unknowns: string[];
  };
  infrastructure: string[];
  features: {
    agent_support: string[];
    orchestration: string[];
    workspace_isolation: string[];
    review_shipping: string[];
    remote_mobile: string[];
    context_memory: string[];
    integrations: string[];
  };
  benchmarking: {
    readiness: BenchmarkReadiness;
    install_surface: string[];
    parity_risks: string[];
    suggested_first_tasks: string[];
  };
  moat: {
    hypotheses: string[];
    evidence: string[];
    unknowns: string[];
  };
}

export interface Competitor {
  id: string;
  name: string;
  class: ProductClass;
  homepage: string | null;
  source_url: string | null;
  license: string;
  runner: {
    kind: "manual" | "cli" | "api";
    notes: string;
  };
  inclusion: string;
  pricing_model?: string;
  public_stack_signals?: string[];
  capabilities_to_probe?: string[];
  moat_hypotheses?: string[];
  setup_notes?: string[];
  research: CompetitorResearch;
  research_status: string;
  updated_at: string;
}

export interface TaskMeta {
  id: string;
  title: string;
  category: string;
  difficulty: string;
}

export interface CompetitorSummary {
  id: string;
  name: string;
  class: ProductClass;
  license: string;
  sourceUrl: string | null;
  homepage: string | null;
  positioning: string;
  readiness: BenchmarkReadiness;
  confidence: ResearchConfidence;
  sourceCount: number;
  featureCount: number;
  taskCount: number;
  localScore: number;
  orchestrationScore: number;
  stack: string[];
  integrations: string[];
  suggestedTasks: string[];
}

export type AcquisitionResult = "found" | "not-found" | "partial" | "blocked";

export interface MarketingAdEvent {
  ad_fingerprint: string;
  advertiser_name: string;
  body: string | null;
  claims: string[];
  countries: string[];
  creative_hash: string | null;
  creative_type: string;
  creative_url: string | null;
  cta: string | null;
  event_type: string;
  headline: string | null;
  landing_domain: string | null;
  landing_url: string | null;
  notes: string | null;
  observed_at: string;
  platform: string;
  platform_ad_id: string | null;
  positioning_tags: string[];
  product_id: string;
  raw_ref: string;
  scan_id: string;
  source_url: string;
  status: string;
}

export interface MarketingCurrentAd {
  ad_fingerprint: string;
  advertiser_name: string;
  first_seen: string;
  last_seen: string;
  latest: MarketingAdEvent;
  platform: string;
  platform_ad_id: string | null;
  product_id: string;
  seen_count: number;
  status: string;
}

export interface MarketingCampaign {
  ad_count: number;
  first_seen: string;
  last_seen: string;
  platform: string;
  positioning_tags: string[];
  product_id: string;
}

export interface MarketingManifestQuery {
  country: string | null;
  method: string;
  platform: string;
  product_id: string;
  query: string;
  result: AcquisitionResult;
  source_url: string;
}

export interface MarketingManifest {
  completed_at?: string;
  git_commit: string;
  limitations: string[];
  queries: MarketingManifestQuery[];
  scan_id: string;
  schema_version: string;
  started_at: string;
  tool_version: string;
}

export interface AcquisitionCoverageRow extends MarketingManifestQuery {
  product_name: string;
  scan_id: string;
}

export interface AcquisitionAdRow extends MarketingCurrentAd {
  product_name: string;
  evidence_refs: string[];
}

export interface AcquisitionCampaignRow extends MarketingCampaign {
  product_name: string;
}

export interface AcquisitionBoardData {
  ads: AcquisitionAdRow[];
  campaigns: AcquisitionCampaignRow[];
  coverageRows: AcquisitionCoverageRow[];
  generatedAt: string | null;
  latestScan: MarketingManifest | null;
  manifests: MarketingManifest[];
  platformCount: number;
  queryCount: number;
  scanCount: number;
  statusCounts: Partial<Record<AcquisitionResult, number>>;
}
