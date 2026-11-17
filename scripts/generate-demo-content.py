"""Generate elegant labelled demo SVG placeholders and CMS demo content files."""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))

PALETTES = {
    "gold":    ("#E9DFCF", "#B69A62", "#171615"),
    "wedding": ("#F1E4D3", "#B08D57", "#171615"),
    "everyday":("#F8F5EF", "#B69A62", "#171615"),
    "diamond": ("#EFEDE8", "#9A9184", "#171615"),
    "silver":  ("#EFF0F2", "#8E9299", "#171615"),
    "brand":   ("#171615", "#B69A62", "#F8F5EF"),
}

def svg(path, label, sub, theme="gold", w=1200, h=1200):
    bg, accent, fg = PALETTES.get(theme, PALETTES["gold"])
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="{bg}"/>
  <rect x="{w*0.06:.0f}" y="{h*0.06:.0f}" width="{w*0.88:.0f}" height="{h*0.88:.0f}" fill="none" stroke="{accent}" stroke-width="3"/>
  <circle cx="{w/2:.0f}" cy="{h*0.42:.0f}" r="{w*0.13:.0f}" fill="none" stroke="{accent}" stroke-width="4"/>
  <circle cx="{w/2:.0f}" cy="{h*0.42:.0f}" r="{w*0.09:.0f}" fill="none" stroke="{accent}" stroke-width="2"/>
  <text x="{w/2:.0f}" y="{h*0.66:.0f}" font-family="Georgia, 'Times New Roman', serif" font-size="{w*0.045:.0f}" fill="{fg}" text-anchor="middle" letter-spacing="2">{label}</text>
  <text x="{w/2:.0f}" y="{h*0.72:.0f}" font-family="Arial, sans-serif" font-size="{w*0.022:.0f}" fill="{fg}" text-anchor="middle" opacity="0.65">{sub}</text>
</svg>'''
    full = os.path.join(ROOT, "public", *path.split("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def md(path, frontmatter, body=""):
    full = os.path.join(ROOT, "src", "content", *path.split("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    lines = ["---"]
    for k, v in frontmatter.items():
        lines.append(f"{k}: {json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else json.dumps(v, ensure_ascii=False)}")
    lines.append("---")
    if body:
        lines += ["", body]
    with open(full, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

# ---------------- Brand / banner / about images ----------------
svg("uploads/brand/logo.svg", "VARDHMAN", "JEWELLERS · JAMMU", "brand", 800, 800)
svg("uploads/banners/hero-1.svg", "DEMO HERO IMAGE", "Replace with your campaign photograph in Pages CMS", "wedding", 1920, 1080)
svg("uploads/banners/craftsmanship.svg", "DEMO CRAFT IMAGE", "Replace with a karigar-at-work photograph", "gold", 1200, 900)
svg("uploads/about/showroom.svg", "DEMO SHOWROOM PHOTO", "Replace in Pages CMS → Business Information", "gold", 1400, 900)
svg("uploads/about/interior-1.svg", "DEMO INTERIOR 1", "Shop interior — replace in Pages CMS", "gold")
svg("uploads/about/interior-2.svg", "DEMO INTERIOR 2", "Shop interior — replace in Pages CMS", "gold")
svg("uploads/about/exterior-1.svg", "DEMO EXTERIOR", "Shop exterior — replace in Pages CMS", "brand")

# ---------------- Categories ----------------
CATEGORIES = [
    ("gold-rings",        "Gold Rings",        "gold",     "Timeless gold rings in 22K and 18K, from classic bands to statement pieces.", 10),
    ("gold-necklaces",    "Gold Necklaces",    "gold",     "Necklaces and chains crafted in hallmarked 22K gold.", 20),
    ("gold-earrings",     "Gold Earrings",     "gold",     "Studs, drops and jhumka-inspired gold earrings.", 30),
    ("gold-bangles",      "Gold Bangles",      "gold",     "Bangles and kadas in traditional and contemporary designs.", 40),
    ("gold-mangalsutra",  "Gold Mangalsutra",  "gold",     "Mangalsutras in hallmarked gold with black bead strands.", 50),
    ("bridal-sets",       "Complete Bridal Sets", "wedding", "Head-to-toe bridal ensembles curated for your wedding day.", 10),
    ("bridal-chokers",    "Bridal Chokers",    "wedding", "Statement chokers for the bride's big day.", 20),
    ("rani-haar",         "Rani Haar",         "wedding", "Regal long necklaces in the rani haar tradition.", 30),
    ("lightweight-rings", "Lightweight Rings", "everyday", "Feather-light rings made for daily wear.", 10),
    ("stud-earrings",     "Stud Earrings",     "everyday", "Small, comfortable studs for office and daily wear.", 20),
    ("diamond-rings",     "Diamond Rings",     "diamond",  "Certified diamond rings set in hallmarked gold.", 10),
    ("silver-anklets",    "Silver Anklets",    "silver",   "Silver payal and anklets in classic patterns.", 10),
]
for slug, name, group, desc, order in CATEGORIES:
    svg(f"uploads/categories/{slug}.svg", "DEMO", name, group if group in PALETTES else "gold")
    md(f"categories/{slug}.md", {
        "name": name,
        "group": group,
        "description": desc,
        "coverImage": f"/uploads/categories/{slug}.svg",
        "order": order,
        "enabled": True,
    })

# ---------------- Products ----------------
PRODUCTS = [
    # file, name, id, category, occasion, metal, purity, gross, net, stone_w, stone_price, mtype, mval, wastage, other, override, bis, huid, avail, featured, new, best
    ("royal-22k-gold-bangle", "Royal 22K Gold Bangle", "VJ-GB-001", "gold-bangles", "traditional", "gold", "22K", 18.450, 18.450, 0, 0, "per-gram", 520, 0, 0, None, True, "HUID123456", "available", True, False, True),
    ("temple-gold-necklace", "Temple Design Gold Necklace", "VJ-GN-001", "gold-necklaces", "wedding", "gold", "22K", 42.300, 41.800, 0.5, 4500, "percent", 11, 0, 0, None, True, "HUID234567", "available", True, False, True),
    ("classic-gold-ring", "Classic 22K Gold Ring", "VJ-GR-001", "gold-rings", "everyday", "gold", "22K", 4.250, 4.250, 0, 0, "per-gram", 480, 0, 0, None, True, "HUID345678", "available", False, False, True),
    ("antique-gold-jhumka", "Antique Finish Gold Jhumka", "VJ-GE-001", "gold-earrings", "traditional", "gold", "22K", 12.600, 12.600, 0, 0, "percent", 14, 0, 0, None, True, "HUID456789", "available", False, True, False),
    ("black-bead-mangalsutra", "22K Gold Mangalsutra", "VJ-GM-001", "gold-mangalsutra", "everyday", "gold", "22K", 9.150, 8.900, 0, 0, "per-gram", 450, 0, 0, None, True, "HUID567890", "available", False, True, False),
    ("maharani-bridal-set", "Maharani Complete Bridal Set", "VJ-BS-001", "bridal-sets", "wedding", "gold", "22K", 185.000, 182.500, 2.5, 22000, "percent", 12, 0, 0, None, True, "HUID678901", "made-to-order", True, True, False),
    ("kundan-bridal-choker", "Kundan Bridal Choker", "VJ-BC-001", "bridal-chokers", "wedding", "gold", "22K", 68.400, 66.200, 2.2, 18500, "percent", 15, 0, 0, None, True, "HUID789012", "available", True, False, False),
    ("regal-rani-haar", "Regal Rani Haar", "VJ-RH-001", "rani-haar", "wedding", "gold", "22K", 95.750, 94.100, 1.6, 12000, "percent", 13, 0, 0, None, True, "HUID890123", "made-to-order", False, False, False),
    ("featherlight-ring", "Featherlight Daily Wear Ring", "VJ-LR-001", "lightweight-rings", "everyday", "gold", "18K", 1.850, 1.850, 0, 0, "fixed", 850, 0, 0, None, True, "", "available", False, True, True),
    ("pearl-stud-earrings", "Everyday Gold Studs", "VJ-SE-001", "stud-earrings", "everyday", "gold", "18K", 2.400, 2.400, 0, 0, "fixed", 1100, 0, 0, None, True, "HUID901234", "available", False, False, True),
    ("solitaire-diamond-ring", "Solitaire Diamond Ring", "VJ-DR-001", "diamond-rings", "wedding", "diamond", "18K", 3.600, 3.200, 0.4, 38000, "per-gram", 950, 0, 0, None, True, "HUID012345", "available", True, True, True),
    ("classic-silver-payal", "Classic Silver Payal (Pair)", "VJ-SA-001", "silver-anklets", "everyday", "silver", "925 Silver", 28.000, 28.000, 0, 0, "fixed", 1500, 0, 0, None, False, "", "available", True, False, False),
]
for (slug, name, pid, cat, occ, metal, purity, gross, net, sw, sp, mt, mv, wast, other, override, bis, huid, avail, feat, new, best) in PRODUCTS:
    theme = {"gold": "gold", "diamond": "diamond", "silver": "silver"}.get(metal, "gold")
    img1, img2 = f"/uploads/products/{slug}-1.svg", f"/uploads/products/{slug}-2.svg"
    svg(f"uploads/products/{slug}-1.svg", "DEMO PHOTO", f"{name} — replace in Pages CMS", theme)
    svg(f"uploads/products/{slug}-2.svg", "DEMO PHOTO 2", f"{name} (angle 2) — replace in Pages CMS", theme)
    md(f"products/{slug}.md", {
        "name": name,
        "productId": pid,
        "category": cat,
        "occasion": occ,
        "metal": metal,
        "purity": purity,
        "grossWeight": gross,
        "netGoldWeight": net,
        "stoneWeight": sw,
        "stonePrice": sp,
        "makingChargeType": mt,
        "makingChargeValue": mv,
        "wastagePercent": wast,
        "otherCharges": other,
        "priceOverride": override,
        "bisHallmark": bis,
        "huid": huid,
        "hallmarkNote": "",
        "availability": avail,
        "featured": feat,
        "newArrival": new,
        "bestseller": best,
        "photos": [img1, img2],
        "shortDescription": f"Demonstration product — {name.lower()} shown to demonstrate catalogue features. Replace with real inventory in Pages CMS.",
        "updatedAt": "2026-11-17",
        "demo": True,
    }, body=f"Demonstration description for **{name}**.\n\nThis sample entry demonstrates how product specifications, photographs, hallmark details and automatic price calculation appear on the website. Replace it with a real article through Pages CMS.")

# ---------------- Testimonials ----------------
TESTIMONIALS = [
    ("demo-customer-1", "Demo Customer", "Jammu", "Sample testimonial — replace with a real customer quote through Pages CMS. Families across Talab Tillo trust us for their wedding jewellery.", 5, 10),
    ("demo-customer-2", "Demo Customer", "Talab Tillo", "Sample testimonial — transparent pricing and hallmark details were explained patiently before purchase.", 5, 20),
    ("demo-customer-3", "Demo Customer", "Gandhi Nagar", "Sample testimonial — beautiful bridal set, made to order and delivered before the wedding date.", 5, 30),
]
for slug, name, loc, quote, rating, order in TESTIMONIALS:
    md(f"testimonials/{slug}.md", {
        "customerName": name,
        "location": loc,
        "quote": quote,
        "rating": rating,
        "order": order,
        "published": True,
    })

# ---------------- Gallery albums ----------------
def album(slug, name, desc, order, featured, count, theme):
    images = []
    for i in range(1, count + 1):
        p = f"/uploads/gallery/{slug}-{i}.svg"
        svg(f"uploads/gallery/{slug}-{i}.svg", "DEMO GALLERY PHOTO", f"{name} #{i} — replace in Pages CMS", theme)
        images.append({"src": p, "caption": f"Demo photograph {i} — replace with your own"})
    md(f"albums/{slug}.md", {
        "name": name,
        "description": desc,
        "coverImage": images[0]["src"],
        "images": images,
        "order": order,
        "published": True,
        "featuredOnHomepage": featured,
    })

album("wedding-highlights", "Wedding Highlights", "Demo album — bridal and wedding jewellery photography. Replace with your own album in Pages CMS.", 10, True, 4, "wedding")
album("showroom-gallery", "Our Showroom", "Demo album — photographs of the showroom. Replace with your own album in Pages CMS.", 20, False, 3, "gold")

print("Demo content generated.")
