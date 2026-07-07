import { defineConfig } from "astro/config";
import react from "@astrojs/react";

export default defineConfig({
  site: "https://cfpperche.github.io",
  base: "/tachyon-ade-bench",
  output: "static",
  integrations: [react()],
});
