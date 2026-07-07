export function url(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  if (path === "/") {
    return `${base}/`;
  }
  return `${base}${path}`;
}
