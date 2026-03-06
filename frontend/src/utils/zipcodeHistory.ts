const STORAGE_KEY = 'chc_recent_zipcodes';
const MAX_RECENT = 10;

export function addZipcodeToHistory(zipcode: string): void {
  if (!zipcode?.trim()) return;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const list: string[] = raw ? JSON.parse(raw) : [];
    const next = [zipcode.trim(), ...list.filter((z) => z !== zipcode.trim())].slice(0, MAX_RECENT);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  } catch {
    // ignore
  }
}

export function getUniqueZipcodes(): string[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const list: string[] = raw ? JSON.parse(raw) : [];
    return [...new Set(list)];
  } catch {
    return [];
  }
}
