import { useEffect, useRef } from "react";
import * as echarts from "echarts";
import type { CompetitorSummary } from "../lib/types";

interface Props {
  competitors: CompetitorSummary[];
}

function readinessColor(value: string): string {
  const colors: Record<string, string> = {
    "manual-ready": "#2f6f3e",
    "needs-install": "#9a6500",
    "enterprise-gated": "#2457c5",
    "owned-reference": "#05746f",
    "research-only": "#5d6872",
  };
  return colors[value] ?? "#5d6872";
}

export default function DashboardCharts({ competitors }: Props) {
  const readinessRef = useRef<HTMLDivElement | null>(null);
  const moatRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!readinessRef.current || !moatRef.current) return;
    const readinessChart = echarts.init(readinessRef.current, undefined, {
      renderer: "svg",
    });
    const moatChart = echarts.init(moatRef.current, undefined, {
      renderer: "svg",
    });
    const readinessCounts = competitors.reduce<Record<string, number>>((counts, competitor) => {
      counts[competitor.readiness] = (counts[competitor.readiness] ?? 0) + 1;
      return counts;
    }, {});
    const readinessData = Object.entries(readinessCounts).map(([name, value]) => ({
      name,
      value,
      itemStyle: { color: readinessColor(name) },
    }));

    readinessChart.setOption({
      tooltip: { trigger: "item" },
      legend: { bottom: 0, left: "center", itemWidth: 12, itemHeight: 12 },
      series: [
        {
          name: "Benchmark readiness",
          type: "pie",
          radius: ["42%", "68%"],
          center: ["50%", "43%"],
          avoidLabelOverlap: true,
          label: { show: false },
          data: readinessData,
        },
      ],
    });

    moatChart.setOption({
      grid: { top: 24, right: 28, bottom: 48, left: 52 },
      tooltip: {
        formatter: (params: any) => {
          const data = params.data;
          return `${data.name}<br/>Local-first: ${data.value[0]}<br/>Orchestration: ${data.value[1]}<br/>Features: ${data.value[2]}`;
        },
      },
      xAxis: {
        name: "Local-first",
        min: 0,
        max: 100,
        splitLine: { lineStyle: { color: "#e6edf2" } },
      },
      yAxis: {
        name: "Orchestration depth",
        min: 0,
        max: 100,
        splitLine: { lineStyle: { color: "#e6edf2" } },
      },
      series: [
        {
          type: "scatter",
          symbolSize: (value: number[]) => Math.max(16, Math.min(46, value[2] * 1.4)),
          data: competitors.map((competitor) => ({
            name: competitor.name,
            value: [
              competitor.localScore,
              competitor.orchestrationScore,
              competitor.featureCount,
            ],
            itemStyle: {
              color:
                competitor.class === "B-enterprise-agentic-platform"
                  ? "#2457c5"
                  : competitor.id === "tachyon"
                    ? "#05746f"
                    : "#9a6500",
              opacity: 0.86,
            },
          })),
          label: {
            show: false,
            formatter: "{b}",
            position: "right",
            color: "#172026",
            fontSize: 11,
            overflow: "truncate",
            width: 92,
          },
          emphasis: {
            label: {
              show: true,
              fontWeight: 700,
              color: "#172026",
            },
          },
        },
      ],
    });

    const resize = () => {
      readinessChart.resize();
      moatChart.resize();
    };
    window.addEventListener("resize", resize);
    return () => {
      window.removeEventListener("resize", resize);
      readinessChart.dispose();
      moatChart.dispose();
    };
  }, [competitors]);

  return (
    <div className="charts-grid" aria-label="Competitor charts">
      <section className="panel">
        <div className="panel__head">
          <div>
            <h2>Benchmark Readiness</h2>
            <p>Profiles are grouped by how close they are to a comparable benchmark run.</p>
          </div>
        </div>
        <div className="panel__body">
          <div ref={readinessRef} className="chart-surface" />
        </div>
      </section>
      <section className="panel">
        <div className="panel__head">
          <div>
            <h2>Moat Map</h2>
            <p>Derived positioning map from local-first and orchestration signals in the profiles.</p>
          </div>
        </div>
        <div className="panel__body">
          <div ref={moatRef} className="chart-surface" />
        </div>
      </section>
    </div>
  );
}
