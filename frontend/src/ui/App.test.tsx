import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import App from './App';

vi.mock('./MapView', () => ({ default: () => <div aria-label="Map placeholder"/> }));
vi.mock('./TimelineChart', () => ({ default: () => <div/> }));
vi.mock('./DataExplorer', () => ({ default: () => <div/> }));
vi.mock('./ProcessedComparison', () => ({ default: () => <div/> }));

describe('API connection status', () => {
  afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

  it('recovers from offline to online after Retry without a page reload', async () => {
    let healthCalls = 0;
    vi.stubGlobal('fetch', vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith('/api/health')) {
        healthCalls += 1;
        if (healthCalls === 1) return Promise.reject(new TypeError('Failed to fetch'));
        return Promise.resolve(new Response(JSON.stringify({ firms_api_configured: false, local_analytics_available: true, data_status: 'ok' }), { status: 200 }));
      }
      return Promise.resolve(new Response(JSON.stringify({ countries: [], products: [] }), { status: 200 }));
    }));

    render(<App/>);
    expect(await screen.findByText(/FIREWATCH API OFFLINE/)).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Retry connection' }));
    expect(await screen.findByText(/FIREWATCH API ONLINE/)).toBeTruthy();
    expect(healthCalls).toBe(2);
  });
});
