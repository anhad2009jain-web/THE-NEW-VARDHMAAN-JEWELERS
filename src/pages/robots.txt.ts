export async function GET({ site }: { site: URL | undefined }) {
  const origin = site ? site.toString().replace(/\/$/, '') : '';
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const body = `User-agent: *
Allow: /

Sitemap: ${origin}${base}/sitemap-index.xml
`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain' } });
}
