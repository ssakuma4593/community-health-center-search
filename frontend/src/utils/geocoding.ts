import type { ZipcodeLocation } from '../types';

/**
 * Free zipcode geocoding using a simple API
 * Falls back to a basic lookup if API fails
 */
export async function geocodeZipcode(zipcode: string): Promise<ZipcodeLocation | null> {
  // Remove any non-numeric characters
  const cleanZip = zipcode.replace(/\D/g, '');
  
  if (cleanZip.length !== 5) {
    return null;
  }

  try {
    // Try using Nominatim (OpenStreetMap's free geocoding service)
    // No API key required, but please use responsibly (max 1 request per second)
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?postalcode=${cleanZip}&countrycodes=us&format=json&limit=1`,
      {
        headers: {
          'User-Agent': 'CommunityHealthCenterSearch/1.0', // Required by Nominatim
        },
      }
    );
    
    if (response.ok) {
      const data = await response.json();
      if (data && data.length > 0) {
        const result = data[0];
        return {
          zipcode: cleanZip,
          latitude: parseFloat(result.lat),
          longitude: parseFloat(result.lon),
          city: result.address?.city || result.address?.town || result.address?.village,
          state: result.address?.state,
        };
      }
    }
  } catch (error) {
    console.warn('Geocoding API failed, using fallback:', error);
  }

  // Fallback: Use a simple lookup for common MA zipcodes
  // This is a basic fallback - in production you'd want a more complete dataset
  const fallback = getZipcodeFallback(cleanZip);
  if (fallback) {
    return fallback;
  }

  return null;
}

/**
 * Fallback zipcode lookup for common Massachusetts zipcodes
 * This is a minimal implementation - you could expand this with a full dataset
 */
function getZipcodeFallback(zipcode: string): ZipcodeLocation | null {
  // Common MA zipcode centroids (approximate)
  const commonZipcodes: Record<string, { lat: number; lng: number; city: string }> = {
    '02138': { lat: 42.3736, lng: -71.1190, city: 'Cambridge' },
    '02139': { lat: 42.3656, lng: -71.1040, city: 'Cambridge' },
    '02140': { lat: 42.3916, lng: -71.1230, city: 'Cambridge' },
    '02141': { lat: 42.3731, lng: -71.0854, city: 'Cambridge' },
    '02118': { lat: 42.3389, lng: -71.0736, city: 'Boston' },
    '02115': { lat: 42.3429, lng: -71.1000, city: 'Boston' },
    '02116': { lat: 42.3500, lng: -71.0800, city: 'Boston' },
    '01420': { lat: 42.5806, lng: -71.7939, city: 'Fitchburg' },
    '02148': { lat: 42.4199, lng: -71.0728, city: 'Malden' },
    '02145': { lat: 42.3921, lng: -71.0930, city: 'Somerville' },
  };

  const match = commonZipcodes[zipcode];
  if (match) {
    return {
      zipcode,
      latitude: match.lat,
      longitude: match.lng,
      city: match.city,
      state: 'MA',
    };
  }

  // If no match, try to estimate based on first 3 digits (MA area codes)
  // This is very approximate
  const prefix = zipcode.substring(0, 3);
  if (prefix === '021') {
    // Boston area - approximate center
    return {
      zipcode,
      latitude: 42.3601,
      longitude: -71.0589,
      city: 'Boston Area',
      state: 'MA',
    };
  }

  return null;
}
