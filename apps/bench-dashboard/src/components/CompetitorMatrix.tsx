import { useMemo, useState } from "react";
import { RotateCcw, Search } from "lucide-react";
import type { CompetitorSummary } from "../lib/types";

interface Props {
  competitors: CompetitorSummary[];
  baseUrl: string;
}

const classOptions = [
  ["all", "All classes"],
  ["A-local-ade", "Class A"],
  ["B-enterprise-agentic-platform", "Class B"],
];

const readinessOptions = [
  ["all", "All readiness"],
  ["manual-ready", "Manual ready"],
  ["needs-install", "Needs install"],
  ["enterprise-gated", "Enterprise gated"],
  ["owned-reference", "Owned reference"],
];

function badgeLabel(value: string): string {
  return value
    .replace(/-/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase())
    .replace(/\bAde\b/g, "ADE");
}

function productUrl(baseUrl: string, id: string): string {
  return `${baseUrl.replace(/\/$/, "")}/competitors/${id}/`;
}

export default function CompetitorMatrix({ competitors, baseUrl }: Props) {
  const [query, setQuery] = useState("");
  const [klass, setKlass] = useState("all");
  const [readiness, setReadiness] = useState("all");
  const [opensourceOnly, setOpenSourceOnly] = useState(false);

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return competitors.filter((competitor) => {
      const searchable = [
        competitor.name,
        competitor.positioning,
        competitor.license,
        competitor.readiness,
        competitor.class,
        ...competitor.stack,
        ...competitor.integrations,
      ]
        .join(" ")
        .toLowerCase();
      const matchesQuery = needle.length === 0 || searchable.includes(needle);
      const matchesClass = klass === "all" || competitor.class === klass;
      const matchesReadiness = readiness === "all" || competitor.readiness === readiness;
      const matchesSource =
        !opensourceOnly ||
        /mit|agpl|busl|open|source/i.test(competitor.license) ||
        competitor.sourceUrl !== null;
      return matchesQuery && matchesClass && matchesReadiness && matchesSource;
    });
  }, [competitors, klass, opensourceOnly, query, readiness]);

  const reset = () => {
    setQuery("");
    setKlass("all");
    setReadiness("all");
    setOpenSourceOnly(false);
  };

  return (
    <section className="matrix-app" aria-label="Competitor matrix">
      <div className="matrix-toolbar">
        <label className="search-box">
          <Search aria-hidden="true" size={18} />
          <span className="sr-only">Search competitors</span>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search stack, integrations, moat..."
          />
        </label>
        <label>
          <span>Class</span>
          <select value={klass} onChange={(event) => setKlass(event.target.value)}>
            {classOptions.map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>
        <label>
          <span>Readiness</span>
          <select value={readiness} onChange={(event) => setReadiness(event.target.value)}>
            {readinessOptions.map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>
        <label className="toggle">
          <input
            type="checkbox"
            checked={opensourceOnly}
            onChange={(event) => setOpenSourceOnly(event.target.checked)}
          />
          <span>Open/source-visible</span>
        </label>
        <button className="icon-button" type="button" onClick={reset} title="Reset filters">
          <RotateCcw aria-hidden="true" size={18} />
          <span className="sr-only">Reset filters</span>
        </button>
      </div>

      <p className="matrix-count">
        Showing <strong>{filtered.length}</strong> of {competitors.length} tracked products.
      </p>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Class</th>
              <th>Readiness</th>
              <th>Stack signals</th>
              <th>Integrations</th>
              <th>Evidence</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((competitor) => (
              <tr key={competitor.id}>
                <td>
                  <a className="link" href={productUrl(baseUrl, competitor.id)}>
                    {competitor.name}
                  </a>
                  <small className="table-note">{competitor.license}</small>
                </td>
                <td>{competitor.class === "A-local-ade" ? "Class A" : "Class B"}</td>
                <td>
                  <span className={`badge badge--${competitor.readiness}`}>
                    {badgeLabel(competitor.readiness)}
                  </span>
                </td>
                <td>{competitor.stack.slice(0, 5).join(", ")}</td>
                <td>{competitor.integrations.slice(0, 5).join(", ") || "Not mapped"}</td>
                <td>
                  {competitor.sourceCount} sources, {competitor.featureCount} features
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="matrix-mobile-list" aria-label="Mobile competitor matrix">
        {filtered.map((competitor) => (
          <article className="matrix-mobile-card" key={competitor.id}>
            <div>
              <a className="link" href={productUrl(baseUrl, competitor.id)}>
                {competitor.name}
              </a>
              <small>{competitor.license}</small>
            </div>
            <div className="badge-row">
              <span className="badge">
                {competitor.class === "A-local-ade" ? "Class A" : "Class B"}
              </span>
              <span className={`badge badge--${competitor.readiness}`}>
                {badgeLabel(competitor.readiness)}
              </span>
            </div>
            <dl>
              <div>
                <dt>Stack</dt>
                <dd>{competitor.stack.slice(0, 5).join(", ")}</dd>
              </div>
              <div>
                <dt>Integrations</dt>
                <dd>{competitor.integrations.slice(0, 5).join(", ") || "Not mapped"}</dd>
              </div>
              <div>
                <dt>Evidence</dt>
                <dd>
                  {competitor.sourceCount} sources, {competitor.featureCount} features
                </dd>
              </div>
            </dl>
          </article>
        ))}
      </div>
    </section>
  );
}
