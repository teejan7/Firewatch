import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import ProcessedComparison from './ProcessedComparison';

const comparison = {
  status: 'comparison_only', calibration_status: 'insufficient_calibration',
  calibration_reason: 'No validated calibration.', coverage_status: 'detection-record coverage only',
  metric_definition: 'Detected cell-days, not fire counts.', method_version: '1.0.0',
  data_status: 'Processed local FIRMS archives',
  daily_union: [{ date: '2025-01-01', unique_detected_cell_days: 5, modis_detected_cell_days: 3, viirs_detected_cell_days: 4, cross_sensor_overlap_cell_days: 2 }],
  daily_by_product_platform: [{ date: '2025-01-01', sensor_family: 'VIIRS', platform: 'NOAA-20', product_type: 'SP', detected_cell_days: 4, raw_records: 8, frp_sum_mw: 10, frp_max_mw: 4 }],
};

function jsonResponse(body: unknown, ok = true) { return Promise.resolve(new Response(JSON.stringify(body), { status: ok ? 200 : 422 })); }

describe('ProcessedComparison', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes('/api/data-quality')) return jsonResponse({ status: 'partial_local_archive', files_processed: 3, files_discovered: 5 });
      return jsonResponse(comparison);
    }));
  });
  afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

  it('queries the local calendar and shows sensor-specific day details', async () => {
    render(<ProcessedComparison api="http://localhost:8000" apiStatus="online"/>);
    expect(await screen.findByText(/3 of 5 discovered files processed/)).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Query processed data' }));
    expect(await screen.findByLabelText('2025-01-01: 5 detected cell-days')).toBeTruthy();
    fireEvent.click(screen.getByLabelText('2025-01-01: 5 detected cell-days'));
    expect((await screen.findAllByText('NOAA-20')).length).toBe(2);
    expect(screen.getByText(/INSUFFICIENT CALIBRATION/)).toBeTruthy();
  });

  it('shows actionable API errors without hiding them as zero activity', async () => {
    vi.stubGlobal('fetch', vi.fn((input: RequestInfo | URL) => String(input).includes('/api/data-quality')
      ? jsonResponse({ status: 'partial_local_archive', files_processed: 1, files_discovered: 2 })
      : jsonResponse({ detail: 'Processed daily-cell data is unavailable.' }, false)));
    render(<ProcessedComparison api="http://localhost:8000" apiStatus="online"/>);
    fireEvent.click(screen.getByRole('button', { name: 'Query processed data' }));
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('Processed daily-cell data is unavailable.'));
  });
});
