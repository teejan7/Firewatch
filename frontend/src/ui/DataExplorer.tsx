import { useMemo, useState } from 'react';
import { ArrowDownToLine, ChevronLeft, ChevronRight, Search } from 'lucide-react';
import type { FireRecord } from '../data/demo';
import { csvFor } from '../lib/filters';

const PAGE_SIZE = 25;
type SortKey = 'acquired' | 'sensor' | 'latitude';

export default function DataExplorer({ records }: { records: FireRecord[] }) {
  const [search, setSearch] = useState('');
  const [sortKey, setSortKey] = useState<SortKey>('acquired');
  const [page, setPage] = useState(0);
  const filtered = useMemo(() => records.filter(row => `${row.acquired} ${row.sensor} ${row.source} ${row.latitude} ${row.longitude} ${row.confidence}`.toLowerCase().includes(search.trim().toLowerCase())).sort((a, b) => sortKey === 'latitude' ? a.latitude - b.latitude : sortKey === 'sensor' ? a.sensor.localeCompare(b.sensor) : a.acquired.localeCompare(b.acquired)), [records, search, sortKey]);
  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const visible = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  function exportFiltered() {
    const url = URL.createObjectURL(new Blob([csvFor(filtered)], { type: 'text/csv;charset=utf-8' }));
    const link = document.createElement('a'); link.href = url; link.download = 'firewatch-data-explorer.csv'; link.click(); URL.revokeObjectURL(url);
  }

  return <section className="data-explorer panel" id="data-explorer" aria-labelledby="data-explorer-title">
    <div className="data-explorer-head"><div><span className="section-kicker">DATA EXPLORER</span><h2 id="data-explorer-title">Selected source records</h2><p>Source metadata is retained for traceability. Filters apply to the currently selected dataset.</p></div><button className="comparison-export" onClick={exportFiltered} disabled={!filtered.length}><ArrowDownToLine size={13}/> Export filtered CSV</button></div>
    <div className="explorer-controls"><label className="explorer-search"><Search size={14}/><input aria-label="Search selected records" placeholder="Search date, sensor, source, coordinates…" value={search} onChange={event => { setSearch(event.target.value); setPage(0); }}/></label><label className="explorer-sort">Sort by<select aria-label="Sort records" value={sortKey} onChange={event => setSortKey(event.target.value as SortKey)}><option value="acquired">Acquisition date</option><option value="sensor">Sensor</option><option value="latitude">Latitude</option></select></label></div>
    <div className="table-scroll"><table><thead><tr><th>Date (UTC)</th><th>Sensor / platform</th><th>Latitude</th><th>Longitude</th><th>Confidence</th><th>Source / provenance</th></tr></thead><tbody>{visible.map(row => <tr key={row.id}><td>{row.acquired}</td><td>{row.sensor}{row.metadata?.satellite ? ` · ${String(row.metadata.satellite)}` : ''}</td><td>{row.latitude.toFixed(3)}</td><td>{row.longitude.toFixed(3)}</td><td>{row.confidence}</td><td title={row.source}>{row.source}</td></tr>)}</tbody></table>{!visible.length&&<div className="explorer-empty">{records.length ? 'No records match this search.' : 'No source records loaded. Query a local archive or load a FIRMS source to populate the explorer.'}</div>}</div>
    <div className="explorer-pagination"><span>{filtered.length ? `${(page * PAGE_SIZE + 1).toLocaleString()}–${Math.min((page + 1) * PAGE_SIZE, filtered.length).toLocaleString()} of ${filtered.length.toLocaleString()} matching records` : '0 matching records'}</span><div><button aria-label="Previous record page" disabled={page === 0} onClick={() => setPage(value => Math.max(0, value - 1))}><ChevronLeft size={15}/></button><span>Page {page + 1} of {pageCount}</span><button aria-label="Next record page" disabled={page + 1 >= pageCount} onClick={() => setPage(value => Math.min(pageCount - 1, value + 1))}><ChevronRight size={15}/></button></div></div>
  </section>;
}
