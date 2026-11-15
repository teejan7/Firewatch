import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import StaticApp from './StaticApp';

vi.mock('./GlobalMap', () => ({ default: () => <div role="img" aria-label="Aggregated global map"/> }));

const catalog = { data_status: 'PARTIAL FIRMS', countries: [{ name: 'India', slug: 'india', coverage_years: [2020, 2021], first_date: '2020-01-01', last_date: '2021-12-31', products: ['MODIS_SP', 'VIIRS_NOAA20_SP'], platforms: ['Terra', 'NOAA-20'], processed_source_files: 4, observed_bbox: null }] };
const series = { country: 'India', data_status: 'Partial', coverage: { first_date: '2020-01-01', last_date: '2021-12-31', years: [2020, 2021], products: ['MODIS_SP', 'VIIRS_NOAA20_SP'], platforms: ['Terra', 'NOAA-20'], processed_source_files: 4, source_rows_processed: 100, by_product_year: [{ country: 'India', product: 'MODIS_SP', year: 2021, expected: 2, processed: 1, rows: 20, status: 'partial' }] }, daily: [['2021-01-01', 'MODIS', 'Terra', 'SP', 8, 12.5, 0.6, 5, 8.25, 7, 11.5, 3, 5.5, 5, 7, 1, true, true, true]], grid: [], source_files: [{ source_file: 'modis_2021_India.csv', file_id: 'abc123', product: 'MODIS_SP', year: 2021, rows_processed: 20, processing_versions: ['61.03'] }], metric_definition: 'Source records', harmonization_status: 'not applied', grid_definition: '1-degree view' };
const methods = { method_version: 'loglog-theilsen-loyo-v1', validation_metrics: { median_r2: 0.8, median_holdout_mdape: 0.4, confidence_counts: { High: 67, Medium: 65, Low: 104 }, median_continuity_ratio_before: 2.8, median_continuity_ratio_after: 1 }, thresholds: { minimum_weekly_frp_mw_per_family: 5, minimum_country_overlap_weeks: 40 }, plain_language_rule: 'Fit paired operating weeks.' };
const harmonized = { country: 'India', confidence: 'High', fit: 'country', daily: [{ date: '2021-01-01', year: 2021, doy: 1, raw_modis_frp: 5, raw_viirs_frp: 8, raw_frp_sum: 13, modis_n: 5, viirs_n: 8, week: '2020-12-28', operating_week: true, daily_scale_for_viirs: 0.3, scaled_viirs_frp: 2.4, harmonized_frp_daily: 7.4, raw_unusual_week: false, harmonized_unusual_week: false, has_source_record: true }], climatology_by_doy: [{ doy: 1, sample_years: 1, raw_median: 13, raw_q25: 13, raw_q75: 13, harmonized_median: 7.4, harmonized_q25: 7.4, harmonized_q75: 7.4, raw_by_year: { '2021': 13 }, harmonized_by_year: { '2021': 7.4 }, raw_unusual_by_year: {}, harmonized_unusual_by_year: {} }], fire_season_by_year: { '2021': { raw: { start: '2021-01-01', peak: '2021-01-01', end: '2021-01-01', annual_frp: 13 }, harmonized: { start: '2021-01-01', peak: '2021-01-01', end: '2021-01-01', annual_frp: 7.4 } } } };
const jsonResponse = (body: unknown) => new Response(JSON.stringify(body), { status: 200, headers: { 'content-type': 'application/json' } });

describe('static FIREWATCH dashboard', () => {
  afterEach(() => { cleanup(); vi.unstubAllGlobals(); });
  beforeEach(() => { vi.stubGlobal('ResizeObserver', class { observe(){} unobserve(){} disconnect(){} }); });

  it('loads country JSON, displays the coverage caveat and method explanation without API calls', async () => {
    const fetcher = vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes('countries.json')) return Promise.resolve(jsonResponse(catalog));
      if (url.includes('map_activity.json')) return Promise.resolve(jsonResponse({ countries: [] }));
      if (url.includes('methods_validation.json')) return Promise.resolve(jsonResponse(methods));
      if (url.includes('harmonized/')) return Promise.resolve(jsonResponse(harmonized));
      return Promise.resolve(jsonResponse(series));
    });
    vi.stubGlobal('fetch', fetcher);
    render(<StaticApp/>);
    expect(await screen.findByRole('heading', { name: 'Burning activity · India' })).toBeTruthy();
    expect(screen.getByText(/Partial source-file set/)).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: /How it works/ }));
    expect(screen.getByRole('dialog', { name: 'How FIREWATCH handles these records' })).toBeTruthy();
    expect(fetcher.mock.calls.every(([input]) => !String(input).includes('/api/'))).toBe(true);
    expect(screen.getByText(/Statistical cross-sensor calibration, validated leave-one-year-out/)).toBeTruthy();
    expect(screen.getByText(/Not a physical retrieval correction/)).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Harmonized' })).toBeTruthy();
    expect(screen.getAllByText(/PRELIMINARY \(6-year baseline\)/).length).toBeGreaterThan(0);
    expect(fetcher.mock.calls.some(([input]) => String(input).endsWith('data/methods_validation.json'))).toBe(true);
    expect(fetcher.mock.calls.some(([input]) => String(input).includes('data/harmonized/india.json'))).toBe(true);
  });

  it('explains when a missing static series is served as an HTML fallback', async () => {
    const fetcher = vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes('countries.json')) return Promise.resolve(jsonResponse(catalog));
      if (url.includes('map_activity.json')) return Promise.resolve(jsonResponse({ countries: [] }));
      return Promise.resolve(new Response('<!doctype html><title>Not found</title>', { status: 200, headers: { 'content-type': 'text/html' } }));
    });
    vi.stubGlobal('fetch', fetcher);
    render(<StaticApp/>);
    expect(await screen.findByRole('alert')).toBeTruthy();
    expect(screen.getByText(/Series for India did not return JSON.*text\/html.*static data file may be missing/i)).toBeTruthy();
    expect(screen.queryByRole('heading', { name: 'Burning activity · India' })).toBeNull();
  });

  it('exports the daily quality, type and day/night fields in the selected-year CSV', async () => {
    const fetcher = vi.fn((input: RequestInfo | URL) => { const url = String(input); if (url.includes('countries.json')) return Promise.resolve(jsonResponse(catalog)); if (url.includes('methods_validation.json')) return Promise.resolve(jsonResponse(methods)); if (url.includes('harmonized/')) return Promise.resolve(jsonResponse(harmonized)); return Promise.resolve(jsonResponse(series)); });
    vi.stubGlobal('fetch', fetcher);
    const createObjectURL = vi.fn((blob: Blob | MediaSource) => {
      expect(blob).toBeInstanceOf(Blob);
      return 'blob:firewatch';
    });
    const URLWithBlobMethods = Object.assign(class extends URL {}, {
      createObjectURL,
      revokeObjectURL: vi.fn(),
    });
    vi.stubGlobal('URL', URLWithBlobMethods);
    vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => undefined);
    render(<StaticApp/>);
    await screen.findByRole('heading', { name: 'Burning activity · India' });
    fireEvent.click(screen.getByRole('button', { name: 'Export selected year CSV' }));
    const blob = createObjectURL.mock.calls[0]?.[0];
    if (!(blob instanceof Blob)) throw new Error('CSV export did not create a Blob.');
    const csv = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result));
      reader.onerror = () => reject(reader.error);
      reader.readAsText(blob);
    });
    expect(csv).toContain('vegetation_n_detections');
    expect(csv).toContain('high_quality_frp_sum_mw');
    expect(csv).toContain('night_n_detections');
    expect(csv).toContain('"2021-01-01","MODIS","Terra","SP","8","12.5"');
  });
});
