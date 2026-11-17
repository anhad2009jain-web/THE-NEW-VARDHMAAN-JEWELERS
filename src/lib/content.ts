import { getCollection, type CollectionEntry } from 'astro:content';

export type Product = CollectionEntry<'products'>;
export type Category = CollectionEntry<'categories'>;
export type Testimonial = CollectionEntry<'testimonials'>;
export type Album = CollectionEntry<'albums'>;

let _categories: Category[] | null = null;

/** All categories sorted by display order (enabled only by default). */
export async function getCategories(enabledOnly = true): Promise<Category[]> {
  if (!_categories) {
    _categories = await getCollection('categories');
  }
  return _categories
    .filter((c) => (enabledOnly ? c.data.enabled : true))
    .sort((a, b) => a.data.order - b.data.order);
}

/**
 * Resolve a product's category reference. Pages CMS may store either the
 * file slug ("gold-rings") or the display name ("Gold Rings") — accept both.
 */
export async function resolveCategory(ref: string): Promise<Category | undefined> {
  const cats = await getCategories(false);
  const norm = (s: string) => s.trim().toLowerCase();
  const asSlug = (s: string) => norm(s).replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  return (
    cats.find((c) => c.slug === ref) ||
    cats.find((c) => norm(c.data.name) === norm(ref)) ||
    cats.find((c) => asSlug(c.data.name) === asSlug(ref))
  );
}

export async function getProducts(): Promise<Product[]> {
  return await getCollection('products');
}

export async function getTestimonials(): Promise<Testimonial[]> {
  const all = await getCollection('testimonials');
  return all.filter((t) => t.data.published).sort((a, b) => a.data.order - b.data.order);
}

export async function getAlbums(): Promise<Album[]> {
  const all = await getCollection('albums');
  return all.filter((a) => a.data.published).sort((a, b) => a.data.order - b.data.order);
}

export type Review = CollectionEntry<'reviews'>;

export async function getReviews(): Promise<Review[]> {
  const all = await getCollection('reviews');
  return all.filter((r) => r.data.published).sort((a, b) => a.data.order - b.data.order);
}
