import { useEffect, useMemo, useRef, useState } from "react";
import * as echarts from "echarts";
import type { CapabilityAxis, CompetitorSummary } from "../lib/types";
import { CAPABILITY_AXES } from "../lib/types";

interface Props {
  competitors: CompetitorSummary[];
  labels: {
    aria: string;
    readinessTitle: string;
    readinessDescription: string;
    readinessCalcTitle: string;
    readinessCalc: readonly string[];
    positioningTitle: string;
    positioningDescription: string;
    positioningCalcTitle: string;
    positioningCalc: readonly string[];
    capabilityTitle: string;
    capabilityDescription: string;
    capabilityDisclaimer: string;
    capabilityCalcTitle: string;
    capabilityCalc: readonly string[];
    compareProducts: string;
    resetDefaults: string;
    localFirst: string;
    orchestrationDepth: string;
    features: string;
    readinessLabels: Record<string, string>;
    capabilityAxes: Record<CapabilityAxis, string>;
  };
}

function ChartCalcNote({
  title,
  items,
}: {
  title: string;
  items: readonly string[];
}) {
  return (
    <details className="chart-calc">
      <summary className="chart-calc__summary">{title}</summary>
      <ul className="chart-calc__list">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </details>
  );
}

const SERIES_COLORS = [
  "#05746f",
  "#9a6500",
  "#2457c5",
  "#8b3a62",
  "#2f6f3e",
  "#6b4c9a",
  "#c45c26",
  "#3d5a80",
  "#b45309",
  "#0f766e",
];

const DEFAULT_IDS = ["tachyon", "orca", "fusion"];

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

function colorForId(id: string, index: number): string {
  if (id === "tachyon") return "#05746f";
  if (id === "orca") return "#9a6500";
  if (id === "fusion") return "#c45c26";
  if (id === "augment-code") return "#2457c5";
  return SERIES_COLORS[index % SERIES_COLORS.length];
}

function defaultSelection(competitors: CompetitorSummary[]): string[] {
  const available = new Set(competitors.map((c) => c.id));
  const preferred = DEFAULT_IDS.filter((id) => available.has(id));
  if (preferred.length >= 2) return preferred.slice(0, 3);
  const fillers = competitors
    .filter((c) => c.class === "A-local-ade" && !preferred.includes(c.id))
    .map((c) => c.id);
  return [...preferred, ...fillers].slice(0, 3);
}

export default function DashboardCharts({ competitors, labels }: Props) {
  const readinessRef = useRef<HTMLDivElement | null>(null);
  const positioningRef = useRef<HTMLDivElement | null>(null);
  const radarRef = useRef<HTMLDivElement | null>(null);
  const [selectedIds, setSelectedIds] = useState<string[]>(() =>
    defaultSelection(competitors),
  );

  const selected = useMemo(
    () => competitors.filter((c) => selectedIds.includes(c.id)),
    [competitors, selectedIds],
  );

  const colorById = useMemo(() => {
    const map = new Map<string, string>();
    competitors.forEach((c, index) => {
      map.set(c.id, colorForId(c.id, index));
    });
    return map;
  }, [competitors]);

  useEffect(() => {
    // Drop stale ids if the roster changes.
    setSelectedIds((current) => {
      const available = new Set(competitors.map((c) => c.id));
      const next = current.filter((id) => available.has(id));
      return next.length > 0 ? next : defaultSelection(competitors);
    });
  }, [competitors]);

  useEffect(() => {
    if (!readinessRef.current || !positioningRef.current) return;
    const readinessChart = echarts.init(readinessRef.current, undefined, {
      renderer: "svg",
    });
    const positioningChart = echarts.init(positioningRef.current, undefined, {
      renderer: "svg",
    });

    const readinessCounts = competitors.reduce<Record<string, number>>((counts, competitor) => {
      counts[competitor.readiness] = (counts[competitor.readiness] ?? 0) + 1;
      return counts;
    }, {});
    const readinessData = Object.entries(readinessCounts).map(([name, value]) => ({
      name: labels.readinessLabels[name] ?? name,
      value,
      itemStyle: { color: readinessColor(name) },
    }));

    readinessChart.setOption({
      tooltip: { trigger: "item" },
      legend: { bottom: 0, left: "center", itemWidth: 12, itemHeight: 12 },
      series: [
        {
          name: labels.readinessTitle,
          type: "pie",
          radius: ["42%", "68%"],
          center: ["50%", "43%"],
          avoidLabelOverlap: true,
          label: { show: false },
          data: readinessData,
        },
      ],
    });

    positioningChart.setOption({
      grid: { top: 24, right: 28, bottom: 48, left: 52 },
      tooltip: {
        formatter: (params: { data: { name: string; value: number[] } }) => {
          const data = params.data;
          return `${data.name}<br/>${labels.localFirst}: ${data.value[0]}<br/>${labels.orchestrationDepth}: ${data.value[1]}<br/>${labels.features}: ${data.value[2]}`;
        },
      },
      xAxis: {
        name: labels.localFirst,
        min: 0,
        max: 100,
        splitLine: { lineStyle: { color: "#e6edf2" } },
      },
      yAxis: {
        name: labels.orchestrationDepth,
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
      positioningChart.resize();
    };
    window.addEventListener("resize", resize);
    return () => {
      window.removeEventListener("resize", resize);
      readinessChart.dispose();
      positioningChart.dispose();
    };
  }, [competitors, labels]);

  useEffect(() => {
    if (!radarRef.current) return;
    const radarChart = echarts.init(radarRef.current, undefined, {
      renderer: "svg",
    });

    const indicators = CAPABILITY_AXES.map((axis) => ({
      name: labels.capabilityAxes[axis],
      max: 100,
    }));

    radarChart.setOption({
      color: selected.map((c) => colorById.get(c.id) ?? "#5d6872"),
      legend: {
        bottom: 0,
        left: "center",
        itemWidth: 12,
        itemHeight: 12,
        data: selected.map((c) => c.name),
      },
      tooltip: {
        trigger: "item",
      },
      radar: {
        center: ["50%", "46%"],
        radius: "62%",
        indicator: indicators,
        splitNumber: 4,
        axisName: {
          color: "#3d4a54",
          fontSize: 11,
          fontWeight: 600,
        },
        splitLine: {
          lineStyle: { color: "#d8e2ea" },
        },
        splitArea: {
          areaStyle: {
            color: ["rgba(246,249,251,0.9)", "rgba(236,242,247,0.55)"],
          },
        },
        axisLine: {
          lineStyle: { color: "#c5d2dc" },
        },
      },
      series: [
        {
          type: "radar",
          emphasis: {
            lineStyle: { width: 3 },
          },
          data:
            selected.length === 0
              ? []
              : selected.map((competitor) => ({
                  name: competitor.name,
                  value: CAPABILITY_AXES.map(
                    (axis) => competitor.capabilityScores[axis],
                  ),
                  areaStyle: { opacity: selected.length === 1 ? 0.32 : 0.14 },
                  lineStyle: { width: 2 },
                  symbol: "circle",
                  symbolSize: 5,
                })),
        },
      ],
    });

    const resize = () => radarChart.resize();
    window.addEventListener("resize", resize);
    return () => {
      window.removeEventListener("resize", resize);
      radarChart.dispose();
    };
  }, [selected, labels, colorById]);

  function toggleProduct(id: string) {
    setSelectedIds((current) => {
      if (current.includes(id)) {
        if (current.length === 1) return current;
        return current.filter((value) => value !== id);
      }
      return [...current, id];
    });
  }

  function resetDefaults() {
    setSelectedIds(defaultSelection(competitors));
  }

  return (
    <div className="charts-stack" aria-label={labels.aria}>
      <div className="charts-grid">
        <section className="panel">
          <div className="panel__head">
            <div>
              <h2>{labels.readinessTitle}</h2>
              <p>{labels.readinessDescription}</p>
            </div>
          </div>
          <div className="panel__body">
            <ChartCalcNote
              title={labels.readinessCalcTitle}
              items={labels.readinessCalc}
            />
            <div ref={readinessRef} className="chart-surface" />
          </div>
        </section>
        <section className="panel">
          <div className="panel__head">
            <div>
              <h2>{labels.positioningTitle}</h2>
              <p>{labels.positioningDescription}</p>
            </div>
          </div>
          <div className="panel__body">
            <ChartCalcNote
              title={labels.positioningCalcTitle}
              items={labels.positioningCalc}
            />
            <div ref={positioningRef} className="chart-surface" />
          </div>
        </section>
      </div>

      <section className="panel charts-radar">
        <div className="panel__head">
          <div>
            <h2>{labels.capabilityTitle}</h2>
            <p>{labels.capabilityDescription}</p>
          </div>
          <button type="button" className="radar-reset" onClick={resetDefaults}>
            {labels.resetDefaults}
          </button>
        </div>
        <div className="panel__body">
          <div className="radar-toolbar">
            <span className="radar-toolbar__label">{labels.compareProducts}</span>
            <div className="radar-toggles" role="group" aria-label={labels.compareProducts}>
              {competitors.map((competitor) => {
                const active = selectedIds.includes(competitor.id);
                const color = colorById.get(competitor.id) ?? "#5d6872";
                return (
                  <button
                    key={competitor.id}
                    type="button"
                    className={`radar-toggle${active ? " is-active" : ""}`}
                    aria-pressed={active}
                    onClick={() => toggleProduct(competitor.id)}
                    style={
                      active
                        ? {
                            borderColor: color,
                            background: `${color}18`,
                            color: "#172026",
                          }
                        : undefined
                    }
                  >
                    <span
                      className="radar-toggle__swatch"
                      style={{ background: active ? color : "#c5d2dc" }}
                    />
                    {competitor.name}
                  </button>
                );
              })}
            </div>
          </div>
          <p className="radar-disclaimer">{labels.capabilityDisclaimer}</p>
          <ChartCalcNote
            title={labels.capabilityCalcTitle}
            items={labels.capabilityCalc}
          />
          <div ref={radarRef} className="chart-surface chart-surface--radar" />
        </div>
      </section>
    </div>
  );
}
