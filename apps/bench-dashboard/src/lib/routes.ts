import { localizedPath, type Locale } from "./i18n";

export function url(path: string, locale: Locale = "en"): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  const localized = localizedPath(path, locale);
  if (localized === "/") {
    return `${base}/`;
  }
  return `${base}${localized}`;
}
