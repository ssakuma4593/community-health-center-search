export interface HealthCenter {
  name: string;
  street_address_1: string;
  street_address_2: string;
  city_town: string;
  state: string;
  zipcode: string;
  phone: string;
  types: string;
  website: string;
  source: string;
  latitude: number;
  longitude: number;
  distance?: number; // Calculated distance from search zipcode
  // OpenAI enrichment fields (optional)
  openai_phone?: string;
  openai_address?: string;
  openai_new_patient_md?: string;
  openai_other_notes_md?: string;
  openai_source_urls?: string;
  openai_last_checked_utc?: string;
  openai_confidence?: string;
}

export interface ZipcodeLocation {
  zipcode: string;
  latitude: number;
  longitude: number;
  city?: string;
  state?: string;
}
