/**
 * Analytics utility for tracking user interactions
 * Uses Google Analytics 4 (GA4) for event tracking
 */

// GA4 Measurement ID - Set this via environment variable or replace with your ID
// @ts-expect-error - VITE_GA_MEASUREMENT_ID is provided by Vite
const GA_MEASUREMENT_ID = import.meta.env.VITE_GA_MEASUREMENT_ID || '';

// Initialize GA4
export const initAnalytics = () => {
  // Only run in browser environment
  if (typeof window === 'undefined') {
    return;
  }

  if (!GA_MEASUREMENT_ID) {
    console.warn('GA4 Measurement ID not set. Analytics will not track events.');
    return;
  }

  // Load gtag script if not already loaded
  if (!window.gtag) {
    const script1 = document.createElement('script');
    script1.async = true;
    script1.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
    document.head.appendChild(script1);

    const script2 = document.createElement('script');
    script2.innerHTML = `
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '${GA_MEASUREMENT_ID}', {
        anonymize_ip: true,
        allow_google_signals: false,
        allow_ad_personalization_signals: false
      });
    `;
    document.head.appendChild(script2);
  }
};

// Track zip code search
export const trackZipcodeSearch = (zipcode: string, radius: number, resultsCount: number, serviceFilters: string[] = []) => {
  if (!GA_MEASUREMENT_ID || typeof window === 'undefined' || !window.gtag) {
    return;
  }

  window.gtag('event', 'zipcode_search', {
    zipcode: zipcode,
    radius: radius,
    results_count: resultsCount,
    service_filters: serviceFilters.join(','),
    // Don't send full zipcode to GA for privacy - hash it or use first 3 digits
    zipcode_hash: hashZipcode(zipcode)
  });
};

// Track booking info button click
export const trackBookingInfoClick = (centerName: string, searchZipcode?: string) => {
  if (!GA_MEASUREMENT_ID || typeof window === 'undefined' || !window.gtag) {
    return;
  }

  window.gtag('event', 'booking_info_click', {
    center_name: centerName,
    search_zipcode: searchZipcode || 'none'
  });
};

// Track service filter toggle
export const trackServiceFilterToggle = (filterType: string, enabled: boolean) => {
  if (!GA_MEASUREMENT_ID || typeof window === 'undefined' || !window.gtag) {
    return;
  }

  window.gtag('event', 'service_filter_toggle', {
    filter_type: filterType,
    enabled: enabled
  });
};

// Track center detail view
export const trackCenterDetailView = (centerName: string) => {
  if (!GA_MEASUREMENT_ID || typeof window === 'undefined' || !window.gtag) {
    return;
  }

  window.gtag('event', 'center_detail_view', {
    center_name: centerName
  });
};

// Track contact link click (phone, website, maps)
export const trackContactClick = (type: 'phone' | 'website' | 'maps', centerName: string) => {
  if (!GA_MEASUREMENT_ID || typeof window === 'undefined' || !window.gtag) {
    return;
  }

  window.gtag('event', 'contact_click', {
    contact_type: type,
    center_name: centerName
  });
};

// Simple hash function for zipcode (for privacy)
// Returns first 3 digits + hash of full zipcode
function hashZipcode(zipcode: string): string {
  if (zipcode.length < 3) return '***';
  const prefix = zipcode.substring(0, 3);
  // Simple hash of remaining digits
  const remaining = zipcode.substring(3);
  let hash = 0;
  for (let i = 0; i < remaining.length; i++) {
    hash = ((hash << 5) - hash) + remaining.charCodeAt(i);
    hash = hash & hash; // Convert to 32bit integer
  }
  return `${prefix}-${Math.abs(hash).toString(36)}`;
}

// Extend Window interface for TypeScript
declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
    dataLayer?: any[];
  }
}
