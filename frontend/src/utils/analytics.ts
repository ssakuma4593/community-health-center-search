/**
 * Google Analytics (GA4) for Community Health Center Search.
 * Tracks usage on both localhost and the public GitHub Pages site.
 * Set VITE_GA_MEASUREMENT_ID (e.g. G-XXXXXXXXXX) in .env or GitHub Actions secrets.
 */

const env = (import.meta as unknown as { env?: { VITE_GA_MEASUREMENT_ID?: string; DEV?: boolean } }).env;
const MEASUREMENT_ID = env?.VITE_GA_MEASUREMENT_ID;

declare global {
  interface Window {
    dataLayer: unknown[];
    gtag: (...args: unknown[]) => void;
  }
}

function getGtag(): typeof window.gtag | null {
  if (!MEASUREMENT_ID) return null;
  return typeof window !== 'undefined' && typeof window.gtag === 'function' ? window.gtag : null;
}

/**
 * Initialize Google Analytics. Runs on every origin (localhost and GitHub Pages)
 * when VITE_GA_MEASUREMENT_ID is set, so the public site is tracked.
 */
export function initAnalytics(): void {
  if (!MEASUREMENT_ID) {
    if (env?.DEV) {
      console.debug('[Analytics] No VITE_GA_MEASUREMENT_ID; analytics disabled.');
    }
    return;
  }

  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag() {
    window.dataLayer.push(arguments);
  };
  window.gtag('js', new Date());
  window.gtag('config', MEASUREMENT_ID, {
    send_page_view: true,
    page_path: window.location.pathname + window.location.search,
  });

  // Load gtag.js script (works on any domain, including GitHub Pages)
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${MEASUREMENT_ID}`;
  document.head.appendChild(script);
}

export function trackZipcodeSearch(
  zipcode: string,
  radiusMiles: number,
  resultCount: number,
  _serviceFilters: string[]
): void {
  const g = getGtag();
  if (!g) return;
  g('event', 'zipcode_search', {
    zipcode,
    radius_miles: radiusMiles,
    result_count: resultCount,
  });
}

export function trackServiceFilterToggle(_filterName: string, _enabled: boolean): void {
  const g = getGtag();
  if (!g) return;
  g('event', 'service_filter_toggle', {
    filter_name: _filterName,
    enabled: _enabled,
  });
}

export function trackCenterDetailView(centerName: string): void {
  const g = getGtag();
  if (!g) return;
  g('event', 'view_center_detail', { center_name: centerName });
}

export function trackContactClick(contactType: string, centerName: string): void {
  const g = getGtag();
  if (!g) return;
  g('event', 'contact_click', { contact_type: contactType, center_name: centerName });
}

export function trackBookingInfoClick(centerName: string): void {
  const g = getGtag();
  if (!g) return;
  g('event', 'booking_info_click', { center_name: centerName });
}
