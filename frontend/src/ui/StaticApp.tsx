import { lazy, Suspense, useEffect, useMemo, useRef, useState } from 'react';
import { Activity, AlertTriangle, CalendarDays, CircleHelp, Download, Flame, Info, Search, ShieldAlert } from 'lucide-react';
import HarmonizedAnalytics, { type HarmonizedMode, type HarmonizedSeries } from './HarmonizedAnalytics';
import '../static.css';

type Country = { name: string; slug: string; coverage_years: number[]; first_date: string | null; last_date: string | null; products: string[]; platforms: string[]; processed_source_files: number; observed_bbox: number[] | null; observed_centroid_lon_lat: [number, number] | null };
type MapActivity = { name: string; activity_by_year: Array<{ year: number; modis_detections: number; viirs_detections: number; modis_frp_sum_mw: number; viirs_frp_sum_mw: number }>; activity_by_month: Array<{ year: number; month: number; modis_detections: number; viirs_detections: number; modis_frp_sum_mw: number; viirs_frp_sum_mw: number }>; coverage_by_product_year: Coverage[] };
type Catalog = { data_status: string; countries: Country[] };
type MapCatalog = { countries: MapActivity[] };
type Daily = [string, 'MODIS' | 'VIIRS', string, 'SP', number, number, number | null, number, number, number, number, number, number, number, number, number, boolean, boolean, boolean];
type Grid = [number, 'MODIS' | 'VIIRS', string, 'SP', number, number, number, number];
type Coverage = { country: string; product: string; year: number; expected: number; processed: number; rows: number; status: string };
type Series = { country: string; data_status: string; coverage: { first_date: string | null; last_date: string | null; years: number[]; products: string[]; platforms: string[]; processed_source_files: number; source_rows_processed: number; by_product_year: Coverage[] }; daily: Daily[]; grid: Grid[]; source_files: Array<{ source_file: string; file_id: string; product: string; platform_product_label: string; year: number; rows_source: number; rows_processed: number; processing_versions: string[] }>; metric_definition: string; harmonization_status: string; grid_definition: string };
type MethodStats = { median_r2: number | null; median_holdout_mdape: number | null; confidence_counts: Record<string, number>; median_continuity_ratio_before: number | null; median_continuity_ratio_after: number | null };
type MethodsValidation = { method_version: string; validation_metrics: MethodStats; thresholds: { minimum_weekly_frp_mw_per_family: number; minimum_country_overlap_weeks: number }; plain_language_rule: string };
type Metric = 'detections' | 'frp';
type Sensor = 'All' | 'MODIS' | 'VIIRS';
const base = import.meta.env.BASE_URL;
const displayCountry = (name: string) => name.replace(/_/g, ' ');
const GlobalMap = lazy(() => import('./GlobalMap'));

async function fetchJson<T>(url: string, label: string): Promise<T> {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${label} request failed (HTTP ${response.status}).`);
  const contentType = response.headers.get('content-type') || '';
  if (!/(?:application\/json|\+json)(?:\s*;|$)/i.test(contentType)) {
    throw new Error(`${label} did not return JSON (received ${contentType || 'an unknown content type'}). The static data file may be missing; rebuild the packaged data and reload.`);
  }
  try {
    return await response.json() as T;
  } catch {
    throw new Error(`${label} contains invalid JSON. Rebuild the packaged data and reload.`);
  }
}

function safeCell(value: unknown): string {
  const text = String(value ?? '');
  return /^[=+@\-\t\r]/.test(text) ? `'${text}` : text;
}
function saveBlob(blob: Blob, name: string) {
  const url = URL.createObjectURL(blob); const link = document.createElement('a'); link.href = url; link.download = name; link.click(); URL.revokeObjectURL(url);
}
function coverageStatus(series: Series, year: number, sensor: Sensor) {
  const rows = series.coverage.by_product_year.filter(item => item.year === year && (sensor === 'All' || item.product.startsWith(sensor)));
  if (!rows.length) return 'missing';
  return rows.every(item => item.expected > 0 && item.processed === item.expected) ? 'complete' : 'partial';
}

export default function StaticApp() {
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [series, setSeries] = useState<Series | null>(null);
  const [harmonized, setHarmonized] = useState<HarmonizedSeries | null>(null);
  const [methods, setMethods] = useState<MethodsValidation | null>(null);
  const [mode, setMode] = useState<HarmonizedMode>('raw');
  const [countryName, setCountryName] = useState('');
  const [year, setYear] = useState(0);
  const [mapMonth, setMapMonth] = useState(0);
  const [metric, setMetric] = useState<Metric>('detections');
  const [sensor, setSensor] = useState<Sensor>('All');
  const [selectedDate, setSelectedDate] = useState('');
  const [loadingCatalog, setLoadingCatalog] = useState(true);
  const [loadingSeries, setLoadingSeries] = useState(false);
  const [error, setError] = useState('');
  const [showMethod, setShowMethod] = useState(false);
  const [query, setQuery] = useState('');
  const mapAnchorRef = useRef<HTMLDivElement>(null);
  const [mapReady, setMapReady] = useState(false);
  const [mapCatalog, setMapCatalog] = useState<MapCatalog | null>(null);
  const [mapDataError, setMapDataError] = useState('');
  const [harmonizedError, setHarmonizedError] = useState('');

  useEffect(() => {
    const anchor = mapAnchorRef.current;
    if (!anchor) return;
    if (!('IntersectionObserver' in window)) { setMapReady(true); return; }
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) { setMapReady(true); observer.disconnect(); }
    }, { rootMargin: '240px' });
    observer.observe(anchor);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    let cancelled = false;
    fetchJson<MethodsValidation>(`${base}data/methods_validation.json`, 'Calibration validation')
      .then(body => { if (!cancelled) setMethods(body); })
      .catch(cause => { if (!cancelled) setHarmonizedError(cause instanceof Error ? cause.message : 'Calibration summary could not be loaded.'); });
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    if (!mapReady || mapCatalog) return;
    let cancelled = false;
    fetchJson<MapCatalog>(`${base}data/map_activity.json`, 'Map activity data')
      .then(body => { if (!cancelled) setMapCatalog(body); })
      .catch(cause => { if (!cancelled) setMapDataError(cause instanceof Error ? cause.message : 'Map activity data could not be loaded.'); });
    return () => { cancelled = true; };
  }, [mapReady, mapCatalog]);

  useEffect(() => {
    let cancelled = false;
    fetchJson<Catalog>(`${base}data/countries.json`, 'Country index')
      .then((body: Catalog) => { if (cancelled) return; setCatalog(body); const first = body.countries.find(item => item.name === 'Australia') || body.countries[0]; if (first) setCountryName(first.name); })
      .catch(cause => { if (!cancelled) setError(cause instanceof Error ? cause.message : 'Could not load the local data index.'); })
      .finally(() => { if (!cancelled) setLoadingCatalog(false); });
    return () => { cancelled = true; };
  }, []);

  const selectedCountry = catalog?.countries.find(item => item.name === countryName);
  useEffect(() => {
    if (!selectedCountry) return;
    let cancelled = false;
    setHarmonized(null); setHarmonizedError('');
    fetchJson<HarmonizedSeries>(`${base}data/harmonized/${selectedCountry.slug}.json`, `Calibration for ${displayCountry(selectedCountry.name)}`)
      .then(body => { if (!cancelled) setHarmonized(body); })
      .catch(cause => { if (!cancelled) setHarmonizedError(cause instanceof Error ? cause.message : 'Country calibration could not be loaded.'); });
    return () => { cancelled = true; };
  }, [selectedCountry]);
  useEffect(() => {
    if (!selectedCountry) return;
    let cancelled = false;
    setLoadingSeries(true); setError(''); setSeries(null); setSelectedDate('');
    fetchJson<Series>(`${base}data/series/${selectedCountry.slug}.json`, `Series for ${displayCountry(selectedCountry.name)}`)
      .then((body: Series) => { if (cancelled) return; setSeries(body); setYear(body.coverage.years[body.coverage.years.length - 1] || 0); })
      .catch(cause => { if (!cancelled) setError(cause instanceof Error ? cause.message : 'Could not load this country series.'); })
      .finally(() => { if (!cancelled) setLoadingSeries(false); });
    return () => { cancelled = true; };
  }, [selectedCountry]);

  const days = useMemo(() => {
    const totals = new Map<string, { MODIS: number; VIIRS: number; frpMODIS: number; frpVIIRS: number }>();
    for (const row of series?.daily || []) {
      if (Number(row[0].slice(0, 4)) !== year) continue;
      const item = totals.get(row[0]) || { MODIS: 0, VIIRS: 0, frpMODIS: 0, frpVIIRS: 0 };
      item[row[1]] += row[4]; item[row[1] === 'MODIS' ? 'frpMODIS' : 'frpVIIRS'] += row[5]; totals.set(row[0], item);
    }
    const count = year ? (new Date(Date.UTC(year, 1, 29)).getUTCDate() === 29 ? 366 : 365) : 365;
    const calibratedDays = new Map((harmonized?.daily || []).map(row => [row.date, row]));
    return Array.from({ length: count }, (_, index) => {
      const date = new Date(Date.UTC(year, 0, index + 1)).toISOString().slice(0, 10); const value = totals.get(date);
      const visible = sensor === 'All' ? (value?.MODIS || 0) + (value?.VIIRS || 0) : value?.[sensor] || 0;
      const frpValue = sensor === 'All' ? (value?.frpMODIS || 0) + (value?.frpVIIRS || 0) : value?.[`frp${sensor}` as 'frpMODIS' | 'frpVIIRS'] || 0;
      const calibrated = calibratedDays.get(date);
      const useHarmonizedFrp = mode === 'harmonized' && metric === 'frp';
      return { date, value: useHarmonizedFrp ? calibrated?.harmonized_frp_daily || 0 : metric === 'detections' ? visible : frpValue,
        available: !useHarmonizedFrp || calibrated?.harmonized_frp_daily !== null && calibrated?.harmonized_frp_daily !== undefined,
        MODIS: value?.MODIS || 0, VIIRS: value?.VIIRS || 0,
        frpMODIS: value?.frpMODIS || 0, frpVIIRS: value?.frpVIIRS || 0,
        scaledVIIRS: calibrated?.scaled_viirs_frp ?? null, dailyScale: calibrated?.daily_scale_for_viirs ?? null };
    });
  }, [series, harmonized, year, sensor, metric, mode]);
  const max = Math.max(1, ...days.filter(day => day.available).map(day => day.value));
  const yearTotals = useMemo(() => (series?.coverage.years || []).map(itemYear => {
    const rows = (series?.daily || []).filter(row => Number(row[0].slice(0, 4)) === itemYear);
    return { year: itemYear, MODIS: rows.filter(row => row[1] === 'MODIS').reduce((sum, row) => sum + row[4], 0), VIIRS: rows.filter(row => row[1] === 'VIIRS').reduce((sum, row) => sum + row[4], 0), coverage: coverageStatus(series!, itemYear, 'All') };
  }), [series]);
  const selected = days.find(day => day.date === selectedDate);
  const yearCoverage = series ? coverageStatus(series, year, sensor) : 'missing';

  function exportCsv() {
    if (!series) return;
    const header = ['acq_date_utc','sensor_family','platform','product_type','n_detections','frp_sum_mw','day_fraction','vegetation_n_detections','vegetation_frp_sum_mw','high_quality_n_detections','high_quality_frp_sum_mw','day_n_detections','day_frp_sum_mw','night_n_detections','night_frp_sum_mw','platform_day_observed','type_available','confidence_available','daynight_available','country','source_file','source_file_id','source_product','processing_version','method_version','harmonization_status'];
    const rows = series.daily.filter(row => Number(row[0].slice(0, 4)) === year && (sensor === 'All' || row[1] === sensor)).map(row => {
      const product = row[1] === 'MODIS' ? 'MODIS_SP' : row[2] === 'NOAA-20' ? 'VIIRS_NOAA20_SP' : row[2] === 'S-NPP' ? 'VIIRS_SNPP_SP' : '';
      const source = series.source_files.find(item => item.year === year && item.product === product);
      return [...row, series.country, source?.source_file || '', source?.file_id || '', product, source?.processing_versions.join('; ') || '', 'firewatch-static-0.2', 'not applied'];
    });
    const text = [header, ...rows].map(row => row.map(value => `"${safeCell(value).replace(/"/g, '""')}"`).join(',')).join('\r\n');
    saveBlob(new Blob([text], { type: 'text/csv;charset=utf-8' }), `firewatch-${selectedCountry?.slug}-${year}-source-series.csv`);
  }
  function exportCalendarPng() {
    const canvas = document.createElement('canvas'); const cell = 12; const gap = 2; const left = 64; canvas.width = left + days.length * (cell + gap); canvas.height = 90;
    const ctx = canvas.getContext('2d'); if (!ctx) return;
    ctx.fillStyle = '#101712'; ctx.fillRect(0, 0, canvas.width, canvas.height); ctx.fillStyle = '#e8efdf'; ctx.font = '16px sans-serif'; ctx.fillText(`FIREWATCH · ${countryName} · ${year} · ${metric === 'frp' ? 'FRP sum (MW)' : 'detections'}`, 16, 28);
    ctx.fillStyle = '#a6b1a5'; ctx.font = '11px sans-serif'; ctx.fillText('Source detections; sensor families are not calibrated or harmonized.', 16, 49);
    days.forEach((day, i) => { const shade = Math.log1p(day.value) / Math.log1p(max); ctx.fillStyle = day.value ? `hsl(${84 - shade * 58} 68% ${30 + shade * 22}%)` : '#28332b'; ctx.fillRect(left + i * (cell + gap), 62, cell, cell); });
    canvas.toBlob(blob => { if (blob) saveBlob(blob, `firewatch-${selectedCountry?.slug}-${year}-calendar.png`); });
  }

  const filteredCountries = (catalog?.countries || []).filter(item => item.name.toLowerCase().includes(query.toLowerCase()));
  return <main className="firewatch-static">
    <header className="fw-header">
      <div className="fw-brand"><span className="fw-logo"><Flame size={21}/></span><div><strong>FIREWATCH</strong><span>GLOBAL BURNING ACTIVITY MONITOR</span></div></div>
      <p>Explore NASA FIRMS active-fire records by place and time.</p>
      <div className="fw-header-actions"><span className="fw-status"><i/>FIRMS SP · CALIBRATION</span><button className="fw-help" onClick={() => setShowMethod(true)}><CircleHelp size={15}/> How it works</button></div>
    </header>

    <section className="fw-notice" role="status"><ShieldAlert size={18}/><div><b>Coverage: 2020–2025, MODIS, S-NPP, NOAA-20.</b></div><span className="fw-version">FIRMS SP</span></section>

    <div className="fw-layout">
      <aside className="fw-sidebar">
        <div className="fw-sidebar-title"><Search size={15}/> SELECT AREA</div>
        <label className="fw-label" htmlFor="country-search">Country</label>
        <input id="country-search" className="fw-input" value={query} placeholder="Search country…" onChange={event => { const value = event.target.value; setQuery(value); const match = catalog?.countries.find(item => displayCountry(item.name).toLowerCase() === value.toLowerCase()); if (match) setCountryName(match.name); }} list="country-options" disabled={loadingCatalog}/>
        <datalist id="country-options">{filteredCountries.map(item => <option key={item.slug} value={displayCountry(item.name)}/>)}</datalist>
        <label className="fw-label" htmlFor="country-picker">Available country series</label>
        <select id="country-picker" className="fw-input" value={countryName} onChange={event => { setCountryName(event.target.value); setQuery(''); }} disabled={!catalog?.countries.length}>
          {(query ? filteredCountries : catalog?.countries || []).map(item => <option key={item.slug} value={item.name}>{displayCountry(item.name)} · {item.coverage_years.join(', ')}</option>)}
        </select>
        <div className="fw-side-card"><span>OBSERVED RECORD EXTENT</span><b>{selectedCountry?.first_date || '—'} → {selectedCountry?.last_date || '—'}</b><small>{selectedCountry?.processed_source_files ?? 0} processed country files</small><small>Coordinates show detections, not a country boundary.</small></div>
        <div className="fw-divider"/>
        <label className="fw-label" htmlFor="year-picker">Year</label>
        <select id="year-picker" className="fw-input" value={year} onChange={event => { setYear(Number(event.target.value)); setSelectedDate(''); }} disabled={!series}>{(series?.coverage.years || []).map(value => <option key={value} value={value}>{value}</option>)}</select>
        <label className="fw-label" htmlFor="sensor-picker">Sensor family</label>
        <select id="sensor-picker" className="fw-input" value={sensor} disabled={mode === 'harmonized'} onChange={event => setSensor(event.target.value as Sensor)}><option>All</option><option>MODIS</option><option>VIIRS</option></select>
        <label className="fw-label" htmlFor="metric-picker">Displayed metric</label>
        <select id="metric-picker" className="fw-input" value={metric} onChange={event => setMetric(event.target.value as Metric)}><option value="detections">Source detections</option><option value="frp">FRP sum (MW)</option></select>
        <div className={`fw-coverage fw-coverage-${yearCoverage}`}><span>FILE COVERAGE</span><b>{yearCoverage === 'complete' ? 'Complete source-file set' : yearCoverage === 'partial' ? 'Partial source-file set' : 'No source file coverage'}</b><small>Completeness is checked against extracted FIRMS filenames. This does not imply continuous satellite observation.</small></div>
        <button className="fw-export" onClick={exportCsv} disabled={!series}><Download size={15}/> Export selected year CSV</button>
        <button className="fw-export fw-export-secondary" onClick={exportCalendarPng} disabled={!series}><Download size={15}/> Save calendar PNG</button>
        <p className="fw-sidebar-note">Dataset access is local and static. No API key, NASA request, or backend is used by this dashboard.</p>
      </aside>

      <div className="fw-main">
        {loadingCatalog && <div className="fw-state">Loading the packaged data index…</div>}
        {loadingSeries && <div className="fw-state">Loading {countryName} source series…</div>}
        {error && <div className="fw-error" role="alert"><AlertTriangle size={18}/><div><b>Data could not be loaded</b><span>{error}</span></div></div>}
        {!catalog?.countries.length && !loadingCatalog && !error && <div className="fw-empty">No country summary is packaged yet. See README for the local build command.</div>}

        {series && !loadingSeries && <>
          <section className="fw-hero fw-panel">
            <div className="fw-section-head"><div><span className="fw-kicker"><Activity size={13}/> ACTIVITY CALENDAR</span><h1>Burning activity · {displayCountry(series.country)}</h1><p>Daily source records grouped by acquisition date (UTC). Empty dates mean no packaged detections, not confirmed absence of fire.</p></div><div className="fw-calendar-badges"><span className={`fw-pill fw-pill-${yearCoverage}`}>{yearCoverage.toUpperCase()} COVERAGE</span><span className={`fw-pill fw-confidence-${(harmonized?.confidence || 'loading').toLowerCase()}`} aria-label={`Calibration confidence: ${harmonized?.confidence || 'loading'}`}>{harmonized ? `${harmonized.confidence.toUpperCase()} CONFIDENCE` : 'LOADING CONFIDENCE'}</span></div></div>
            <div className="fw-mode-toggle" role="group" aria-label="Calendar calibration mode"><button type="button" aria-pressed={mode === 'raw'} onClick={() => setMode('raw')}>Raw sensors</button><button type="button" aria-pressed={mode === 'harmonized'} disabled={!harmonized} onClick={() => { setMode('harmonized'); setSensor('All'); }}>Harmonized</button></div>
            <div className="fw-sensor-legend"><span><i className="fw-dot modis"/>MODIS</span><span><i className="fw-dot viirs"/>VIIRS</span><span>Selection: {mode === 'harmonized' ? 'Combined FRP' : sensor} · {metric === 'frp' ? 'FRP sum (MW)' : 'detections'}</span></div>
            <div className="fw-calendar-scroll"><div className="fw-doy-labels"><span>JAN</span><span>MAR</span><span>MAY</span><span>JUL</span><span>SEP</span><span>NOV</span></div><div className="fw-calendar-row" role="group" aria-label={`${year} activity calendar, days of year`}>
              {days.map(day => { const active = day.value > 0 && day.available; const intensity = active ? Math.min(4, Math.ceil(Math.log1p(day.value) / Math.log1p(max) * 4)) : 0; const selectedClass = selectedDate === day.date ? ' is-selected' : ''; const emptyNote = !day.available ? ' · not calibrated for this week' : active ? '' : ' · no packaged detection; not evidence of no fire'; const viirsValue = mode === 'harmonized' && metric === 'frp' ? day.scaledVIIRS : day.frpVIIRS; const tip = `${day.date} · MODIS ${metric === 'frp' ? `${day.frpMODIS.toFixed(1)} MW` : day.MODIS.toLocaleString()} · VIIRS ${metric === 'frp' ? `${viirsValue === null ? 'unavailable' : viirsValue.toFixed(1)} MW${mode === 'harmonized' && day.dailyScale !== null ? ` (scale ${day.dailyScale.toFixed(3)})` : ''}` : day.VIIRS.toLocaleString()} · ${yearCoverage} source-file coverage${emptyNote}`; const labelValue = !day.available ? 'not calibrated' : metric === 'frp' ? `${day.value.toFixed(1)} MW FRP` : `${day.value.toLocaleString()} detections`; return <button key={day.date} type="button" aria-label={`${day.date}: ${labelValue}${active ? '' : emptyNote}`} title={tip} onClick={() => setSelectedDate(day.date)} className={`fw-day intensity-${intensity}${!day.available ? ' is-uncalibrated' : ''}${selectedClass}${yearCoverage !== 'complete' ? ' coverage-partial' : ''}`} />; })}
            </div></div>
            <div className="fw-calendar-foot"><span>{mode === 'harmonized' ? metric === 'frp' ? 'Daily VIIRS FRP is scaled by its week’s factor; weeks outside the operating rule are blank.' : 'Detection counts remain raw; this calibration is for FRP only.' : 'Click a date for sensor-specific totals. Cell color is scaled within this selected year.'}</span><button onClick={exportCalendarPng}><Download size={13}/> PNG</button></div>
            {selected && <div className="fw-day-detail" aria-live="polite"><CalendarDays size={16}/><b>{selected.date}</b><span>MODIS: {metric === 'frp' ? `${selected.frpMODIS.toFixed(1)} MW` : `${selected.MODIS.toLocaleString()} detections`}</span><span>VIIRS: {metric === 'frp' ? `${mode === 'harmonized' ? selected.scaledVIIRS === null ? 'uncalibrated' : `${selected.scaledVIIRS.toFixed(1)} scaled MW` : `${selected.frpVIIRS.toFixed(1)} MW`}` : `${selected.VIIRS.toLocaleString()} detections`}</span>{yearCoverage !== 'complete' && <em>Partial coverage — values are observed records only.</em>}</div>}
          </section>

          <div className="fw-two-col">
            <section className="fw-panel fw-map-panel"><div className="fw-section-head"><div><span className="fw-kicker">SPATIAL OVERVIEW</span><h2>Global activity by country</h2><p>Bubble location is an observed-record centroid; click a point to select that country.</p></div></div><label className="fw-map-time">Map period <input aria-label="Map month" type="range" min="0" max="12" step="1" value={mapMonth} onChange={event => setMapMonth(Number(event.target.value))}/><b>{mapMonth ? new Date(Date.UTC(2020, mapMonth - 1, 1)).toLocaleString('en', { month: 'long' }) : 'Full year'} · {year}</b></label><div ref={mapAnchorRef}>{mapReady ? mapCatalog ? <Suspense fallback={<div className="fw-map fw-map-loading" role="status">Loading the activity map…</div>}><GlobalMap countries={catalog?.countries || []} activity={mapCatalog.countries} year={year} month={mapMonth} metric={metric} sensor={sensor} selectedCountry={countryName} onSelect={name => { setCountryName(name); setQuery(''); }}/></Suspense> : <div className="fw-map fw-map-loading" role={mapDataError ? 'alert' : 'status'}>{mapDataError || 'Loading map activity data…'}</div> : <button className="fw-map fw-map-loading" type="button" onClick={() => setMapReady(true)}>Load interactive map</button>}</div></section>
            <section className="fw-panel fw-history"><div className="fw-section-head"><div><span className="fw-kicker">HISTORICAL RECORDS</span><h2>Processed source totals</h2><p>Counts by archive year · incomplete years are marked.</p></div></div><div className="fw-year-chart">{yearTotals.map(row => { const maxValue = Math.max(1, ...yearTotals.map(item => Math.max(item.MODIS, item.VIIRS))); return <div className="fw-year-line" key={row.year}><b>{row.year}</b><div className="fw-bars"><i className="fw-bar modis" style={{ width: `${Math.max(1, row.MODIS / maxValue * 100)}%` }} title={`MODIS ${row.MODIS.toLocaleString()}`}/><i className="fw-bar viirs" style={{ width: `${Math.max(1, row.VIIRS / maxValue * 100)}%` }} title={`VIIRS ${row.VIIRS.toLocaleString()}`}/></div><span>{row.coverage === 'complete' ? 'complete' : 'partial'}</span></div>})}</div><div className="fw-legend-small"><span><i className="fw-dot modis"/>MODIS detections</span><span><i className="fw-dot viirs"/>VIIRS detections</span></div></section>
          </div>

          <div className="fw-two-col">
            <section className="fw-panel fw-harmonization"><span className="fw-kicker"><Info size={13}/> HARMONIZATION · {methods?.method_version || 'validation summary unavailable'}</span><h2>Statistical cross-sensor calibration, validated leave-one-year-out</h2><p>Median country R²: {methods?.validation_metrics?.median_r2?.toFixed(3) ?? '—'} · median holdout MdAPE: {methods?.validation_metrics?.median_holdout_mdape === null || methods?.validation_metrics?.median_holdout_mdape === undefined ? '—' : `${(methods.validation_metrics.median_holdout_mdape * 100).toFixed(1)}%`}.</p><div className="fw-method-status"><ShieldAlert size={16}/><div><b>{displayCountry(countryName)} confidence: {harmonized?.confidence || 'loading'}</b><small>High {methods?.validation_metrics?.confidence_counts.High ?? '—'} · Medium {methods?.validation_metrics?.confidence_counts.Medium ?? '—'} · Low {methods?.validation_metrics?.confidence_counts.Low ?? '—'} country calibrations. {harmonizedError || 'Confidence is based on the documented fit and holdout thresholds.'}</small></div></div><p>Not a physical retrieval correction. Weeks with no fire in either sensor are not part of the fit.</p><button className="fw-text-button" onClick={() => setShowMethod(true)}>Read method and limitations →</button></section>
          </div>

          {harmonized && <HarmonizedAnalytics data={harmonized} year={year} mode={mode}/>}

          <section className="fw-panel fw-provenance"><span className="fw-kicker">SOURCE AND PROVENANCE</span><h2>What these values represent</h2><p>{series.metric_definition} The 1° map cells are display aggregates; they are not fire boundaries and do not correct the difference between MODIS and VIIRS pixel sizes.</p><div className="fw-prov-grid"><div><span>PROCESSING</span><b>Standard Processing (SP)</b></div><div><span>OBSERVED SATELLITES</span><b>{series.coverage.platforms.join(', ') || 'None'}</b></div><div><span>SOURCE FILES</span><b>{series.coverage.processed_source_files}</b></div><div><span>ROWS IN INPUT FILES</span><b>{series.coverage.source_rows_processed.toLocaleString()}</b></div></div><details><summary>Show source files and processing provenance ({series.source_files.length})</summary><div className="fw-source-list">{series.source_files.map(source => <div key={source.file_id}><code>{source.source_file}</code><span>{source.platform_product_label} · {source.year} · {source.rows_processed.toLocaleString()} rows · {source.processing_versions.join(', ') || 'version not recorded'}</span></div>)}</div></details></section>
        </>}
      </div>
    </div>
    <footer className="fw-footer"><span>FIREWATCH · NASA SPACE APPS CHALLENGE</span><span>Static data snapshot · NOAA-21 global files excluded from country series</span><span>FIRMS data citation and product guides are in the documentation.</span></footer>

    {showMethod && <div className="fw-modal-backdrop" role="presentation" onClick={event => { if (event.target === event.currentTarget) setShowMethod(false); }}><section className="fw-modal" role="dialog" aria-modal="true" aria-labelledby="fw-modal-title"><button className="fw-modal-close" onClick={() => setShowMethod(false)} aria-label="Close method dialog">×</button><span className="fw-kicker">METHOD · VERSION firewatch-static-0.1</span><h2 id="fw-modal-title">How FIREWATCH handles these records</h2><ol><li>Read validated local FIRMS Standard Processing Parquet files and preserve source product, platform, acquisition date and processing version.</li><li>Aggregate detections and FRP by country source file, UTC date, sensor family and platform. Missing source files/dates are not silently filled with zero.</li><li>Display a separate one-degree spatial aggregation to make the map legible. This does not equalize the native MODIS and VIIRS footprints.</li><li>Do not calculate a MODIS-equivalent index, anomaly, trend or fire season until the official product documentation, complete inputs, calibration design and holdout validation are reviewed.</li></ol><div className="fw-modal-warning"><AlertTriangle size={17}/><span>Coverage is partial. The source ZIP archive folder is empty in this workspace, so extracted CSVs are retained and the missing-year coverage cannot be restored from local archives.</span></div><p>FRP sums from different sensors are not directly comparable. FIRMS active-fire detections are not fire perimeters or a complete census of fires.</p><button className="fw-close-action" onClick={() => setShowMethod(false)}>Close</button></section></div>}
  </main>;
}
