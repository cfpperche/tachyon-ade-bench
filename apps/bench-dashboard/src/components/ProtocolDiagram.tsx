import { useEffect, useId, useRef } from "react";
import mermaid from "mermaid";

const diagram = `flowchart LR
  A[Competitor JSON] --> B[Dashboard build]
  T[Task metadata] --> B
  B --> C[Static GitHub Pages site]
  C --> D[Overview and charts]
  C --> E[Matrix and filters]
  C --> F[Competitor detail]
  P[Benchmark protocol] --> R[prepare run]
  R --> U[product under test]
  U --> V[verify from canonical task]
  V --> O[artifacts and report]
`;

export default function ProtocolDiagram() {
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
    mermaid.render(`bench-protocol-${id}`, diagram).then(({ svg }) => {
      if (ref.current) {
        ref.current.innerHTML = svg;
      }
    });
  }, [id]);

  return <div ref={ref} className="protocol-diagram" aria-label="Benchmark protocol diagram" />;
}
