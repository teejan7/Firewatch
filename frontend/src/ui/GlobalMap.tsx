import { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';

type Activity = { year: number; modis_detections: number; viirs_detections: number; modis_frp_sum_mw: number; viirs_frp_sum_mw: number };
type CountryPoint = { name: string; observed_centroid_lon_lat: [number, number] | null };
type MapActivity = { name: string; activity_by_year: Activity[]; activity_by_month: Array<Activity & { month: number }>; coverage_by_product_year: Array<{ product: string; year: number; expected: number; processed: number }> };
type Props = { countries: CountryPoint[]; activity: MapActivity[]; year: number; month: number; metric: 'detections' | 'frp'; sensor: 'All' | 'MODIS' | 'VIIRS'; selectedCountry: string; onSelect: (name: string) => void };

export default function GlobalMap({ countries, activity, year, month, metric, sensor, selectedCountry, onSelect }: Props) {
  const node = useRef<HTMLDivElement>(null); const map = useRef<maplibregl.Map | null>(null); const selectRef = useRef(onSelect); const yearRef = useRef(year); const monthRef = useRef(month); const metricRef = useRef(metric); const [failed, setFailed] = useState(false);
  useEffect(() => { selectRef.current = onSelect; }, [onSelect]);
  useEffect(() => { yearRef.current = year; }, [year]);
  useEffect(() => { monthRef.current = month; }, [month]);
  useEffect(() => { metricRef.current = metric; }, [metric]);
  useEffect(() => {
    if (!node.current || map.current) return;
    try {
      const instance = new maplibregl.Map({ container: node.current, style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json', center: [0, 15], zoom: 0.25, minZoom: 0, maxZoom: 6 });
      map.current = instance; instance.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right');
      instance.on('error', () => setFailed(true));
      instance.on('load', () => {
        instance.addSource('country-activity', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });
        instance.addLayer({ id: 'country-activity-points', type: 'circle', source: 'country-activity', paint: {
          'circle-radius': ['interpolate', ['linear'], ['get', 'weight'], 0, 3, 10, 6, 15, 10],
          'circle-color': ['match', ['get', 'family'], 'MODIS', '#ffad6f', 'VIIRS', '#d8f06a', '#b8a7ff'],
          'circle-opacity': 0.8,
          'circle-stroke-color': ['case', ['get', 'selected'], '#ffffff', '#17201a'],
          'circle-stroke-width': ['case', ['get', 'selected'], 2, 1],
        } });
        instance.on('click', 'country-activity-points', event => {
          const properties = event.features?.[0]?.properties; if (!properties?.country) return;
          selectRef.current(String(properties.country));
          const popup = document.createElement('div'); popup.className = 'fw-map-popup';
          const title = document.createElement('b'); title.textContent = String(properties.country).replace(/_/g, ' '); popup.append(title);
          const period = monthRef.current ? new Date(Date.UTC(2020, monthRef.current - 1, 1)).toLocaleString('en', { month: 'short' }) : 'full year';
          const label = metricRef.current === 'frp' ? 'MW FRP sum' : 'detections';
          const detail = document.createElement('span'); detail.textContent = `${period} ${yearRef.current} · MODIS ${Number(properties.modis).toLocaleString()} · VIIRS ${Number(properties.viirs).toLocaleString()} ${label}`; popup.append(detail);
          const note = document.createElement('small'); note.textContent = 'Select the bubble to open this country. Centroid marker; no country boundary data.'; popup.append(note);
          new maplibregl.Popup({ offset: 8, closeButton: true }).setLngLat(event.lngLat).setDOMContent(popup).addTo(instance);
        });
        instance.on('mouseenter', 'country-activity-points', () => { instance.getCanvas().style.cursor = 'pointer'; });
        instance.on('mouseleave', 'country-activity-points', () => { instance.getCanvas().style.cursor = ''; });
      });
    } catch { setFailed(true); }
    return () => { map.current?.remove(); map.current = null; };
  }, []);
  useEffect(() => {
    const instance = map.current; if (!instance) return;
    const update = () => {
      const source = instance.getSource('country-activity') as maplibregl.GeoJSONSource | undefined; if (!source) return;
      const activityByCountry = new Map(activity.map(item => [item.name, item]));
      const features = countries.flatMap(country => {
        if (!country.observed_centroid_lon_lat) return [];
        const countryActivity = activityByCountry.get(country.name); if (!countryActivity) return [];
        const activityRow = month ? countryActivity.activity_by_month.find(item => item.year === year && item.month === month) : countryActivity.activity_by_year.find(item => item.year === year); if (!activityRow) return [];
        const modis = metric === 'frp' ? activityRow.modis_frp_sum_mw : activityRow.modis_detections;
        const viirs = metric === 'frp' ? activityRow.viirs_frp_sum_mw : activityRow.viirs_detections;
        const value = sensor === 'MODIS' ? modis : sensor === 'VIIRS' ? viirs : modis + viirs;
        const hasModis = activityRow.modis_detections > 0; const hasViirs = activityRow.viirs_detections > 0;
        const family = sensor === 'All' ? 'BOTH' : sensor;
        const productRows = countryActivity.coverage_by_product_year.filter(row => row.year === year && (sensor === 'All' || row.product.startsWith(sensor)));
        const coverage = productRows.length && productRows.every(row => row.expected > 0 && row.processed === row.expected) ? 'complete' : 'partial';
        return [{ type: 'Feature' as const, geometry: { type: 'Point' as const, coordinates: country.observed_centroid_lon_lat }, properties: {
          country: country.name, modis, viirs, count: value, weight: Math.log1p(Math.max(value, 0)), family: family === 'BOTH' ? (hasModis && hasViirs ? 'BOTH' : hasModis ? 'MODIS' : 'VIIRS') : family,
          selected: country.name === selectedCountry, coverage,
        } }];
      });
      source.setData({ type: 'FeatureCollection', features });
    };
    if (instance.isStyleLoaded()) update(); else instance.once('load', update);
  }, [countries, activity, year, month, metric, sensor, selectedCountry]);
  return <div className="fw-map-wrap"><div ref={node} className="fw-map" role="img" aria-label={`Global country activity bubble map for ${year}; markers are detection centroids, not country boundaries`}/>{failed && <div className="fw-map-fallback" role="status">Basemap tiles are unavailable. Country search and the activity calendar remain usable.</div>}<div className="fw-map-caption"><span>Country activity at weighted detection centroids · click a bubble to select</span><span>Not a boundary choropleth</span></div></div>;
}
