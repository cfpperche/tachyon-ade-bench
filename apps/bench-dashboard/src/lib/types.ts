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
