import { useEffect, useId, useRef } from "react";
import mermaid from "mermaid";

interface Props {
  labels: {
    competitorJson: string;
    dashboardBuild: string;
    taskMetadata: string;
    pagesSite: string;
    overviewCharts: string;
    matrixFilters: string;
    competitorDetail: string;
    benchmarkProtocol: string;
    prepareRun: string;
    productUnderTest: string;
    verifyCanonical: string;
    artifactsReport: string;
  };
}

function diagram(labels: Props["labels"]) {
  return `flowchart LR
  A[${labels.competitorJson}] --> B[${labels.dashboardBuild}]
  T[${labels.taskMetadata}] --> B
  B --> C[${labels.pagesSite}]
  C --> D[${labels.overviewCharts}]
  C --> E[${labels.matrixFilters}]
  C --> F[${labels.competitorDetail}]
  P[${labels.benchmarkProtocol}] --> R[${labels.prepareRun}]
  R --> U[${labels.productUnderTest}]
  U --> V[${labels.verifyCanonical}]
  V --> O[${labels.artifactsReport}]
`;
}

export default function ProtocolDiagram({ labels }: Props) {
  const id = useId().replace(/:/g, "");
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    mermaid.initialize({
      startOnLoad: false,
      theme: "base",
      themeVariables: {
        primaryColor: "#d8f0ed",
        primaryTextColor: "#172026",
        primaryBorderColor: "#05746f",
        lineColor: "#5d6872",
        secondaryColor: "#dfe8ff",
        tertiaryColor: "#fff0cc",
        fontFamily: "Inter, system-ui, sans-serif",
      },
    });
    mermaid.render(`bench-protocol-${id}`, diagram(labels)).then(({ svg }) => {
      if (ref.current) {
        ref.current.innerHTML = svg;
      }
    });
  }, [id, labels]);

  return <div ref={ref} className="protocol-diagram" aria-label={labels.benchmarkProtocol} />;
}
