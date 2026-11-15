import { useEffect, useRef, useState } from 'react';
import { MapPin } from 'lucide-react';
import maplibregl from 'maplibre-gl';
import type { FireRecord } from '../data/demo';
export default function MapView({ records, onBboxSelect }: { records: FireRecord[]; onBboxSelect?: (bbox: string) => void }) {
  const node = useRef<HTMLDivElement>(null); const map = useRef<maplibregl.Map | null>(null); const [failed, setFailed] = useState(false);
  const [drawing, setDrawing] = useState(false); const [firstCorner, setFirstCorner] = useState<[number, number] | null>(null); const [selection, setSelection] = useState<[number, number, number, number] | null>(null);
  const drawingRef = useRef(false); const firstCornerRef = useRef<[number, number] | null>(null); const callbackRef = useRef(onBboxSelect);
  useEffect(() => { callbackRef.current = onBboxSelect; }, [onBboxSelect]);
  useEffect(() => {
    if (!node.current || map.current) return;
    try {
      map.current = new maplibregl.Map({ container: node.current, style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json', center: [5, 13], zoom: 0.25, minZoom: 0, maxZoom: 8, attributionControl: false });
      map.current.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right');
      map.current.on('error', () => setFailed(true));
    } catch { setFailed(true); }
    return () => { map.current?.remove(); map.current = null; };
  }, []);
  useEffect(() => {
    const m = map.current; if (!m) return;
    const update = () => {
      const features = records.map(r => ({ type: 'Feature' as const, geometry: { type: 'Point' as const, coordinates: [r.longitude, r.latitude] }, properties: { sensor: r.sensor, confidence: r.confidence, acquired: r.acquired, brightness: r.brightness, source: r.source, platform: r.metadata?.satellite || r.metadata?.platform || '', version: r.metadata?.version || '', frp: r.metadata?.frp || '' } }));
      const data = { type: 'FeatureCollection' as const, features };
      if (m.getSource('fires')) (m.getSource('fires') as maplibregl.GeoJSONSource).setData(data);
      else if (m.isStyleLoaded()) { m.addSource('fires', { type: 'geojson', data }); m.addLayer({ id: 'fire-halo', type: 'circle', source: 'fires', paint: { 'circle-radius': ['interpolate',['linear'],['zoom'],0,5,4,11], 'circle-color': ['match',['get','sensor'],'VIIRS','#d6fa72','MODIS','#f69c67','#a5ada7'], 'circle-opacity': 0.22, 'circle-blur': 0.5 } }); m.addLayer({ id: 'fire-point', type: 'circle', source: 'fires', paint: { 'circle-radius': ['interpolate',['linear'],['zoom'],0,2.6,4,5.5], 'circle-color': ['match',['get','sensor'],'VIIRS','#d6fa72','MODIS','#f69c67','#a5ada7'], 'circle-stroke-color': '#111a15', 'circle-stroke-width': 1, 'circle-opacity': 0.95 } }); m.on('click', 'fire-point', e => { const p = e.features?.[0]?.properties; if (!p || !e.lngLat) return; const card = document.createElement('div'); card.className = 'popup-record'; const line = (value: unknown, strong = false) => { const item = document.createElement(strong ? 'b' : 'span'); item.textContent = String(value ?? ''); card.append(item); }; line(`${p.sensor} · ${p.source}`, true); line(String(p.acquired)); if (p.platform) line(`Platform: ${p.platform}`); if (p.version) line(`Version: ${p.version}`); line(`Confidence: ${p.confidence}`); line(`Brightness: ${p.brightness ?? 'unavailable'}`); if (p.frp) line(`FRP: ${p.frp}`); new maplibregl.Popup({ closeButton: true, offset: 8 }).setLngLat(e.lngLat).setDOMContent(card).addTo(m); }); m.on('mouseenter', 'fire-point', () => { m.getCanvas().style.cursor = 'pointer'; }); m.on('mouseleave', 'fire-point', () => { m.getCanvas().style.cursor = ''; }); }
    };
    if (m.isStyleLoaded()) update(); else m.once('load', update);
  }, [records]);
  useEffect(() => {
    const m = map.current; if (!m) return;
    const click = (event: maplibregl.MapMouseEvent) => {
      if (!drawingRef.current) return;
      const point: [number, number] = [event.lngLat.lng, event.lngLat.lat];
      if (!firstCornerRef.current) { firstCornerRef.current = point; setFirstCorner(point); return; }
      const start = firstCornerRef.current; const box: [number, number, number, number] = [Math.min(start[0], point[0]), Math.min(start[1], point[1]), Math.max(start[0], point[0]), Math.max(start[1], point[1])];
      firstCornerRef.current = null; drawingRef.current = false; setFirstCorner(null); setDrawing(false); setSelection(box); callbackRef.current?.(box.map(value => value.toFixed(5)).join(','));
      const [west, south, east, north] = box;
      const data = { type: 'Feature' as const, properties: {}, geometry: { type: 'Polygon' as const, coordinates: [[[west,south],[east,south],[east,north],[west,north],[west,south]]] } };
      const source = m.getSource('aoi-selection') as maplibregl.GeoJSONSource | undefined;
      if (source) source.setData(data); else { m.addSource('aoi-selection', { type: 'geojson', data }); m.addLayer({ id: 'aoi-fill', type: 'fill', source: 'aoi-selection', paint: { 'fill-color': '#d6fa72', 'fill-opacity': 0.08 } }); m.addLayer({ id: 'aoi-outline', type: 'line', source: 'aoi-selection', paint: { 'line-color': '#d6fa72', 'line-width': 2, 'line-dasharray': [2, 1] } }); }
    };
    m.on('click', click); return () => { m.off('click', click); };
  }, []);
  function beginDrawing() { firstCornerRef.current = null; drawingRef.current = true; setFirstCorner(null); setDrawing(true); }
  function clearSelection() { const m = map.current; if (m?.getLayer('aoi-outline')) m.removeLayer('aoi-outline'); if (m?.getLayer('aoi-fill')) m.removeLayer('aoi-fill'); if (m?.getSource('aoi-selection')) m.removeSource('aoi-selection'); setSelection(null); callbackRef.current?.(''); }
  return <div className="map-canvas-wrap"><div ref={node} className="map-canvas" aria-label="Map of selected active-fire records; source is shown in the dashboard data status"/><div className="map-aoi-tools"><button type="button" onClick={beginDrawing} aria-pressed={drawing}>{drawing ? 'Click map for corner…' : 'Draw AOI box'}</button>{selection&&<button type="button" onClick={clearSelection}>Clear AOI</button>}<span>{firstCorner ? 'Now click the opposite corner.' : drawing ? 'Click two map corners.' : selection ? 'AOI applied to processed comparison.' : 'Optional: draw an area for comparison.'}</span></div>{failed&&<div className="map-unavailable"><MapPin size={18}/><b>Map tiles unavailable</b><span>Check your connection to load the basemap. Selected records and analytics are still available.</span></div>}{records.length===0&&<div className="map-empty"><span>No records match these filters</span></div>}</div>
}
