import { getProducts, resolveCategory } from '../lib/content';
import { formatWeight } from '../lib/format';
import { href, asset } from '../lib/urls';

export async function GET() {
  const products = await getProducts();
  const index = [];

  for (const p of products) {
    const d = p.data;
    const category = await resolveCategory(d.category);

    index.push({
      name: d.name,
      url: href(`/product/${p.slug}`),
      image: asset(d.photos[0]),
      purity: d.purity,
      weight: d.netGoldWeight > 0 ? formatWeight(d.netGoldWeight) : '',
      category: category?.data.name || '',
      haystack: [
        d.name,
        d.productId,
        d.purity,
        d.metal,
        category?.data.name || '',
        d.shortDescription
      ]
        .join(' ')
        .toLowerCase(),
    });
  }

  return new Response(JSON.stringify(index), {
    headers: { 'Content-Type': 'application/json' },
  });
}
