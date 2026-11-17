// URL helpers — every internal link and CMS-managed asset path must pass
// through these so the site works under a GitHub Pages repository base path.

const base = import.meta.env.BASE_URL.replace(/\/$/, '');

/** Internal site link, e.g. href('/collections') → '/collections.html' */
export function href(path: string): string {
  if (!path || path === '/') return base + '/';
  if (/^https?:\/\//i.test(path) || path.startsWith('mailto:') || path.startsWith('tel:')) return path;
  const clean = path.replace(/^\//, '');
  const lastSegment = clean.split('/').pop() || '';
  // Files with an extension (assets, .json, .txt, .xml) are referenced as-is;
  // extensionless page routes get .html to match build.format = 'file'.
  const suffix = lastSegment.includes('.') ? '' : '.html';
  return base + '/' + clean + suffix;
}

/** CMS-uploaded asset (e.g. "/uploads/products/ring.jpg" stored by Pages CMS) */
export function asset(path: string): string {
  if (!path) return '';
  if (/^https?:\/\//i.test(path)) return path;
  return base + '/' + path.replace(/^\//, '');
}

export { base };
