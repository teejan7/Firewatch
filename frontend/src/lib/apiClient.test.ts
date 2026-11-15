import { afterEach, describe, expect, it, vi } from 'vitest';
import { ApiClientError, apiGet, apiPost } from './apiClient';

describe('shared API client', () => {
  afterEach(() => vi.unstubAllGlobals());

  it('turns network failures into a run instruction without raw browser text', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')));
    await expect(apiGet('http://localhost:8000/api/health', { retries: 0 })).rejects.toMatchObject({
      name: 'ApiClientError', kind: 'network',
      message: expect.stringContaining('npm run dev'),
    });
  });

  it('retries an idempotent GET after a server error', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify({ detail: 'temporary failure' }), { status: 503 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'ok' }), { status: 200 }));
    vi.stubGlobal('fetch', fetchMock);
    await expect(apiGet<{ status: string }>('http://localhost:8000/api/health', { retries: 1 })).resolves.toEqual({ status: 'ok' });
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it('keeps validation messages actionable and never retries POST uploads', async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: 'Start date must be on or before end date.' }), { status: 422 }));
    vi.stubGlobal('fetch', fetchMock);
    await expect(apiPost('http://localhost:8000/api/ingest/firms', new FormData())).rejects.toMatchObject({
      name: 'ApiClientError', kind: 'http', status: 422,
      message: 'Start date must be on or before end date.',
    } satisfies Partial<ApiClientError>);
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});
