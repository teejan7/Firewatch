import { useMemo } from 'react';
import { Area, CartesianGrid, ComposedChart, Line, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

export type HarmonizedMode = 'raw' | 'harmonized';
export type HarmonizedDaily = {
  date: string; year: number; doy: number; raw_modis_frp: number; raw_viirs_frp: number;
  raw_frp_sum: number; modis_n: number; viirs_n: number; week: string;
  operating_week: boolean; daily_scale_for_viirs: number | null;
  scaled_viirs_frp: number | null; harmonized_frp_daily: number | null;
  raw_unusual_week: boolean; harmonized_unusual_week: boolean; has_source_record: boolean;
};
type ClimatologyDay = {
  doy: number; sample_years: number;
  raw_median: number | null; raw_q25: number | null; raw_q75: number | null;
  harmonized_median: number | null; harmonized_q25: number | null; harmonized_q75: number | null;
  raw_by_year: Record<string, number>; harmonized_by_year: Record<string, number>;
  raw_unusual_by_year: Record<string, boolean>; harmonized_unusual_by_year: Record<string, boolean>;
};
type SeasonPart = { start: string | null; peak: string | null; end: string | null; annual_frp: number };
export type HarmonizedSeries = {
  country: string; confidence: string; fit: string;
  daily: HarmonizedDaily[]; climatology_by_doy: ClimatologyDay[];
  fire_season_by_year: Record<string, { raw: SeasonPart; harmonized: SeasonPart }>;
};

type Props = { data: HarmonizedSeries; year: number; mode: HarmonizedMode };

export default function HarmonizedAnalytics({ data, year, mode }: Props) {
  const byDay = useMemo(() => new Map(data.daily.map(row => [`${row.year}:${row.doy}`, row])), [data]);
  const max = Math.max(1, ...data.daily.map(row => mode === 'harmonized' ? row.harmonized_frp_daily || 0 : row.raw_frp_sum));
  const chartRows = useMemo(() => data.climatology_by_doy.map(row => {
    const median = mode === 'harmonized' ? row.harmonized_median : row.raw_median;
    const q25 = mode === 'harmonized' ? row.harmonized_q25 : row.raw_q25;
    const q75 = mode === 'harmonized' ? row.harmonized_q75 : row.raw_q75;
    const yearValues = mode === 'harmonized' ? row.harmonized_by_year : row.raw_by_year;
    const unusualValues = mode === 'harmonized' ? row.harmonized_unusual_by_year : row.raw_unusual_by_year;
    const selected = yearValues[String(year)];
    return { doy: row.doy, median, q25, band: q25 === null || q75 === null ? null : q75 - q25,
      selected: selected ?? null, unusual: unusualValues[String(year)] ? selected ?? null : null };
  }), [data, mode, year]);
  const season = data.fire_season_by_year[String(year)]?.[mode];
  const modeLabel = mode === 'harmonized' ? 'harmonized FRP' : 'raw MODIS + VIIRS FRP';

  return <div className="fw-harmonized-analytics">
    <div className="fw-preliminary">PRELIMINARY (6-year baseline) · Vegetation FRP</div>
    <section className="fw-panel fw-multiyear">
      <div className="fw-section-head"><div><span className="fw-kicker">MULTI-YEAR CALENDAR</span><h2>Daily fire activity · {modeLabel}</h2><p>Rows are 2020–2025; blanks are outside reported operating weeks or have no packaged record.</p></div></div>
      <div className="fw-heatmap-scroll"><div className="fw-heatmap-months"><span>JAN</span><span>MAR</span><span>MAY</span><span>JUL</span><span>SEP</span><span>NOV</span></div>
        {data.fire_season_by_year && [2020, 2021, 2022, 2023, 2024, 2025].map(itemYear => <div className="fw-heatmap-row" key={itemYear}>
          <b>{itemYear}</b><div role="group" aria-label={`${itemYear} multi-year calendar`}>{Array.from({ length: 366 }, (_, index) => {
            const doy = index + 1; const point = byDay.get(`${itemYear}:${doy}`);
            const value = mode === 'harmonized' ? point?.harmonized_frp_daily : point?.raw_frp_sum;
            const calibrated = mode === 'raw' || point?.harmonized_frp_daily !== null && point?.harmonized_frp_daily !== undefined;
            const intensity = value && calibrated ? Math.min(4, Math.ceil(Math.log1p(value) / Math.log1p(max) * 4)) : 0;
            const cls = `${calibrated ? `intensity-${intensity}` : 'is-uncalibrated'}${point?.[mode === 'harmonized' ? 'harmonized_unusual_week' : 'raw_unusual_week'] ? ' is-unusual' : ''}`;
            return <i key={doy} className={`fw-heat-cell ${cls}`} title={point ? `${point.date}: ${calibrated ? `${Number(value || 0).toFixed(1)} MW${point[mode === 'harmonized' ? 'harmonized_unusual_week' : 'raw_unusual_week'] ? ' · unusual week' : ''}` : 'Not calibrated for this week'}` : `${itemYear} day ${doy}: no packaged record`}/>;
          })}</div></div>)}
      </div>
      <p className="fw-small-note">Dots mark weeks above the selected mode’s six-year 90th percentile. No-record days do not establish observation opportunity.</p>
    </section>

    <div className="fw-two-col fw-analytics-grid">
      <section className="fw-panel fw-chart-panel">
        <div className="fw-section-head"><div><span className="fw-kicker">TYPICAL VS THIS YEAR</span><h2>Day-of-year FRP · {year}</h2><p>Median and 25–75% range across years; selected year overlaid.</p></div></div>
        <div className="fw-analytics-chart"><ResponsiveContainer width="100%" height="100%"><ComposedChart data={chartRows} margin={{ top: 8, right: 10, bottom: 0, left: -16 }}>
          <CartesianGrid stroke="#29372d" strokeDasharray="3 3"/><XAxis dataKey="doy" tick={{ fill: '#849186', fontSize: 9 }} ticks={[1, 60, 121, 182, 244, 305, 366]} tickFormatter={value => String(value)}/><YAxis tick={{ fill: '#849186', fontSize: 9 }}/><Tooltip formatter={(value) => [`${Number(value).toFixed(1)} MW`, 'FRP']} labelFormatter={label => `Day ${label}`}/>
          <Area dataKey="q25" stackId="band" stroke="none" fill="transparent" isAnimationActive={false}/><Area dataKey="band" stackId="band" stroke="none" fill="#d7f46f" fillOpacity={0.18} isAnimationActive={false}/>
          <Line dataKey="median" name="Six-year median" stroke="#d7f46f" strokeWidth={1.5} dot={false} connectNulls={false} isAnimationActive={false}/>
          <Line dataKey="selected" name={`${year}`} stroke="#ffad6f" strokeWidth={1.5} dot={false} connectNulls={false} isAnimationActive={false}/>
          <Line dataKey="unusual" name="Unusual week (>P90)" stroke="none" dot={{ r: 2.5, fill: '#ff775d' }} connectNulls={false} isAnimationActive={false}/>
        </ComposedChart></ResponsiveContainer></div>
        <p className="fw-small-note">PRELIMINARY (6-year baseline). Missing observations are not filled as zero.</p>
      </section>

      <section className="fw-panel fw-season-panel">
        <div className="fw-section-head"><div><span className="fw-kicker">FIRE SEASON · {year}</span><h2>Cumulative 5%–95% of annual FRP</h2><p>{mode === 'harmonized' ? 'Using weekly harmonized FRP.' : 'Using reported raw sensor FRP sum.'}</p></div></div>
        {season?.start && season.peak && season.end ? <div className="fw-season-line" aria-label={`Fire season start ${season.start}, peak ${season.peak}, end ${season.end}`}>
          <div><i/><b>START</b><span>{season.start}</span></div><hr/><div><i/><b>PEAK</b><span>{season.peak}</span></div><hr/><div><i/><b>END</b><span>{season.end}</span></div>
        </div> : <div className="fw-analytics-empty">No operating-week FRP is available for this year.</div>}
        <p className="fw-small-note">PRELIMINARY (6-year baseline). A reporting-season summary, not a forecast or validated fire-season boundary.</p>
      </section>
    </div>
  </div>;
}
