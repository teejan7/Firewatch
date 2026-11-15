export type FireRecord = { id: string; latitude: number; longitude: number; brightness: number | null; confidence: string; acquired: string; sensor: string; daynight: string; source: string; metadata?: Record<string, unknown>; regionScope?: string };
// Fixed illustrative points for interface development. These are not observations.
const places = [
  ['Amazonas', -3.2, -60.1, 'VIIRS'], ['Amazonas', -5.1, -63.7, 'MODIS'], ['Roraima', 2.8, -61.4, 'VIIRS'], ['Mato Grosso', -12.4, -55.8, 'VIIRS'], ['Mato Grosso', -10.8, -57.2, 'MODIS'],
  ['California', 38.1, -120.4, 'VIIRS'], ['California', 39.6, -121.5, 'MODIS'], ['Oregon', 43.8, -120.1, 'VIIRS'], ['Alaska', 64.2, -150.8, 'MODIS'], ['Alaska', 62.7, -148.3, 'VIIRS'],
  ['Queensland', -18.4, 145.2, 'VIIRS'], ['Queensland', -21.1, 148.9, 'MODIS'], ['Western Australia', -25.7, 121.4, 'VIIRS'], ['New South Wales', -32.3, 149.1, 'MODIS'],
  ['Siberia', 61.5, 105.2, 'VIIRS'], ['Siberia', 58.4, 113.8, 'MODIS'], ['Siberia', 55.9, 96.4, 'VIIRS'], ['Central Africa', 2.1, 23.4, 'MODIS'], ['Central Africa', -1.7, 20.8, 'VIIRS'],
  ['Mediterranean', 38.3, 23.8, 'VIIRS'], ['Mediterranean', 37.2, 15.1, 'MODIS'], ['India', 22.6, 82.1, 'VIIRS'], ['India', 24.2, 91.4, 'MODIS'], ['Indonesia', -2.4, 114.6, 'VIIRS'],
  ['Canada', 53.8, -121.7, 'VIIRS'], ['Canada', 56.4, -116.2, 'MODIS'], ['Canada', 49.1, -82.8, 'VIIRS'], ['Mexico', 18.9, -98.2, 'MODIS'], ['Chile', -37.6, -72.4, 'VIIRS'], ['Argentina', -26.2, -63.4, 'MODIS']
] as const;
export const demoRecords: FireRecord[] = places.map((p, i) => ({ id: `demo-${String(i + 1).padStart(3, '0')}`, latitude: p[1] + (((i % 3) - 1) * 0.22), longitude: p[2] + (((i % 4) - 1.5) * 0.24), brightness: 306 + ((i * 17) % 83), confidence: ['low', 'nominal', 'high'][i % 3], acquired: `2026-10-${String(1 + ((i * 7) % 31)).padStart(2, '0')}`, sensor: p[3], daynight: i % 4 === 0 ? 'N' : 'D', source: 'Simulated demo data' }));
