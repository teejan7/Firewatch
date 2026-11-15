import { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';

type GridRow = [number, string, string, string, number, number, number, number];
type Props = { rows: GridRow[]; year: number; sensor: 'All' | 'MODIS' | 'VIIRS' };

export default function StaticMap({ rows, year, sensor }: Props) {
  const node = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    if (!node.current || map.current) return;
    try {
      const instance = new maplibregl.Map({
        container: node.current,
        style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
        center: [0, 18], zoom: 0.3, minZoom: 0, maxZoom: 7,
      });
      map.current = instance;
      instance.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right');
      instance.on('error', () => setFailed(true));
      instance.on('load', () => {
        instance.addSource('activity-cells', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });
        instance.addLayer({ id: 'activity-points', type: 'circle', source: 'activity-cells', paint: {
          'circle-radius': ['interpolate', ['linear'], ['get', 'count'], 1, 2.5, 500, 8, 5000, 14],
          'circle-color': ['match', ['get', 'sensor'], 'MODIS', '#ffad6f', 'VIIRS', '#d8f06a', '#b7a5ff'],
          'circle-opacity': 0.78, 'circle-stroke-color': '#101713', 'circle-stroke-width': 1,
        } });
      });
    } catch { setFailed(true); }
    return () => { map.current?.remove(); map.current = null; };
  }, []);
  useEffect(() => {
    const instance = map.current;
    if (!instance) return;
    const update = () => {
      const source = instance.getSource('activity-cells') as maplibregl.GeoJSONSource | undefined;
      if (!source) return;
      const filtered = rows.filter(row => row[0] === year && (sensor === 'All' || row[1] === sensor));
      source.setData({ type: 'FeatureCollection', features: filtered.map(row => ({
        type: 'Feature', geometry: { type: 'Point', coordinates: [row[5], row[4]] },
        properties: { sensor: row[1], platform: row[2], product: row[3], count: row[6], frp: row[7] },
      })) });
      if (filtered.length) {
        const lons = filtered.map(row => row[5]); const lats = filtered.map(row => row[4]);
        instance.fitBounds([[Math.min(...lons) - 2, Math.min(...lats) - 2], [Math.max(...lons) + 2, Math.max(...lats) + 2]], { padding: 55, maxZoom: 3.5, duration: 0 });
      }
    };
    if (instance.isStyleLoaded()) update(); else instance.once('load', update);
  }, [rows, year, sensor]);
  return <div className="fw-map-wrap">
    <div ref={node} className="fw-map" role="img" aria-label={`Aggregated FIRMS detections for ${year}; one-degree cells, no country boundaries`} />
    {failed && <div className="fw-map-fallback" role="status">Basemap tiles are unavailable. The dashboard data and calendar remain usable.</div>}
    <div className="fw-map-caption"><span>Circle = detected records grouped to 1° cells</span><span>Sensor-specific · not a fire perimeter</span></div>
  </div>;
}
