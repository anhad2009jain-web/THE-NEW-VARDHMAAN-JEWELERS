// Gold pricing engine.
// All rates, tax and staleness settings come from src/data/gold-rates.json,
// which the owner edits through Pages CMS ("Daily Gold Rates").
// Nothing here is hardcoded — if a rate is missing, zero or outdated,
// products display "Price on Request" instead of an invented number.

import goldRates from '../data/gold-rates.json';

export interface PriceBreakdown {
  available: boolean;          // false → show "Price on Request"
  overridden: boolean;         // owner set a manual price override
  goldValue: number;
  makingCharges: number;
  stoneCharges: number;
  wastage: number;
  otherCharges: number;
  subtotal: number;
  taxAmount: number;
  total: number;
  ratePerGram: number | null;
  taxPercent: number;
  taxLabel: string;
  ratesUpdatedAt: string;
  ratesStale: boolean;
  disclaimer: string;
}

export interface RateTable {
  rates: Record<string, number | null>;
  currency: string;
  taxPercent: number;
  taxLabel: string;
  updatedAt: string;
  stale: boolean;
  valid: boolean;              // false when any core rate is missing/zero
  disclaimer: string;
}

const CORE_PURITIES = ['24K', '22K', '18K'] as const;

function toPaise(n: number): number {
  return Math.round(n * 100);
}
function toRupees(paise: number): number {
  return paise / 100;
}

/** Is the rate table older than the allowed age? */
export function ratesStale(now: Date = new Date()): boolean {
  const maxAgeHours = Number(goldRates.maxRateAgeHours) || 72;
  const updated = new Date(goldRates.updatedAt);
  if (isNaN(updated.getTime())) return true;
  return now.getTime() - updated.getTime() > maxAgeHours * 3600 * 1000;
}

export function getRateTable(now: Date = new Date()): RateTable {
  const rates: Record<string, number | null> = {};
  for (const [purity, value] of Object.entries(goldRates.rates)) {
    const n = Number(value);
    rates[purity] = Number.isFinite(n) && n > 0 ? n : null;
  }
  const stale = ratesStale(now);
  const valid = CORE_PURITIES.every((p) => rates[p] !== null);
  return {
    rates,
    currency: goldRates.currency || 'INR',
    taxPercent: Number(goldRates.taxPercent) || 0,
    taxLabel: goldRates.taxLabel || 'Tax',
    updatedAt: goldRates.updatedAt,
    stale,
    valid,
    disclaimer: goldRates.priceDisclaimer || '',
  };
}

export interface ProductPricingInput {
  purity: string;
  grossWeight: number;
  netGoldWeight: number;
  stonePrice: number;
  diamondPrice: number;
  makingChargeType: 'fixed' | 'per-gram' | 'percent';
  makingChargeValue: number;
  wastagePercent: number;
  otherCharges: number;
  priceOverride: number | null;
  metal: string;
}

const METAL_RATE_KEY: Record<string, string | null> = {
  gold: null,        // resolved from purity below
  diamond: null,     // diamond jewellery is priced on its gold content
  silver: '925 Silver',
  platinum: null,
  other: null,
};

/**
 * Compute the estimated price of one product.
 * Returns available=false whenever a trustworthy price cannot be produced
 * (missing/zero/outdated rate, zero metal weight) so the UI can show
 * "Price on Request" rather than a fabricated number.
 */
export function computePrice(input: ProductPricingInput, now: Date = new Date()): PriceBreakdown {
  const table = getRateTable(now);

  const base: PriceBreakdown = {
    available: false,
    overridden: false,
    goldValue: 0,
    makingCharges: 0,
    stoneCharges: 0,
    wastage: 0,
    otherCharges: 0,
    subtotal: 0,
    taxAmount: 0,
    total: 0,
    ratePerGram: null,
    taxPercent: table.taxPercent,
    taxLabel: table.taxLabel,
    ratesUpdatedAt: table.updatedAt,
    ratesStale: table.stale,
    disclaimer: table.disclaimer,
  };

  // 1. Manual override always wins — the owner has explicitly set this price.
  if (input.priceOverride && input.priceOverride > 0) {
    const total = toRupees(toPaise(input.priceOverride));
    return { ...base, available: true, overridden: true, total };
  }

  // 2. Resolve the applicable per-gram rate.
  const rateKey = input.metal === 'silver' ? '925 Silver' : input.purity;
  const ratePerGram = table.rates[rateKey] ?? null;
  base.ratePerGram = ratePerGram;

  const metalWeight = input.netGoldWeight > 0 ? input.netGoldWeight : 0;
  if (!ratePerGram || metalWeight <= 0 || table.stale) {
    return base; // → "Price on Request"
  }

  // 3. Gold value.
  const goldValue = metalWeight * ratePerGram;
  base.goldValue = toRupees(toPaise(goldValue));

  // 4. Making charges — fixed ₹, ₹/g (on gross weight), or % of gold value.
  let making = 0;
  if (input.makingChargeType === 'fixed') {
    making = input.makingChargeValue;
  } else if (input.makingChargeType === 'per-gram') {
    making = input.makingChargeValue * (input.grossWeight > 0 ? input.grossWeight : metalWeight);
  } else if (input.makingChargeType === 'percent') {
    making = (input.makingChargeValue / 100) * goldValue;
  }
  base.makingCharges = toRupees(toPaise(making));

  // 5. Stones, wastage, other charges.
  const materialPrice =
  input.metal === 'diamond'
    ? input.diamondPrice
    : input.stonePrice;

base.stoneCharges = toRupees(toPaise(materialPrice || 0));
  base.wastage = toRupees(toPaise(((input.wastagePercent || 0) / 100) * goldValue));
  base.otherCharges = toRupees(toPaise(input.otherCharges || 0));

  // 6. Subtotal + tax, all in paise to avoid floating point drift.
  const subtotalPaise =
    toPaise(base.goldValue) +
    toPaise(base.makingCharges) +
    toPaise(base.stoneCharges) +
    toPaise(base.wastage) +
    toPaise(base.otherCharges);
  base.subtotal = toRupees(subtotalPaise);

  base.taxAmount = toRupees(Math.round((subtotalPaise * table.taxPercent) / 100));
  base.total = toRupees(subtotalPaise + toPaise(base.taxAmount));
  base.available = true;

  return base;
}

/** Human-readable description of a product's making charges. */
export function describeMakingCharges(input: ProductPricingInput): string {
  const v = input.makingChargeValue;
  if (input.makingChargeType === 'fixed') return `₹${v.toLocaleString('en-IN')} (fixed)`;
  if (input.makingChargeType === 'per-gram') return `₹${v.toLocaleString('en-IN')} / gram`;
  return `${v}% of gold value`;
}
