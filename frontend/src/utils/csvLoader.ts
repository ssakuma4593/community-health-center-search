import Papa from 'papaparse';
import type { HealthCenter } from '../types';

export async function loadHealthCenters(): Promise<HealthCenter[]> {
  try {
    // Use base URL for GitHub Pages compatibility
    const baseUrl = import.meta.env.BASE_URL;
    const csvPath = `${baseUrl}data/centers.csv`;
    console.log('Loading CSV from:', csvPath);
    const response = await fetch(csvPath);
    
    if (!response.ok) {
      throw new Error(`Failed to load CSV: ${response.status} ${response.statusText}`);
    }
    
    const text = await response.text();
    
    return new Promise((resolve, reject) => {
      Papa.parse<HealthCenter>(text, {
        header: true,
        skipEmptyLines: true,
        transformHeader: (header) => {
          // Normalize header names
          return header.trim().toLowerCase().replace(/\s+/g, '_');
        },
        transform: (value, field) => {
          // Convert numeric fields
          if (field === 'latitude' || field === 'longitude') {
            const num = parseFloat(value);
            return isNaN(num) ? 0 : num;
          }
          return value || '';
        },
        complete: (results) => {
          const centers = results.data.filter(
            (center) => center.latitude && center.longitude && center.latitude !== 0 && center.longitude !== 0
          ) as HealthCenter[];
          console.log(`Loaded ${centers.length} health centers from CSV`);
          resolve(centers);
        },
        error: (error: Error) => {
          reject(error);
        },
      });
    });
  } catch (error) {
    console.error('Error loading health centers:', error);
    return [];
  }
}
