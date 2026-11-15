import { describe, expect, it } from 'vitest';
import { demoRecords } from '../data/demo';
import { csvFor, filterRecords, withDateBound } from './filters';

describe('selected records', () => {
  it('filters consistently by sensor, region and date', () => {
    const records = filterRecords(demoRecords, { region: 'South America', sensor: 'VIIRS', start: '2026-10-01', end: '2026-10-31' });
    expect(records.length).toBeGreaterThan(0);
    expect(records.every(r => r.sensor === 'VIIRS' && r.longitude < -30)).toBe(true);
  });
  it('exports selected records as escaped CSV while retaining provenance', () => {
    const result = csvFor(demoRecords.slice(0, 1));
    expect(result.split('\n')).toHaveLength(2);
    expect(result).toContain('source');
    expect(result).toContain('Simulated demo data');
  });
  it('neutralizes formula-like text in data and provenance cells', () => {
    const record = { ...demoRecords[0], confidence: '=HYPERLINK("https://example.test")', metadata: { source: '+SUM(1,1)' } };
    const result = csvFor([record]);
    expect(result).toContain("'=HYPERLINK");
    expect(result).toContain("'+SUM");
  });
  it('keeps date bounds ordered and supports an open-ended range', () => {
    const filters = { region: 'All regions', sensor: 'All sensors', start: '2025-02-01', end: '2025-02-02' };
    expect(withDateBound(filters, 'start', '2025-02-04')).toMatchObject({ start: '2025-02-04', end: '2025-02-04' });
    expect(withDateBound(filters, 'end', '2025-01-30')).toMatchObject({ start: '2025-01-30', end: '2025-01-30' });
    expect(filterRecords(demoRecords, { ...filters, start: '', end: '' })).toHaveLength(demoRecords.length);
  });
});
