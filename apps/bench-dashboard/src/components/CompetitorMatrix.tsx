import { useMemo, useState } from "react";
import { RotateCcw, Search } from "lucide-react";
import type { CompetitorSummary } from "../lib/types";
import type { Locale } from "../lib/i18n";

interface MatrixLabels {
  aria: string;
  search: string;
  searchPlaceholder: string;
  allClasses: string;
  allReadiness: string;
  openSourceVisible: string;
  resetFilters: string;
  showing: string;
  of: string;
  trackedProducts: string;
  product: string;
  class: string;
  readiness: string;
  stackSignals: string;
  stack: string;
  integrations: string;
  evidence: string;
  notMapped: string;
  source: string;
  sources: string;
  features: string;
  classA: string;
  classB: string;
  readinessLabels: Record<string, string>;
}

interface Props {
  competitors: CompetitorSummary[];
  baseUrl: string;
  locale: Locale;
  labels: MatrixLabels;
}

function productUrl(baseUrl: string, locale: Locale, id: string): string {
  const prefix = locale === "pt" ? "/pt" : "";
  return `${baseUrl.replace(/\/$/, "")}${prefix}/competitors/${id}/`;
}

function sourceCountLabel(count: number, labels: MatrixLabels): string {
  return count === 1 ? labels.source : labels.sources;
}

export default function CompetitorMatrix({ competitors, baseUrl, locale, labels }: Props) {
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
    <section className="matrix-app" aria-label={labels.aria}>
      <div className="matrix-toolbar">
        <label className="search-box">
          <Search aria-hidden="true" size={18} />
          <span className="sr-only">{labels.search}</span>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder={labels.searchPlaceholder}
          />
        </label>
        <label>
          <span>{labels.class}</span>
          <select value={klass} onChange={(event) => setKlass(event.target.value)}>
            {[
              ["all", labels.allClasses],
              ["A-local-ade", labels.classA],
              ["B-enterprise-agentic-platform", labels.classB],
            ].map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>
        <label>
          <span>{labels.readiness}</span>
          <select value={readiness} onChange={(event) => setReadiness(event.target.value)}>
            {[
              ["all", labels.allReadiness],
              ["manual-ready", labels.readinessLabels["manual-ready"]],
              ["needs-install", labels.readinessLabels["needs-install"]],
              ["enterprise-gated", labels.readinessLabels["enterprise-gated"]],
              ["owned-reference", labels.readinessLabels["owned-reference"]],
            ].map(([value, label]) => (
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
          <span>{labels.openSourceVisible}</span>
        </label>
        <button className="icon-button" type="button" onClick={reset} title={labels.resetFilters}>
          <RotateCcw aria-hidden="true" size={18} />
          <span className="sr-only">{labels.resetFilters}</span>
        </button>
      </div>

      <p className="matrix-count">
        {labels.showing} <strong>{filtered.length}</strong> {labels.of} {competitors.length}{" "}
        {labels.trackedProducts}
      </p>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>{labels.product}</th>
              <th>{labels.class}</th>
              <th>{labels.readiness}</th>
              <th>{labels.stackSignals}</th>
              <th>{labels.integrations}</th>
              <th>{labels.evidence}</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((competitor) => (
              <tr key={competitor.id}>
                <td>
                  <a className="link" href={productUrl(baseUrl, locale, competitor.id)}>
                    {competitor.name}
                  </a>
                  <small className="table-note">{competitor.license}</small>
                </td>
                <td>{competitor.class === "A-local-ade" ? labels.classA : labels.classB}</td>
                <td>
                  <span className={`badge badge--${competitor.readiness}`}>
                    {labels.readinessLabels[competitor.readiness]}
                  </span>
                </td>
                <td>{competitor.stack.slice(0, 5).join(", ")}</td>
                <td>{competitor.integrations.slice(0, 5).join(", ") || labels.notMapped}</td>
                <td>
                  {competitor.sourceCount} {sourceCountLabel(competitor.sourceCount, labels)}, {competitor.featureCount}{" "}
                  {labels.features}
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
              <a className="link" href={productUrl(baseUrl, locale, competitor.id)}>
                {competitor.name}
              </a>
              <small>{competitor.license}</small>
            </div>
            <div className="badge-row">
              <span className="badge">
                {competitor.class === "A-local-ade" ? labels.classA : labels.classB}
              </span>
              <span className={`badge badge--${competitor.readiness}`}>
                {labels.readinessLabels[competitor.readiness]}
              </span>
            </div>
            <dl>
              <div>
                <dt>{labels.stack}</dt>
                <dd>{competitor.stack.slice(0, 5).join(", ")}</dd>
              </div>
              <div>
                <dt>{labels.integrations}</dt>
                <dd>{competitor.integrations.slice(0, 5).join(", ") || labels.notMapped}</dd>
              </div>
              <div>
                <dt>{labels.evidence}</dt>
                <dd>
                  {competitor.sourceCount} {sourceCountLabel(competitor.sourceCount, labels)}, {competitor.featureCount}{" "}
                  {labels.features}
                </dd>
              </div>
            </dl>
          </article>
        ))}
      </div>
    </section>
  );
}
