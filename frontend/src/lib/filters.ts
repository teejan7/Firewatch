import type { FireRecord } from '../data/demo';
export type Filters = { region: string; sensor: string; start: string; end: string };
export function filterRecords(records: FireRecord[], filters: Filters): FireRecord[] {
  return records.filter(r => (filters.region === 'All regions' || (r.regionScope ? r.regionScope === filters.region : regionFor(r) === filters.region)) && (filters.sensor === 'All sensors' || r.sensor === filters.sensor) && (!filters.start || r.acquired >= filters.start) && (!filters.end || r.acquired <= filters.end));
}
export function withDateBound(filters: Filters, bound: 'start' | 'end', value: string): Filters {
  if (!value) return { ...filters, [bound]: '' };
  if (bound === 'start' && filters.end && value > filters.end) return { ...filters, start: value, end: value };
  if (bound === 'end' && filters.start && value < filters.start) return { ...filters, start: value, end: value };
  return { ...filters, [bound]: value };
}
export function regionFor(r: FireRecord): string {
  if (r.longitude < -30 && r.latitude < 15 && r.latitude > -25) return 'South America';
  if (r.longitude < -50) return 'North America';
  if (r.longitude > 110 && r.latitude < 0) return 'Oceania';
  if (r.longitude > 90 && r.latitude > 30) return 'Asia';
  if (r.longitude > 10 && r.longitude < 45 && r.latitude < 15) return 'Africa';
  if (r.longitude > 10 && r.longitude < 45) return 'Europe';
  if (r.longitude > 90) return 'Asia';
  return 'Other';
}
export function csvFor(records: FireRecord[]): string {
  const columns = ['id', 'latitude', 'longitude', 'brightness', 'confidence', 'acquired', 'sensor', 'daynight', 'source'];
  const originalColumns = Array.from(new Set(records.flatMap(r => Object.keys(r.metadata || {})))).map(k => `original_${k}`);
  const keys = [...columns, ...originalColumns];
  const value = (record: FireRecord, key: string) => key.startsWith('original_') ? record.metadata?.[key.slice(9)] ?? '' : record[key as keyof FireRecord] ?? '';
  const csvCell = (input: unknown) => { const text = String(input); const safe = /^[=+\-@]/.test(text) ? `'${text}` : text; return `"${safe.replace(/"/g, '""')}"`; };
  return [keys.map(csvCell).join(','), ...records.map(r => keys.map(k => csvCell(value(r, k))).join(','))].join('\n');
}
