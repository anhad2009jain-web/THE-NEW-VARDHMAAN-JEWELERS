// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// SITE_URL and BASE_PATH are injected by the GitHub Actions workflow
// (actions/configure-pages) so the site works under a repository base path.
// For local development the defaults below are used.
export default defineConfig({
  site: process.env.SITE_URL || 'http://localhost:4321',
  base: process.env.BASE_PATH || '/',
  output: 'static',
  trailingSlash: 'ignore',
  // Emit /page.html instead of /page/index.html so the site also works on
  // static hosts that do not resolve directory index files (e.g. kimi.page).
  build: {
    format: 'file',
  },
  integrations: [sitemap()],
});
