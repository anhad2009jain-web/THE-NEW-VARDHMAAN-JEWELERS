import { defineCollection, z } from 'astro:content';

// Every field below is editable through Pages CMS (.pages.yml → "Jewellery Products").
const products = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    productId: z.string(),
    category: z.string(), // slug of an entry in src/content/categories
    occasion: z.enum(['wedding', 'everyday', 'traditional', 'festive']).default('everyday'),
    metal: z.enum(['gold', 'diamond', 'silver', 'platinum', 'other']).default('gold'),
    purity: z.enum(['24K', '22K', '18K', '14K', '925 Silver', 'N/A']).default('22K'),
    grossWeight: z.number().nonnegative().default(0),
    netGoldWeight: z.number().nonnegative().default(0),
    stoneWeight: z.number().nonnegative().default(0),
    stonePrice: z.number().nonnegative().default(0),
    makingChargeType: z.enum(['fixed', 'per-gram', 'percent']).default('per-gram'),
    makingChargeValue: z.number().nonnegative().default(0),
    wastagePercent: z.number().nonnegative().default(0),
    otherCharges: z.number().nonnegative().default(0),
    priceOverride: z.number().nonnegative().nullable().default(null),
    bisHallmark: z.boolean().default(false),
    huid: z.string().default(''),
    hallmarkNote: z.string().default(''),
    availability: z.enum(['available', 'sold', 'made-to-order']).default('available'),
    featured: z.boolean().default(false),
    newArrival: z.boolean().default(false),
    bestseller: z.boolean().default(false),
    photos: z.array(z.string()).min(1),
    shortDescription: z.string().default(''),
   updatedAt: z.preprocess(
  (value) => value instanceof Date ? value.toISOString().slice(0, 10) : value,
  z.string().default('')
),
    demo: z.boolean().default(false),
  }),
});

// Jewellery categories / albums — editable under "Jewellery Categories".
const categories = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    group: z.enum(['gold', 'wedding', 'everyday', 'diamond', 'silver']),
    description: z.string().default(''),
    coverImage: z.string(),
    order: z.number().int().default(99),
    enabled: z.boolean().default(true),
  }),
});

// Customer testimonials — editable under "Customer Testimonials".
const testimonials = defineCollection({
  type: 'content',
  schema: z.object({
    customerName: z.string(),
    location: z.string().default(''),
    quote: z.string(),
    rating: z.number().int().min(1).max(5).default(5),
    order: z.number().int().default(99),
    published: z.boolean().default(true),
  }),
});

// Photo gallery albums — editable under "Gallery Management".
const albums = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    description: z.string().default(''),
    coverImage: z.string(),
    images: z.array(z.object({
      src: z.string(),
      caption: z.string().default(''),
    })),
    order: z.number().int().default(99),
    published: z.boolean().default(true),
    featuredOnHomepage: z.boolean().default(false),
  }),
});

// Customer reviews — editable under "Customer Reviews".
const reviews = defineCollection({
  type: 'content',
  schema: z.object({
    customerName: z.string(),
    location: z.string().default(''),
    rating: z.number().int().min(1).max(5).default(5),
    title: z.string().default(''),
    review: z.string(),
    productName: z.string().default(''),
    date: z.string().default(''),
    order: z.number().int().default(99),
    published: z.boolean().default(true),
  }),
});

export const collections = { products, categories, testimonials, albums, reviews };
