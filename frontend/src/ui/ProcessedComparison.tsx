import { useEffect, useMemo, useRef, useState } from 'react';
import type { CSSProperties } from 'react';
import { AlertCircle, CalendarDays, LoaderCircle, Search, ShieldCheck } from 'lucide-react';
import { apiGet, errorMessage } from '../lib/apiClient';

type DailyUnion = { date: string; unique_detected_cell_days: number; modis_detected_cell_days: number; viirs_detected_cell_days: number; cross_sensor_overlap_cell_days: number };
type ProductDaily = { date: string; sensor_family: string; platform: string; product_type: string; detected_cell_days: number; raw_records: number; frp_sum_mw: number | null; frp_max_mw: number | null };
type CalendarResult = { status: string; calibration_status: string; calibration_reason: string; coverage_status: string; metric_definition: string; daily_union: DailyUnion[]; daily_by_product_platform: ProductDaily[]; data_status: string; method_version: string };
type Props = { api: string; apiStatus: 'starting' | 'online' | 'offline'; bbox?: string; onBboxChange?: (bbox: string) => void };

const platforms = ['Terra', 'Aqua', 'S-NPP', 'NOAA-20', 'NOAA-21'];

function dateRange(start: string, end: string): string[] {
  const from = new Date(`${start}T00:00:00Z`);
  const to = new Date(`${end}T00:00:00Z`);
  if (!Number.isFinite(from.getTime()) || !Number.isFinite(to.getTime()) || to < from || (to.getTime() - from.getTime()) / 86400000 > 365) return [];
  const days: string[] = [];
  for (let day = new Date(from); day <= to; day.setUTCDate(day.getUTCDate() + 1)) days.push(day.toISOString().slice(0, 10));
  return days;
}

export default function ProcessedComparison({ api, apiStatus, bbox: sharedBbox, onBboxChange }: Props) {
  const [start, setStart] = useState('2025-01-01');
  const [end, setEnd] = useState('2025-01-31');
  const [localBbox, setLocalBbox] = useState('');
  const bbox = sharedBbox ?? localBbox;
  const setBbox = (value: string) => { setLocalBbox(value); onBboxChange?.(value); };
  const [productType, setProductType] = useState<'SP' | 'NRT'>('SP');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [result, setResult] = useState<CalendarResult | null>(null);
  const [coverage, setCoverage] = useState<{ status: string; files_processed: number; files_discovered: number } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [coverageError, setCoverageError] = useState('');
  const [selectedDate, setSelectedDate] = useState('');
  const queryController = useRef<AbortController | null>(null);
  const dates = useMemo(() => dateRange(start, end), [start, end]);

  useEffect(() => {
    if (apiStatus !== 'online') { setCoverage(null); setCoverageError(''); return; }
    const controller = new AbortController();
    apiGet<{ status: string; files_processed: number; files_discovered: number }>(`${api}/api/data-quality`, { signal: controller.signal }).then(setCoverage)
      .catch(cause => { if (!controller.signal.aborted) { setCoverage(null); setCoverageError(errorMessage(cause, 'Could not read processed-data coverage.')); } });
    return () => controller.abort();
  }, [api, apiStatus]);
  useEffect(() => () => { queryController.current?.abort(); queryController.current = null; }, []);

  async function query() {
    if (apiStatus !== 'online') { setError('FIREWATCH API is offline. Start the app with npm run dev, then retry.'); return; }
    if (!dates.length) { setError('Choose a valid date window of at most 366 days.'); return; }
    setLoading(true); setError(''); setResult(null); setSelectedDate('');
    const params = new URLSearchParams({ start_date: start, end_date: end, product_type: productType });
    if (bbox.trim()) params.set('bbox', bbox.trim());
    selectedPlatforms.forEach(platform => params.append('platform', platform));
    queryController.current?.abort();
    const controller = new AbortController(); queryController.current = controller;
    const timeout = window.setTimeout(() => controller.abort(), 32000);
    try {
      const body = await apiGet<CalendarResult>(`${api}/api/calendar?${params}`, { signal: controller.signal, timeoutMs: 30_000, retries: 0 });
      setResult(body);
    } catch (cause) {
      if (controller.signal.aborted && queryController.current !== controller) return;
      setError(cause instanceof Error && cause.name === 'AbortError' ? 'The query timed out or was cancelled. Try a smaller date range or bounding box.' : errorMessage(cause, 'Could not load the local calendar. Check that the backend is running.'));
    } finally { window.clearTimeout(timeout); if (queryController.current === controller) { queryController.current = null; setLoading(false); } }
  }

  function exportComparison() {
    if (!result) return;
    const header = ['date', 'metric', 'sensor_family', 'platform', 'product_type', 'value', 'raw_records', 'frp_sum_mw', 'frp_max_mw'];
    const rows = result.daily_union.map(day => [day.date, 'unique_detected_cell_days', 'MODIS+VIIRS', '', productType, day.unique_detected_cell_days, '', '', '']);
    rows.push(...result.daily_by_product_platform.map(row => [row.date, 'sensor_detected_cell_days', row.sensor_family, row.platform, row.product_type, row.detected_cell_days, row.raw_records, row.frp_sum_mw ?? '', row.frp_max_mw ?? '']));
    const csv = [header, ...rows].map(row => row.map(value => { const text = String(value); const safe = /^[=+\-@]/.test(text) ? `'${text}` : text; return `"${safe.replace(/"/g, '""')}"`; }).join(',')).join('\n');
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    const link = document.createElement('a'); link.href = url; link.download = 'firewatch-processed-comparison.csv'; link.click(); URL.revokeObjectURL(url);
  }

  const byDate = new Map((result?.daily_union || []).map(day => [day.date, day]));
  const selectedRows = (result?.daily_by_product_platform || []).filter(row => row.date === selectedDate);
  const max = Math.max(1, ...Array.from(byDate.values(), day => day.unique_detected_cell_days));
  const total = (result?.daily_union || []).reduce((sum, day) => sum + day.unique_detected_cell_days, 0);
  const overlap = (result?.daily_union || []).reduce((sum, day) => sum + day.cross_sensor_overlap_cell_days, 0);

  return <section className="comparison-panel panel" id="sensor-comparison" aria-labelledby="comparison-title">
    <div className="comparison-heading"><div><span className="section-kicker">HARMONIZATION EXPLORER · LOCAL SENSOR COMPARISON</span><h2 id="comparison-title">Compare MODIS and VIIRS detections</h2><p>Harmonization aims to make measurements from different sensors meaningfully comparable. This view groups detections on a shared grid, but does not correct sensor differences or produce calibrated results.</p></div><span className="comparison-status"><ShieldCheck size={13}/>{coverage?.status === 'partial_local_archive' ? 'PARTIAL LOCAL ARCHIVE' : coverage?.status === 'indexed_local_archive' ? 'LOCAL ARCHIVE INDEXED' : 'COVERAGE UNKNOWN'}</span></div>
    <div className="comparison-controls">
      <label>Start date<input aria-label="Comparison start date" type="date" value={start} onChange={event => setStart(event.target.value)}/></label>
      <label>End date<input aria-label="Comparison end date" type="date" value={end} onChange={event => setEnd(event.target.value)}/></label>
      <label>AOI bbox · west,south,east,north<input aria-label="Area bounding box" placeholder="Blank = global" value={bbox} onChange={event => setBbox(event.target.value)}/></label>
      <label>Processing stream<select aria-label="Processing stream" value={productType} onChange={event => setProductType(event.target.value as 'SP' | 'NRT')}><option value="SP">Standard Processing</option><option value="NRT">Near Real-Time</option></select></label>
      <button className="comparison-query" onClick={query} disabled={loading||apiStatus!=='online'} title={apiStatus!=='online'?'API offline. Start with npm run dev.':''}><Search size={14}/>{loading ? 'Querying local data…' : 'Query processed data'}</button>
    </div>
    <fieldset className="platform-picker"><legend>Platforms · all available by default</legend>{platforms.map(platform => <label key={platform}><input type="checkbox" checked={selectedPlatforms.includes(platform)} onChange={event => setSelectedPlatforms(current => event.target.checked ? [...current, platform] : current.filter(value => value !== platform))}/>{platform}</label>)}</fieldset>
    {coverage && <p className="coverage-line">{coverage.files_processed.toLocaleString()} of {coverage.files_discovered.toLocaleString()} discovered files processed · missing rows do not mean zero activity.</p>}
    {coverageError && <p className="coverage-line" role="status">Coverage status unavailable: {coverageError}</p>}
    {apiStatus !== 'online' && <p className="coverage-line" role="status">Local API {apiStatus}. Start it with <code>npm run dev</code> from the project root to query extracted archives.</p>}
    <p className="coverage-line">The map and overview above use the source named in the page status. This panel summarizes processed cell-days; its aggregate results do not replace map points.</p>
    {loading && <div className="comparison-state" role="status"><LoaderCircle className="spin" size={17}/> Querying local Parquet; NASA services are not contacted.</div>}
    {error && <div className="comparison-error" role="alert"><AlertCircle size={16}/>{error}</div>}
    {!result && !loading && !error && <div className="comparison-state"><CalendarDays size={17}/>Choose a date window and query the local processed archive. The simulated demo above remains separate.</div>}
    {result && <>
      <div className="comparison-summary"><div><strong>{total.toLocaleString()}</strong><span>DETECTED CELL-DAYS</span></div><div><strong>{overlap.toLocaleString()}</strong><span>SAME-CELL / DATE OVERLAP</span></div><div><strong>{result.daily_union.length}</strong><span>DATES WITH DETECTIONS</span></div><p>{result.calibration_status.replace(/_/g, ' ').toUpperCase()} · {result.method_version}</p><button className="comparison-export" onClick={exportComparison}>Export comparison CSV</button></div>
      <div className="comparison-days" role="group" aria-label="Daily detected cell-day calendar">{dates.map(day => { const item = byDate.get(day); return <button key={day} className={item ? 'comparison-day has-value' : 'comparison-day no-value'} aria-label={item ? `${day}: ${item.unique_detected_cell_days} detected cell-days` : `${day}: no detection row; coverage unknown`} title={item ? `${item.unique_detected_cell_days.toLocaleString()} detected cell-days · click to inspect sensor records` : 'No detection row returned. Observation opportunity is unknown.'} onClick={() => item && setSelectedDate(day)} disabled={!item} style={item ? { '--day-intensity': 0.2 + 0.8 * item.unique_detected_cell_days / max } as CSSProperties : undefined}><span>{day.slice(-2)}</span><i>{item ? item.unique_detected_cell_days.toLocaleString() : '?'}</i></button>; })}</div>
      <p className="coverage-line">{result.coverage_status}. Dates with no detection row are shown as unknown, not as zero.</p>
      {selectedDate && <div className="platform-results"><h3>{selectedDate} · source-specific records</h3>{selectedRows.length ? <div className="table-scroll"><table><thead><tr><th>Sensor</th><th>Platform</th><th>Cell-days</th><th>Raw records</th><th>FRP sum (MW)</th></tr></thead><tbody>{selectedRows.map((row, index) => <tr key={`${row.sensor_family}-${row.platform}-${index}`}><td>{row.sensor_family}</td><td>{row.platform}</td><td>{row.detected_cell_days.toLocaleString()}</td><td>{row.raw_records.toLocaleString()}</td><td>{row.frp_sum_mw == null ? '—' : row.frp_sum_mw.toLocaleString(undefined, { maximumFractionDigits: 1 })}</td></tr>)}</tbody></table></div> : <p>No source rows were returned for this date.</p>}</div>}
      <p className="comparison-method">{result.metric_definition} {result.calibration_reason}</p>
    </>}
  </section>;
}
