export type ApiErrorKind = 'network' | 'timeout' | 'http' | 'invalid-response' | 'aborted';

export class ApiClientError extends Error {
  constructor(message: string, readonly kind: ApiErrorKind, readonly status?: number) {
    super(message);
    this.name = 'ApiClientError';
  }
}

type RequestOptions = { timeoutMs?: number; retries?: number; signal?: AbortSignal };

function serverDetail(body: unknown): string | undefined {
  if (!body || typeof body !== 'object') return undefined;
  const detail = (body as { detail?: unknown }).detail;
  return typeof detail === 'string' ? detail : undefined;
}

function responseError(status: number, detail?: string): ApiClientError {
  const origin = detail?.trim();
  if (status === 429) return new ApiClientError(origin || 'The local service is busy. Wait a moment and retry.', 'http', status);
  if (status >= 500) return new ApiClientError(origin ? `Server error: ${origin}` : 'The FIREWATCH server encountered an error. Retry in a moment.', 'http', status);
  if (status === 401 || status === 403) return new ApiClientError(origin || 'This request is not authorized. Check the server configuration.', 'http', status);
  if (status >= 400) return new ApiClientError(origin || `The request was rejected (HTTP ${status}). Check the selected dates, area, and source.`, 'http', status);
  return new ApiClientError(origin || `Request failed (HTTP ${status}).`, 'http', status);
}

export async function apiRequest<T>(url: string, init: RequestInit = {}, options: RequestOptions = {}): Promise<T> {
  const method = (init.method || 'GET').toUpperCase();
  const retries = method === 'GET' ? Math.max(0, options.retries ?? 2) : 0;
  const timeoutMs = options.timeoutMs ?? 15_000;
  let lastError: unknown;

  for (let attempt = 0; attempt <= retries; attempt += 1) {
    const controller = new AbortController();
    let timedOut = false;
    const forwardAbort = () => controller.abort();
    options.signal?.addEventListener('abort', forwardAbort, { once: true });
    const timer = window.setTimeout(() => { timedOut = true; controller.abort(); }, timeoutMs);
    try {
      const response = await fetch(url, { ...init, signal: controller.signal });
      const text = await response.text();
      let body: unknown;
      if (text) {
        try { body = JSON.parse(text); }
        catch { throw new ApiClientError('The server returned an unreadable response. Check the server log and retry.', 'invalid-response', response.status); }
      }
      if (!response.ok) {
        const error = responseError(response.status, serverDetail(body));
        if (response.status >= 500 || response.status === 429) lastError = error;
        else throw error;
      } else {
        return body as T;
      }
    } catch (cause) {
      if (cause instanceof ApiClientError) {
        if (cause.status !== 429 && (cause.status ?? 0) < 500) throw cause;
        lastError = cause;
      } else if (timedOut) {
        lastError = new ApiClientError(`The request timed out after ${Math.ceil(timeoutMs / 1000)} seconds. Narrow the date range or area and retry.`, 'timeout');
      } else if (options.signal?.aborted) {
        throw new ApiClientError('The request was cancelled because the selection changed.', 'aborted');
      } else {
        lastError = new ApiClientError(`Cannot reach the FIREWATCH API at ${new URL(url).origin}. Start the app with “npm run dev” from the project root, then retry.`, 'network');
      }
    } finally {
      window.clearTimeout(timer);
      options.signal?.removeEventListener('abort', forwardAbort);
    }
    if (attempt < retries) await new Promise(resolveDelay => window.setTimeout(resolveDelay, 250 * (attempt + 1)));
  }
  throw lastError instanceof ApiClientError ? lastError : new ApiClientError('The request failed. Retry or check the FIREWATCH API.', 'network');
}

export const apiGet = <T>(url: string, options?: RequestOptions) => apiRequest<T>(url, {}, options);
export const apiPost = <T>(url: string, body: BodyInit, options?: RequestOptions) => apiRequest<T>(url, { method: 'POST', body }, options);

export function errorMessage(error: unknown, fallback: string): string {
  return error instanceof ApiClientError ? error.message : fallback;
}
