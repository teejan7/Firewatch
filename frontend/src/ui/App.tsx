import { lazy, Suspense, useEffect, useMemo, useState } from 'react';
import { Activity, ArrowDownToLine, CalendarDays, ChevronDown, CircleHelp, Flame, Layers2, MapPin, Menu, Satellite, SlidersHorizontal, Upload, X } from 'lucide-react';
import { demoRecords } from '../data/demo';
import type { FireRecord } from '../data/demo';
import { csvFor, filterRecords, withDateBound } from '../lib/filters';
import { apiGet, apiPost, errorMessage } from '../lib/apiClient';
import ProcessedComparison from './ProcessedComparison';
import DataExplorer from './DataExplorer';

const regions = ['All regions', 'South America', 'North America', 'Oceania', 'Asia', 'Africa', 'Europe'];
const initial = { region: 'All regions', sensor: 'All sensors', start: '2026-10-01', end: '2026-10-31' };
const api = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const liveSources = ['VIIRS_NOAA21_NRT', 'VIIRS_NOAA20_NRT', 'MODIS_NRT'];
const archiveSources = ['VIIRS_NOAA21_SP', 'VIIRS_NOAA20_SP', 'VIIRS_SNPP_SP', 'MODIS_SP'];
const localYears = Array.from({ length: 26 }, (_, i) => 2025 - i);
type LocalProduct = { id: string; sensor: string; label: string };
type ApiStatus = 'starting' | 'online' | 'offline';
type ApiHealth = { firms_api_configured: boolean; local_analytics_available: boolean; data_status: string };
type CatalogResponse = { countries: string[]; products: LocalProduct[] };
const MapView = lazy(() => import('./MapView'));
const TimelineChart = lazy(() => import('./TimelineChart'));

export default function App() {
  const [filters, setFilters] = useState(initial);
  const [records, setRecords] = useState<FireRecord[]>(demoRecords);
  const [dataStatus, setDataStatus] = useState('Simulated demo data');
  const [dataNote, setDataNote] = useState('Illustrative records for exploring the interface. These are not NASA satellite observations.');
  const [uploadStatus, setUploadStatus] = useState('');
  const [liveSource, setLiveSource] = useState(liveSources[0]);
  const [liveDays, setLiveDays] = useState(1);
  const [liveLoading, setLiveLoading] = useState(false);
  const [archiveSource, setArchiveSource] = useState(archiveSources[0]);
  const [archiveDate, setArchiveDate] = useState('');
  const [archiveDays, setArchiveDays] = useState(1);
  const [archiveLoading, setArchiveLoading] = useState(false);
  const [localCountries, setLocalCountries] = useState<string[]>([]);
  const [localProducts, setLocalProducts] = useState<LocalProduct[]>([]);
  const [localCountry, setLocalCountry] = useState('India');
  const [localYear, setLocalYear] = useState(2025);
  const [localSource, setLocalSource] = useState('ALL');
  const [localStart, setLocalStart] = useState('2025-01-01');
  const [localEnd, setLocalEnd] = useState('2025-01-05');
  const [localLoading, setLocalLoading] = useState(false);
  const [localCalendar, setLocalCalendar] = useState<Record<string, number>>({});
  const [localCalendarKey, setLocalCalendarKey] = useState('');
  const [localCalendarProducts, setLocalCalendarProducts] = useState<string[]>([]);
  const [localCalendarLoading, setLocalCalendarLoading] = useState(false);
  const [localCalendarMessage, setLocalCalendarMessage] = useState('');
  const [mobileFilters, setMobileFilters] = useState(false);
  const [comparisonBbox, setComparisonBbox] = useState('');
  const [apiStatus, setApiStatus] = useState<ApiStatus>('starting');
  const [apiHealth, setApiHealth] = useState<ApiHealth | null>(null);
  const [apiRetry, setApiRetry] = useState(0);
  const [catalogError, setCatalogError] = useState('');
  const apiAvailable = apiStatus === 'online';
  const firmsAvailable = apiAvailable && Boolean(apiHealth?.firms_api_configured);
  useEffect(() => {
    let stopped = false;
    let timer = 0;
    let delay = 500;
    const check = async () => {
      try {
        const health = await apiGet<ApiHealth>(`${api}/api/health`, { timeoutMs: 3_000, retries: 0 });
        if (stopped) return;
        setApiHealth(health);
        setApiStatus('online');
        delay = 10_000;
      } catch {
        if (stopped) return;
        setApiHealth(null);
        setApiStatus('offline');
        delay = Math.min(delay * 2, 15_000);
      }
      if (!stopped) timer = window.setTimeout(check, delay);
    };
    void check();
    return () => { stopped = true; window.clearTimeout(timer); };
  }, [api, apiRetry]);
  useEffect(() => {
    if (apiStatus !== 'online') return;
    let cancelled = false;
    setCatalogError('');
    apiGet<CatalogResponse>(`${api}/api/local-archive/catalog?year=${localYear}`).then(data => {
      if (cancelled) return;
      const countries = Array.isArray(data.countries) ? data.countries as string[] : [];
      const products = Array.isArray(data.products) ? data.products as LocalProduct[] : [];
      setLocalCountries(countries);
      setLocalProducts(products);
      setLocalCountry(current => countries.includes(current) ? current : (countries[0] || ''));
      setLocalSource(current => current === 'ALL' || products.some(product => product.id === current) ? current : 'ALL');
    }).catch(error => { if (!cancelled) setCatalogError(errorMessage(error, 'The local archive catalog could not be loaded.')); });
    return () => { cancelled = true; };
  }, [localYear, api, apiRetry, apiStatus]);
  const selected = useMemo(() => filterRecords(records, filters), [records, filters]);
  const calendarMonth = (filters.start || '2026-10-01').slice(0, 7);
  const [calendarYear, calendarMonthNumber] = calendarMonth.split('-').map(Number);
  const daysInMonth = new Date(calendarYear, calendarMonthNumber, 0).getDate();
  const dates = Array.from({ length: daysInMonth }, (_, i) => `${calendarMonth}-${String(i + 1).padStart(2, '0')}`);
  const monthName = new Date(calendarYear, calendarMonthNumber - 1, 1).toLocaleString('en', { month: 'long', year: 'numeric' });
  const calendarOffset = (new Date(calendarYear, calendarMonthNumber - 1, 1).getDay() + 6) % 7;
  const localCalendarMonth = `${calendarYear}-${String(calendarMonthNumber).padStart(2, '0')}`;
  const expectedCalendarKey = `${localYear}|${localCountry}|${localSource}|${localCalendarMonth}`;
  const useFullMonthCalendar = dataStatus.startsWith('Local FIRMS archive') && localCalendarKey === expectedCalendarKey && filters.region === 'All regions' && filters.sensor === 'All sensors';
  const daily = dates.map(day => ({ day: String(Number(day.slice(-2))), count: useFullMonthCalendar ? (localCalendar[day] || 0) : selected.filter(r => r.acquired === day).length }));
  const timeline = Array.from(selected.reduce((counts, record) => counts.set(record.acquired, (counts.get(record.acquired) || 0) + 1), new Map<string, number>()).entries()).sort(([a], [b]) => a.localeCompare(b)).map(([date, count]) => ({ date, count }));
  const activeDays = daily.filter(d => d.count > 0).length;
  const sensors = Array.from(new Set(selected.map(r => r.sensor))).sort().map(sensor => ({ sensor, count: selected.filter(r => r.sensor === sensor).length }));
  const max = Math.max(...daily.map(d => d.count), 1);
  function downloadCsv() {
    const blob = new Blob([csvFor(selected)], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'firewatch-selected-records.csv'; a.click(); URL.revokeObjectURL(url);
  }
  async function ingest(file?: File) {
    if (!file) return;
    if (!apiAvailable) { setUploadStatus('The FIREWATCH API is offline. Start the app with npm run dev and retry.'); return; }
    setUploadStatus(`Validating ${file.name}…`);
    const body = new FormData(); body.append('file', file);
    try {
      const data = await apiPost<{ count: number; records: Array<Record<string, unknown>> }>(`${api}/api/ingest/firms`, body, { timeoutMs: 45_000 });
      const uploaded: FireRecord[] = data.records.map((row: Record<string, unknown>, i: number) => ({ id: `upload-${i + 1}`, latitude: Number(row.latitude), longitude: Number(row.longitude), brightness: row.brightness == null ? null : Number(row.brightness), confidence: String(row.confidence || 'unknown'), acquired: String(row.acquired).slice(0, 10), sensor: String(row.sensor), daynight: String(row.daynight || 'unknown'), source: `Uploaded: ${file.name}`, metadata: (row.original_fields as Record<string, unknown> | undefined) || undefined }));
      setRecords(uploaded);
      const sortedDates = uploaded.map(r => r.acquired).sort();
      setDataStatus(`User CSV · ${file.name}`); setDataNote(`User-provided FIRMS CSV validated locally. Provenance has not been independently verified; original fields are retained and no harmonization is applied.`); setFilters({ ...initial, start: sortedDates[0], end: sortedDates[sortedDates.length - 1] }); setUploadStatus(`${data.count} validated records loaded from ${file.name}. Sensor labels and source columns are retained; harmonization is not applied.`);
    } catch (error) { setUploadStatus(errorMessage(error, 'CSV validation failed. Check the file and retry.')); }
  }
  async function loadLatestFirms() {
    if (!firmsAvailable) { setUploadStatus(apiAvailable ? 'NASA FIRMS is disabled because the server-side MAP_KEY is not configured.' : 'The FIREWATCH API is offline. Start the app with npm run dev and retry.'); return; }
    setLiveLoading(true); setUploadStatus(`Requesting ${liveSource} from NASA FIRMS…`);
    const area = filters.region === 'All regions' ? 'world' : filters.region;
    const query = new URLSearchParams({ source: liveSource, area, days: String(liveDays) });
    try {
      const data = await apiGet<{ count: number; records: Array<Record<string, unknown>>; dataset: string }>(`${api}/api/firms/latest?${query}`, { timeoutMs: 45_000 });
      if (!data.count) { setUploadStatus(`FIRMS returned no records for ${liveSource} in ${area} over the last ${liveDays} day(s). Try a larger area or date window.`); return; }
      const live: FireRecord[] = data.records.map((row: Record<string, unknown>, i: number) => ({ id: `firms-${i + 1}`, latitude: Number(row.latitude), longitude: Number(row.longitude), brightness: row.brightness == null ? null : Number(row.brightness), confidence: String(row.confidence || 'unknown'), acquired: String(row.acquired).slice(0, 10), sensor: String(row.instrument || row.sensor || 'unknown'), daynight: String(row.daynight || 'unknown'), source: `NASA FIRMS API · ${data.dataset}`, metadata: (row.original_fields as Record<string, unknown> | undefined) || undefined, regionScope: area === 'world' ? undefined : area }));
      const sortedDates = live.map(r => r.acquired).sort(); setRecords(live); setDataStatus(`NASA FIRMS · ${data.dataset}`); setDataNote(`Live near-real-time records queried ${new Date().toLocaleString()} for ${area}, last ${liveDays} day(s). The source feed may be updated or reprocessed; original sensor records are retained and no harmonization is applied.`); setFilters({ ...initial, region: filters.region, sensor: 'All sensors', start: sortedDates[0], end: sortedDates[sortedDates.length - 1] }); setUploadStatus(`${data.count.toLocaleString()} records loaded from NASA FIRMS ${data.dataset}. Original CSV fields are available in export.`);
    } catch (error) { setUploadStatus(errorMessage(error, 'The NASA FIRMS request failed. Check the source and retry.')); }
    finally { setLiveLoading(false); }
  }
  async function loadArchive() {
    if (!firmsAvailable) { setUploadStatus(apiAvailable ? 'NASA FIRMS is disabled because the server-side MAP_KEY is not configured.' : 'The FIREWATCH API is offline. Start the app with npm run dev and retry.'); return; }
    if (!archiveDate) { setUploadStatus('Choose an archive start date before querying NASA FIRMS.'); return; }
    setArchiveLoading(true); setUploadStatus(`Requesting ${archiveSource} archive from ${archiveDate}…`);
    const area = filters.region === 'All regions' ? 'world' : filters.region;
    const query = new URLSearchParams({ source: archiveSource, area, start_date: archiveDate, days: String(archiveDays) });
    try {
      const data = await apiGet<{ count: number; records: Array<Record<string, unknown>>; dataset: string }>(`${api}/api/firms/archive?${query}`, { timeoutMs: 45_000 });
      if (!data.count) { setUploadStatus(`FIRMS returned no archive records for ${archiveSource} in ${area} starting ${archiveDate}. Try another date or area.`); return; }
      const historical: FireRecord[] = data.records.map((row: Record<string, unknown>, i: number) => ({ id: `firms-archive-${i + 1}`, latitude: Number(row.latitude), longitude: Number(row.longitude), brightness: row.brightness == null ? null : Number(row.brightness), confidence: String(row.confidence || 'unknown'), acquired: String(row.acquired).slice(0, 10), sensor: String(row.instrument || row.sensor || 'unknown'), daynight: String(row.daynight || 'unknown'), source: `NASA FIRMS archive · ${data.dataset}`, metadata: (row.original_fields as Record<string, unknown> | undefined) || undefined, regionScope: area === 'world' ? undefined : area }));
      const sortedDates = historical.map(r => r.acquired).sort(); setRecords(historical); setDataStatus(`NASA FIRMS archive · ${data.dataset}`); setDataNote(`NASA FIRMS Standard Processing records queried ${new Date().toLocaleString()} for ${area}, starting ${archiveDate} (${archiveDays} day(s)). This is one sensor-specific archive feed; no cross-sensor harmonization is applied.`); setFilters({ ...initial, region: filters.region, sensor: 'All sensors', start: sortedDates[0], end: sortedDates[sortedDates.length - 1] }); setUploadStatus(`${data.count.toLocaleString()} archive records loaded from ${data.dataset}. Original CSV fields are available in export.`);
    } catch (error) { setUploadStatus(errorMessage(error, 'The NASA FIRMS archive request failed. Check the source and date.')); }
    finally { setArchiveLoading(false); }
  }
  async function loadLocalCalendar(year: number, country: string, source: string, month: number) {
    if (!apiAvailable) { setLocalCalendarLoading(false); setLocalCalendarMessage('Local archive API offline. Start the app with npm run dev, then retry.'); return; }
    setLocalCalendarLoading(true); setLocalCalendarMessage(`Counting full-month source rows for ${country}…`);
    const query = new URLSearchParams({ country, year: String(year), month: String(month) });
    if (source !== 'ALL') query.set('products', source);
    try {
      const data = await apiGet<{ days: Array<{ date: string; count: number }>; products?: string[] }>(`${api}/api/local-archive/calendar?${query}`, { timeoutMs: 60_000 });
      const counts = (data.days as Array<{ date: string; count: number }>).reduce<Record<string, number>>((result, item) => { result[item.date] = Number(item.count); return result; }, {});
      setLocalCalendar(counts); setLocalCalendarProducts(data.products || []); setLocalCalendarKey(`${year}|${country}|${source}|${year}-${String(month).padStart(2, '0')}`); setLocalCalendarMessage('');
    } catch (error) { setLocalCalendarKey(''); setLocalCalendarMessage(`Full-month calendar unavailable: ${errorMessage(error, 'check the selected source and retry.')}`); }
    finally { setLocalCalendarLoading(false); }
  }
  async function loadLocalArchive() {
    if (!apiAvailable) { setUploadStatus('The FIREWATCH API is offline. Start the app with npm run dev and retry.'); return; }
    if (!localCountry || !localStart || !localEnd) { setUploadStatus('Choose a country and date window for the local FIRMS archive.'); return; }
    setLocalLoading(true); setUploadStatus(`Reading local ${localYear} FIRMS records for ${localCountry}…`);
    setLocalCalendarKey(''); setLocalCalendarMessage('');
    const query = new URLSearchParams({ country: localCountry, year: String(localYear), start_date: localStart, end_date: localEnd });
    if (localSource !== 'ALL') query.set('products', localSource);
    try {
      const data = await apiGet<{ count: number; records: Array<Record<string, unknown>> }>(`${api}/api/local-archive/records?${query}`, { timeoutMs: 60_000 });
      if (!data.count) {
        setRecords([]); setDataStatus(`Local FIRMS archive · ${localCountry} · ${localYear}`); setDataNote(`The selected map window has no source rows. The calendar loads full-month source-row counts separately. No harmonization is applied.`); setFilters({ ...initial, region: 'All regions', sensor: 'All sensors', start: localStart, end: localEnd }); setUploadStatus(`No records for the selected map window (${localStart} to ${localEnd}); checking full-month activity for ${localStart.slice(0, 7)}.`); void loadLocalCalendar(localYear, localCountry, localSource, Number(localStart.slice(5, 7))); return;
      }
      const rows: FireRecord[] = data.records.map((row: Record<string, unknown>, i: number) => ({ id: `local-${i + 1}`, latitude: Number(row.latitude), longitude: Number(row.longitude), brightness: row.brightness == null ? null : Number(row.brightness), confidence: String(row.confidence || 'unknown'), acquired: String(row.acquired).slice(0, 10), sensor: String(row.instrument || row.sensor || 'unknown'), daynight: String(row.daynight || 'unknown'), source: `NASA FIRMS local archive · ${row.firms_dataset}`, metadata: { ...((row.original_fields as Record<string, unknown> | undefined) || {}), provenance: row.provenance, firms_dataset: row.firms_dataset } }));
      const counts = rows.reduce<Record<string, number>>((result, row) => { const product = String(row.metadata?.firms_dataset || 'Unknown source'); result[product] = (result[product] || 0) + 1; return result; }, {});
      setRecords(rows); setDataStatus(`Local FIRMS archive · ${localCountry} · ${localYear}`); setDataNote(`Map points show the selected date window. The calendar counts full-month source rows. Products and sensor platforms remain separate; no harmonization or independent provenance verification is applied.`); setFilters({ ...initial, region: 'All regions', sensor: 'All sensors', start: localStart, end: localEnd }); setUploadStatus(`${data.count.toLocaleString()} source rows loaded · ${Object.entries(counts).map(([product, count]) => `${product}: ${count.toLocaleString()}`).join(' · ')}. Original fields are retained; harmonization is not applied.`); void loadLocalCalendar(localYear, localCountry, localSource, Number(localStart.slice(5, 7)));
    } catch (error) { setUploadStatus(errorMessage(error, 'The local archive query failed. Check the selected country and date range.')); }
    finally { setLocalLoading(false); }
  }
  function restoreDemo() {
    setRecords(demoRecords); setFilters(initial); setDataStatus('Simulated demo data'); setDataNote('Illustrative records for exploring the interface. These are not NASA satellite observations.'); setUploadStatus('');
  }
  function retryApi() { setApiStatus('starting'); setApiRetry(value => value + 1); }
  function moveCalendarMonth(delta: number) {
    const target = new Date(calendarYear, calendarMonthNumber - 1 + delta, 1);
    const year = target.getFullYear(); const month = target.getMonth() + 1;
    const first = `${year}-${String(month).padStart(2, '0')}-01`;
    const last = `${year}-${String(month).padStart(2, '0')}-${new Date(year, month, 0).getDate()}`;
    setFilters({ ...filters, start: first, end: last });
    if (dataStatus.startsWith('Local FIRMS archive')) {
      setLocalYear(year); setLocalStart(first); setLocalEnd(last);
      void loadLocalCalendar(year, localCountry, localSource, month);
    }
  }
  return <div className="app-shell">
    <header className="topbar"><a className="brand" href="#top"><span className="brand-mark"><Flame size={21} fill="currentColor" /></span><span>FIREWATCH<small>WILDFIRE ACTIVITY</small></span></a><nav className="topnav"><a className="active" href="#overview">Overview</a><a href="#global-map">Global map</a><a href="#activity-calendar">Calendar</a><a href="#history">History</a><a href="#sensor-comparison">Compare</a><a href="#data-explorer">Data</a><a href="#methodology">Methods</a></nav><div className="top-actions"><span className="live-label"><i /> DATA STATUS</span><span className="demo-chip">{dataStatus.toUpperCase()}</span><button className="icon-btn mobile-menu" aria-label="Toggle filters" onClick={() => setMobileFilters(!mobileFilters)}><Menu size={18}/></button></div></header>
    <main id="overview"><section className="intro"><div><div className="eyebrow"><span className="eyebrow-line"/> GLOBAL FIRE MONITOR <span className="eyebrow-date">· DATA EXPLORATION</span></div><h1>See the signal.<br/><em>Understand the fire.</em></h1><p className="intro-copy">Explore fire activity across the globe by location and time. A clear view of the patterns, grounded in the data.</p></div><button className="export-button" onClick={downloadCsv}><ArrowDownToLine size={16}/> Export selected data <span className="file-type">CSV</span></button></section>
      <div className="notice"><span className="notice-dot"/><strong>{dataStatus}</strong><span>— {dataNote}</span><button title="About data provenance"><CircleHelp size={15}/></button></div>
      <div className={`api-banner api-${apiStatus}`} role="status" aria-live="polite"><span className="api-indicator"/><strong>FIREWATCH API {apiStatus.toUpperCase()}</strong><span>{apiStatus==='online' ? apiHealth?.firms_api_configured ? 'Local archive, validation and FIRMS controls are available.' : 'Local archive and validation are available. NASA live/archive needs a server-side MAP_KEY.' : apiStatus==='starting' ? 'Checking the local service…' : 'API-backed controls are paused. Start both services with npm run dev from the project root.'}</span>{apiStatus==='offline'&&<button type="button" onClick={retryApi}>Retry connection</button>}</div>
      <div className="workspace"><aside className={`sidebar ${mobileFilters ? 'sidebar-open' : ''}`}><div className="side-head"><div><SlidersHorizontal size={15}/><span>EXPLORE</span></div><button onClick={()=>setFilters(initial)} className="clear-button">Reset</button><button className="close-filter" aria-label="Close filters" onClick={()=>setMobileFilters(false)}><X size={17}/></button></div>
        <label className="field-label" htmlFor="region">Area of interest</label><div className="select-wrap"><MapPin size={15}/><select id="region" value={filters.region} onChange={e=>setFilters({...filters, region:e.target.value})}>{regions.map(x=><option key={x}>{x}</option>)}</select><ChevronDown size={14}/></div>
        <label className="field-label" htmlFor="range">Time range</label><div className="date-range"><CalendarDays size={15}/><input aria-label="Start date" type="date" value={filters.start} onChange={e=>setFilters(current=>withDateBound(current,'start',e.target.value))}/><span>—</span><input aria-label="End date" type="date" value={filters.end} onChange={e=>setFilters(current=>withDateBound(current,'end',e.target.value))}/></div><p className="date-help">Filters the data already loaded; dates do not fetch NASA records. {dataStatus==='Simulated demo data'?'Demo records are dated October 2026.':''}</p>
        <label className="field-label" htmlFor="sensor">Sensor</label><div className="select-wrap"><Satellite size={15}/><select id="sensor" value={filters.sensor} onChange={e=>setFilters({...filters,sensor:e.target.value})}><option>All sensors</option><option>MODIS</option><option>VIIRS</option></select><ChevronDown size={14}/></div>
        <div className="sensor-legend"><span className="sensor-key"><i className="dot viirs"/> {sensors[0]?.sensor || 'No sensors'}</span>{sensors[1]&&<span className="sensor-key"><i className="dot modis"/> {sensors[1].sensor}</span>}</div>
        <div className="side-divider"/><div className="ingest"><div className="ingest-title"><Satellite size={15}/><span>NASA FIRMS LIVE</span></div><p>Fetch recent detections. Requires a free server-side FIRMS MAP_KEY.</p><div className="select-wrap compact-select"><select aria-label="FIRMS dataset" title={!apiAvailable?'API offline. Start with npm run dev.':!firmsAvailable?'Server-side FIRMS MAP_KEY is not configured.':''} disabled={!firmsAvailable} value={liveSource} onChange={e=>setLiveSource(e.target.value)}>{liveSources.map(source=><option key={source}>{source}</option>)}</select><ChevronDown size={14}/></div><div className="select-wrap compact-select"><select aria-label="Days to request" disabled={!firmsAvailable} value={liveDays} onChange={e=>setLiveDays(Number(e.target.value))}><option value={1}>Latest 1 day</option><option value={3}>Latest 3 days</option><option value={5}>Latest 5 days</option></select><ChevronDown size={14}/></div><button className="upload-button live-button" title={!apiAvailable?'API offline. Start with npm run dev.':!firmsAvailable?'Server-side FIRMS MAP_KEY is not configured.':''} disabled={liveLoading||!firmsAvailable} onClick={loadLatestFirms}>{liveLoading?'Loading FIRMS…':'Load latest records'}</button>{dataStatus!=='Simulated demo data'&&<button className="upload-button demo-return" onClick={restoreDemo}>Switch back to simulated demo</button>}<p className="small-muted">Current operational feeds: NOAA-20, NOAA-21 and MODIS NRT. Suomi NPP is historical only.</p></div>
        <div className="side-divider"/><div className="ingest"><div className="ingest-title"><CalendarDays size={15}/><span>NASA FIRMS ARCHIVE</span></div><p>Query a short historical window from Standard Processing (SP) records. A MAP_KEY is required.</p><div className="select-wrap compact-select"><select aria-label="FIRMS archive dataset" title={!apiAvailable?'API offline. Start with npm run dev.':!firmsAvailable?'Server-side FIRMS MAP_KEY is not configured.':''} disabled={!firmsAvailable} value={archiveSource} onChange={e=>setArchiveSource(e.target.value)}>{archiveSources.map(source=><option key={source}>{source}</option>)}</select><ChevronDown size={14}/></div><label className="field-label archive-label" htmlFor="archive-date">Start date</label><input id="archive-date" className="archive-date" type="date" disabled={!firmsAvailable} value={archiveDate} onChange={e=>setArchiveDate(e.target.value)}/><div className="select-wrap compact-select"><select aria-label="Archive days" disabled={!firmsAvailable} value={archiveDays} onChange={e=>setArchiveDays(Number(e.target.value))}><option value={1}>1 day</option><option value={3}>3 days</option><option value={5}>5 days</option></select><ChevronDown size={14}/></div><button className="upload-button live-button archive-button" title={!apiAvailable?'API offline. Start with npm run dev.':!firmsAvailable?'Server-side FIRMS MAP_KEY is not configured.':''} disabled={!firmsAvailable||archiveLoading||!archiveDate} onClick={loadArchive}>{archiveLoading?'Loading archive…':'Load archive window'}</button><p className="small-muted">Suomi NPP standard records are available for historical analysis; current NRT feeds use NOAA-20/21.</p></div>
        <div className="side-divider"/><div className="ingest"><div className="ingest-title"><Layers2 size={15}/><span>LOCAL GLOBAL ARCHIVE</span></div><p>Browse extracted global Standard Processing country files. Choose a year, country, source and up to 31 days. No MAP_KEY needed.</p><label className="field-label archive-label" htmlFor="local-year">Archive year</label><div className="select-wrap compact-select"><select id="local-year" aria-label="Local archive year" title={!apiAvailable?'API offline. Start with npm run dev.':''} disabled={!apiAvailable} value={localYear} onChange={e=>{const year=Number(e.target.value);setLocalYear(year);setLocalStart(`${year}-01-01`);setLocalEnd(`${year}-01-05`);setLocalSource('ALL')}}>{localYears.map(year=><option key={year} value={year}>{year}</option>)}</select><ChevronDown size={14}/></div><label className="field-label archive-label" htmlFor="local-source">Source product</label><div className="select-wrap compact-select"><select id="local-source" aria-label="Local archive source product" title={!apiAvailable?'API offline. Start with npm run dev.':''} value={localSource} onChange={e=>setLocalSource(e.target.value)} disabled={!apiAvailable||!localProducts.length}><option value="ALL">All available products</option>{localProducts.map(product=><option key={product.id} value={product.id}>{product.label}</option>)}</select><ChevronDown size={14}/></div><label className="field-label archive-label" htmlFor="local-country">Country</label><div className="select-wrap compact-select"><select id="local-country" aria-label="Local archive country" title={!apiAvailable?'API offline. Start with npm run dev.':''} value={localCountry} onChange={e=>setLocalCountry(e.target.value)} disabled={!apiAvailable||!localCountries.length}>{localCountries.map(c=><option key={c} value={c}>{c.replace(/_/g,' ')}</option>)}</select><ChevronDown size={14}/></div><label className="field-label archive-label" htmlFor="local-start">Date window</label><div className="date-range local-dates"><input id="local-start" aria-label="Local archive start date" title={!apiAvailable?'API offline. Start with npm run dev.':''} type="date" disabled={!apiAvailable} min={`${localYear}-01-01`} max={`${localYear}-12-31`} value={localStart} onChange={e=>setLocalStart(e.target.value)}/><span>—</span><input aria-label="Local archive end date" title={!apiAvailable?'API offline. Start with npm run dev.':''} type="date" disabled={!apiAvailable} min={`${localYear}-01-01`} max={`${localYear}-12-31`} value={localEnd} onChange={e=>setLocalEnd(e.target.value)}/></div><button className="upload-button live-button archive-button" title={!apiAvailable?'API offline. Start with npm run dev.':''} disabled={!apiAvailable||localLoading||!localCountries.length||!localProducts.length} onClick={loadLocalArchive}>{localLoading?'Reading local files…':'Load local records'}</button><p className="small-muted">{catalogError || (localProducts.length ? `${localProducts.length} source product(s) · ${localCountries.length} countries available for ${localYear}` : apiAvailable ? `No extracted source CSVs found for ${localYear}. Choose a year with available archives.` : 'Connect to the local API to inspect extracted files.')}</p></div>
        <div className="side-divider"/><div className="ingest"><div className="ingest-title"><Upload size={15}/><span>OR IMPORT A CSV</span></div><p>Validate FIRMS CSV files. Original fields stay available in export.</p><label className={`upload-button ${!apiAvailable?'disabled':''}`} title={!apiAvailable?'API offline. Start with npm run dev.':''}>Choose a CSV<input type="file" accept=".csv,text/csv" disabled={!apiAvailable} onChange={e=>ingest(e.target.files?.[0])}/></label>{uploadStatus&&<div className={`upload-status ${uploadStatus.startsWith('The')||uploadStatus.startsWith('Could')||uploadStatus.startsWith('FIRMS_MAP_KEY')||uploadStatus.startsWith('FIRMS rejected')?'error':''}`} role="status">{uploadStatus}</div>}</div>
        <div className="side-foot"><span className="foot-icon"><Layers2 size={14}/></span><span>Sources stay distinct.<br/><b>Harmonization not applied.</b></span></div>
      </aside>
      {mobileFilters&&<button className="scrim" onClick={()=>setMobileFilters(false)} aria-label="Close filters"/>}
      <div className="dashboard"><div className="map-panel panel" id="global-map"><div className="panel-top"><div><span className="section-kicker">{dataStatus === 'Simulated demo data' ? 'DEMO MAP' : 'DATA MAP'} <i className="mini-dot"/></span><h2>Global fire activity</h2><p>Selected records · {filters.region}</p></div><div className="map-meta"><span className="map-count"><Flame size={15}/><b>{selected.length}</b><small>records</small></span><span className="map-window">{filters.start || 'ANY DATE'} — {filters.end || 'ANY DATE'}</span></div></div><Suspense fallback={<div className="map-canvas-wrap map-loading">Loading interactive map…</div>}><MapView records={selected} onBboxSelect={setComparisonBbox}/></Suspense><div className="map-bottom">{sensors.map(sensor=><span key={sensor.sensor}><i className={`dot ${sensor.sensor==='MODIS'?'modis':sensor.sensor==='VIIRS'?'viirs':''}`}/> {sensor.sensor} <b>{sensor.count}</b></span>)}<span className="map-note">Each point represents one selected record</span></div></div>
        <section className="calendar-panel panel" id="activity-calendar"><div className="calendar-head"><div><span className="section-kicker">ACTIVITY CALENDAR</span><h2>When activity was recorded</h2></div><div className="month-switch"><button aria-label="Previous month" onClick={()=>moveCalendarMonth(-1)}>‹</button><span>{monthName}</span><button aria-label="Next month" onClick={()=>moveCalendarMonth(1)}>›</button></div></div><div className="calendar-grid">{['M','T','W','T','F','S','S'].map((d,i)=><span className="weekday" key={i}>{d}</span>)}{[...Array(calendarOffset)].map((_,i)=><span className="calendar-blank" key={`b${i}`}/>)}{daily.map(d=><button className={`calendar-day ${d.count?'has-fire':''} ${d.count===max?'peak':''}`} key={d.day} title={`${d.count.toLocaleString()} ${useFullMonthCalendar?'source rows in full month':'selected records'}`} onClick={()=>{const day=`${calendarMonth}-${d.day.padStart(2,'0')}`;setFilters({...filters,start:day,end:day})}}><span>{d.day}</span>{d.count>0&&<i style={{opacity:.38+d.count/max*.62}}/>}</button>)}</div><div className="calendar-foot"><span>{useFullMonthCalendar?`Full-month source rows · ${localCalendarProducts.join(', ')}`:localCalendarLoading?localCalendarMessage:localCalendarMessage||`${activeDays} active days shown in ${monthName}`}</span><div className="scale"><span>Less</span><i/><i/><i/><i className="hot"/><span>More</span></div></div></section>
        <ProcessedComparison api={api} apiStatus={apiStatus} bbox={comparisonBbox} onBboxChange={setComparisonBbox}/>
        <section className="analytics-panel panel" id="history"><div className="analytics-head"><div><span className="section-kicker">ACTIVITY TIMELINE</span><h2>Records by acquisition date</h2><p>One count per date represented in the selection</p></div><div className="metric"><b>{selected.length}</b><span>RECORDS<br/>IN VIEW</span></div></div><div className="chart-wrap">{selected.length===0?<div className="empty-state"><Activity size={20}/><b>No records in this selection</b><span>Adjust the area, sensor or date range to continue.</span></div>:<Suspense fallback={<div className="empty-state">Loading timeline…</div>}><TimelineChart data={timeline}/></Suspense>}</div><div className="chart-caption"><span><i className="chart-line"/> Records per acquisition date</span><span>Counts describe this dataset only</span></div></section>
        <DataExplorer records={selected}/>
        <section className="integrity-panel" id="methodology"><div className="integrity-icon"><Activity size={16}/></div><div id="data"><b>Exploratory view, transparent data.</b><span>Overview and map: {dataStatus}. The processed comparison uses detected cell-days; calibrated estimates and validated anomalies are not available.</span></div><span className="integrity-badge">CALIBRATION INSUFFICIENT</span></section>
      </div></div>
      <footer><span>FIREWATCH <i>·</i> NASA SPACE APPS CHALLENGE 2026</span><span>FIRMS feeds: NOAA-20 / NOAA-21 VIIRS and MODIS NRT</span><a href="#data">Data provenance & methods ↗</a></footer>
    </main>
  </div>
}
