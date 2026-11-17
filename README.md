# Vardhman Jewellers — Website

Luxury jewellery website for **Vardhman Jewellers, Talab Tillo, Jammu**, built with
[Astro](https://astro.build) (static site), managed entirely through
[Pages CMS](https://pagescms.org) and deployed automatically to **GitHub Pages**.

> The sample products, photographs, rates and business details currently in the
> repository are **demonstration content**. Replace them with real content through
> Pages CMS before going live (see `OWNER_GUIDE.md`).

---

## How it works

```
Pages CMS (app.pagescms.org)
        │  owner edits content → commits to GitHub
        ▼
GitHub repository (this repo)
        │  push to main triggers
        ▼
GitHub Actions (.github/workflows/deploy.yml)
        │  npm ci → astro build → deploy
        ▼
GitHub Pages (live website)
```

**No database, no server, no paid backend.** Every piece of content lives in files
inside this repository and is editable through Pages CMS.

## Where content lives

| Content | File(s) | Pages CMS section |
|---|---|---|
| Business name, address, phones, WhatsApp, social, hours, About Us, logo, favicon, footer, jewellery section names | `src/data/site.json` | **Business Information** |
| Homepage banner, promo text, section visibility, featured products, SEO | `src/data/homepage.json` | **Homepage Content** |
| Daily gold rates (24K/22K/18K/14K/silver), tax, disclaimer | `src/data/gold-rates.json` | **Daily Gold Rates** |
| Products (name, photos, weights, purity, making charges, HUID, price, availability) | `src/content/products/*.md` | **Jewellery Products** |
| Jewellery categories / albums (name, cover, order, enable/disable) | `src/content/categories/*.md` | **Jewellery Categories** |
| Photo gallery albums (create, upload, reorder, publish/hide, feature) | `src/content/albums/*.md` | **Gallery Management** |
| Customer testimonials | `src/content/testimonials/*.md` | **Customer Testimonials** |
| Customer reviews (rating, title, product, date) | `src/content/reviews/*.md` | **Customer Reviews** |
| Uploaded photographs | `public/uploads/**` | Media library |

The CMS dashboard layout is defined by **`.pages.yml`** in the repository root.

## Gold price calculator

`src/lib/pricing.ts` computes every product's estimated price at build time:

```
Gold value   = net gold weight × applicable CMS gold rate (₹/g of its purity)
Making       = fixed ₹ | ₹/g (on gross weight) | % of gold value
Subtotal     = gold value + making + stone + wastage + other charges
Total        = subtotal + configurable tax %
```

- Rates come only from `gold-rates.json` — **never hardcoded, never invented**.
- If a rate is missing, zero, or older than `maxRateAgeHours`, products show
  **"Price on Request"**.
- `priceOverride` on a product always wins.
- Calculations use integer-paise arithmetic to avoid floating-point errors.

## Local development

```bash
npm install
npm run dev        # http://localhost:4321 (passes --host/--port through to Astro)
npm run build      # outputs static site to dist/
npm run preview    # preview the production build
```

## Deployment (one-time setup)

1. Push this repository to GitHub.
2. In the repository: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Push any commit to `main` (or save anything in Pages CMS) — the
   `Deploy website to GitHub Pages` workflow builds and publishes the site.
4. The site works automatically under a repository base path
   (`https://<user>.github.io/<repo>/`) — the workflow injects `SITE_URL` and
   `BASE_PATH` from `actions/configure-pages`.
5. Open **https://app.pagescms.org**, sign in with GitHub, install the Pages CMS
   GitHub App on the repository, and start editing.

## Editing content

See **`OWNER_GUIDE.md`** — written for the shop owner, no technical knowledge needed.

## Project structure

```
.pages.yml                  Pages CMS dashboard configuration
.github/workflows/deploy.yml  GitHub Pages deployment
public/uploads/             CMS-uploaded media
src/
  data/site.json            Business Information
  data/homepage.json        Homepage content
  data/gold-rates.json      Daily gold rates + tax
  content/products/         Jewellery products (Markdown + frontmatter)
  content/categories/       Jewellery categories
  content/albums/           Gallery albums
  content/testimonials/     Testimonials
  lib/pricing.ts            Gold price calculator
  lib/urls.ts               Base-path-safe URL helpers
  pages/                    Home, collections, category, product, gallery, about, contact, search
```
