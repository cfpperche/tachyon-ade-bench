import { getUi, type Locale } from "./i18n";

export function label(value: string, locale: Locale = "en"): string {
  const translated = (getUi(locale).labels as Record<string, string>)[value];
  if (translated) {
    return translated;
  }
  return value
    .replace(/-/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase())
    .replace(/\bAde\b/g, "ADE");
}

export function readinessLabel(value: string, locale: Locale = "en"): string {
  return label(value, locale);
}

export function classLabel(value: string, locale: Locale = "en"): string {
  return label(value, locale);
}
