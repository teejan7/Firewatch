# FIREWATCH project structure and technical inventory

**Snapshot:** 2026-11-15T13:29:14+05:30 local time. Read-only audit; no NASA APIs called. `.env` contents were not read. A Python processor was active while scanning, so generated data can change and rows absent during the scan are ASSUMED incomplete.

## 1. TREE

Root: `nasa`; paths through depth 6. Excluded: `node_modules`, `.venv`, `__pycache__`, `dist`, `build`, `.git`. Raw extracted contents are summarized separately.

```text
nasa
├── .pytest_cache/
│   ├── v/
│   │   └── cache/
│   │       ├── lastfailed
│   │       └── nodeids
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   └── README.md
├── .ruff_cache/
│   ├── 0.17.5/
│   ├── .gitignore
│   └── CACHEDIR.TAG
├── .tmp/
│   ├── pytest/
│   └── duckdb_temp_2024_0_owner
├── backend/
│   ├── .pytest_cache/
│   │   ├── v/
│   │   │   └── cache/
│   │   │       ├── lastfailed
│   │   │       └── nodeids
│   │   ├── .gitignore
│   │   ├── CACHEDIR.TAG
│   │   └── README.md
│   ├── .ruff_cache/
│   │   ├── 0.17.5/
│   │   │   ├── 15555960183036323003
│   │   │   └── 16039197481397102676
│   │   ├── .gitignore
│   │   └── CACHEDIR.TAG
│   ├── app/
│   │   ├── __init__.py
│   │   ├── analytics_api.py
│   │   ├── firms.py
│   │   ├── harmonize.py
│   │   ├── local_archive.py
│   │   ├── main.py
│   │   └── validation.py
│   ├── scripts/
│   │   ├── __init__.py
│   │   └── build_processed.py
│   ├── tests/
│   │   ├── test_analytics_api.py
│   │   ├── test_firms.py
│   │   ├── test_harmonize.py
│   │   ├── test_processing.py
│   │   └── test_validation.py
│   ├── check.ps1
│   ├── pyproject.toml
│   └── requirements.txt
├── backups/
│   └── firewatch-pre-2.0-20261114-202127/
│       ├── backend/
│       │   ├── app/
│       │   │   ├── __init__.py
│       │   │   ├── firms.py
│       │   │   ├── local_archive.py
│       │   │   ├── main.py
│       │   │   └── validation.py
│       │   └── tests/
│       │       ├── test_firms.py
│       │       └── test_validation.py
│       ├── data/
│       │   └── raw/
│       │       └── README.txt
│       ├── frontend/
│       │   ├── src/
│       │   │   ├── data/
│       │   │   │   └── demo.ts
│       │   │   ├── lib/
│       │   │   │   ├── filters.test.ts
│       │   │   │   └── filters.ts
│       │   │   ├── ui/
│       │   │   │   ├── App.tsx
│       │   │   │   ├── MapView.tsx
│       │   │   │   └── TimelineChart.tsx
│       │   │   ├── main.tsx
│       │   │   ├── styles.css
│       │   │   ├── testSetup.ts
│       │   │   └── vite-env.d.ts
│       │   ├── index.html
│       │   ├── package.json
│       │   ├── tsconfig.json
│       │   └── vite.config.ts
│       ├── .gitignore
│       ├── package.json
│       └── README.md
├── data/
│   ├── processed/
│   │   ├── cell_shards/
│   │   │   ├── sensor_family=MODIS/
│   │   │   │   ├── year=2020/
│   │   │   │   │   └── product_type=SP/
│   │   │   │   └── year=2021/
│   │   │   │       └── product_type=SP/
│   │   │   └── sensor_family=VIIRS/
│   │   │       ├── year=2020/
│   │   │       │   └── product_type=SP/
│   │   │       └── year=2021/
│   │   │           └── product_type=SP/
│   │   ├── observations/
│   │   │   ├── sensor_family=MODIS/
│   │   │   │   ├── year=2023/
│   │   │   │   │   └── product_type=SP/
│   │   │   │   └── year=2025/
│   │   │   │       └── product_type=SP/
│   │   │   └── sensor_family=VIIRS/
│   │   │       ├── year=2023/
│   │   │       │   └── product_type=SP/
│   │   │       ├── year=2024/
│   │   │       │   └── product_type=SP/
│   │   │       ├── year=2025/
│   │   │       │   └── product_type=SP/
│   │   │       └── year=2026/
│   │   │           └── product_type=NRT/
│   │   ├── archive_index.json
│   │   ├── daily_cell.parquet
│   │   ├── manifest.json
│   │   └── quality_report.json
│   └── raw/
│       ├── archives/
│       │   ├── MODIS_SP/
│       │   ├── VIIRS_NOAA20_SP/
│       │   ├── VIIRS_NOAA21_SP/
│       │   └── VIIRS_SNPP_SP/
│       ├── extracted/
│       └── README.txt
├── docs/
│   ├── API.md
│   ├── DATA_ENGINE.md
│   ├── HARMONIZATION.md
│   └── LIMITATIONS.md
├── frontend/
│   ├── src/
│   │   ├── data/
│   │   │   └── demo.ts
│   │   ├── lib/
│   │   │   ├── apiClient.test.ts
│   │   │   ├── apiClient.ts
│   │   │   ├── filters.test.ts
│   │   │   └── filters.ts
│   │   ├── ui/
│   │   │   ├── App.test.tsx
│   │   │   ├── App.tsx
│   │   │   ├── DataExplorer.test.tsx
│   │   │   ├── DataExplorer.tsx
│   │   │   ├── MapView.tsx
│   │   │   ├── ProcessedComparison.test.tsx
│   │   │   ├── ProcessedComparison.tsx
│   │   │   └── TimelineChart.tsx
│   │   ├── main.tsx
│   │   ├── styles.css
│   │   ├── testSetup.ts
│   │   └── vite-env.d.ts
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.tsbuildinfo
│   └── vite.config.ts
├── scripts/
│   └── dev.mjs
├── .env
├── .gitignore
├── AUDIT_REPORT.md
├── eslint.config.mjs
├── package-lock.json
├── package.json
├── process_2020_2026_compact.bat
├── PROJECT_STRUCTURE.md
├── README.md
└── start.bat
```

### Raw data folders

| Folder | Files | Size (GB) | Year range |
|---|---:|---:|---|
| `data/raw/archives/` | 0 | 0.00 | not encoded |
| `data/raw/extracted/` | 10,154 | 46.07 | 2000–2026 |

### Processed data files

MiB uses 1024² bytes. Rows/min/max date are from Parquet footer metadata (`acq_date`), when available.

| File | Size (MB) | Rows | min/max `acq_date` |
|---|---:|---:|---|
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/0063477b21263bbe.parquet` | 0.065 | 9,202 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/00d4b1107d12932b.parquet` | 1.063 | 170,199 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/03c342d965c18a49.parquet` | 0.010 | 921 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/065176bfe44fda03.parquet` | 0.086 | 14,043 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/0678711e17c28a07.parquet` | 0.184 | 31,106 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/06895e5b18cb9c6d.parquet` | 0.158 | 24,097 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/069c3706b1162f15.parquet` | 0.120 | 18,270 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/0825b2134f287512.parquet` | 0.054 | 7,383 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/08dee40c0887258a.parquet` | 0.003 | 34 | 2020-01-10 – 2020-12-06 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/09601dadf03d5759.parquet` | 0.005 | 343 | 2020-01-03 – 2020-12-06 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/0a09348ff3b8d8c6.parquet` | 0.026 | 3,250 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/0a22740476205c27.parquet` | 0.003 | 33 | 2020-03-25 – 2020-09-26 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/0a6ad1a92ca96f6f.parquet` | 0.002 | 2 | 2020-01-18 – 2020-04-07 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/0e94653ed315bbff.parquet` | 0.005 | 311 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/0f449871b8153e8c.parquet` | 0.003 | 35 | 2020-03-14 – 2020-09-17 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/0fa07d1bbea0ebb7.parquet` | 0.005 | 230 | 2020-01-03 – 2020-11-10 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/1020b37a5830db95.parquet` | 0.003 | 30 | 2020-01-08 – 2020-10-08 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/1105a0ec10ac6cca.parquet` | 0.003 | 9 | 2020-03-08 – 2020-09-08 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/115ec43d7d55bc88.parquet` | 0.003 | 10 | 2020-01-04 – 2020-11-23 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/13084da691385460.parquet` | 0.003 | 23 | 2020-01-03 – 2020-12-27 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/13f916794c21dc30.parquet` | 0.015 | 1,689 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/1520f9ece5da770d.parquet` | 0.002 | 2 | 2020-01-09 – 2020-02-26 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/1743ca733163742d.parquet` | 0.002 | 1 | 2020-05-23 – 2020-05-23 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/19885a7d3f6a565d.parquet` | 0.002 | 2 | 2020-05-25 – 2020-07-21 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/1a625f424c1a42ec.parquet` | 0.002 | 9 | 2020-01-29 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/1ab69ab79da1fc24.parquet` | 0.002 | 3 | 2020-05-19 – 2020-08-11 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/1c2fba2fd8c0e6d6.parquet` | 0.316 | 52,325 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/1f3a401537f7eef8.parquet` | 0.009 | 780 | 2020-01-04 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/1ff9029c1b305f4b.parquet` | 0.005 | 297 | 2020-01-24 – 2020-11-10 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/1ff98f3b03fdfca4.parquet` | 0.041 | 5,512 | 2020-01-02 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/235e273db6a35c57.parquet` | 0.003 | 21 | 2020-03-27 – 2020-08-19 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/268c5dcf8245aa40.parquet` | 0.011 | 1,081 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/283506c74c8911c7.parquet` | 0.005 | 299 | 2020-02-09 – 2020-12-24 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/283f6ee2682c7bad.parquet` | 0.004 | 86 | 2020-01-07 – 2020-11-27 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/2976b47f5d2e9632.parquet` | 0.002 | 2 | 2020-12-29 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/29a524a0687dbbed.parquet` | 0.009 | 887 | 2020-01-02 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/2b97fbc4a586b81f.parquet` | 0.004 | 95 | 2020-01-25 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/2beafd8a227e8723.parquet` | 0.105 | 17,129 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/2d7ded54cf66f1c5.parquet` | 0.003 | 45 | 2020-01-06 – 2020-12-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/2dc55e95dd5c142f.parquet` | 0.091 | 14,366 | 2020-01-03 – 2020-12-11 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/2e402307a57c88b7.parquet` | 0.003 | 19 | 2020-02-20 – 2020-12-11 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/2fb4381ad3016f29.parquet` | 0.004 | 85 | 2020-05-15 – 2020-11-23 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/31840f51d6e96426.parquet` | 0.002 | 2 | 2020-03-01 – 2020-03-29 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/3229b026f6870597.parquet` | 0.081 | 12,733 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/326bebbb42c2c6b9.parquet` | 0.007 | 548 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/32798ea5a8dc7e12.parquet` | 0.010 | 880 | 2020-01-13 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/327ff88e1dda4c71.parquet` | 0.003 | 7 | 2020-01-06 – 2020-07-06 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/331abfef8b408672.parquet` | 0.004 | 152 | 2020-01-10 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/33d9833299dd1ccf.parquet` | 0.183 | 26,800 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/35c65f52066ad9c3.parquet` | 0.005 | 276 | 2020-01-14 – 2020-12-11 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/3694aaf8204d08c8.parquet` | 0.011 | 1,150 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/36b6468dea8aa2d9.parquet` | 0.063 | 9,425 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/3758622cd17431ef.parquet` | 0.012 | 1,158 | 2020-01-02 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/3a10679ca5bd8b1e.parquet` | 0.008 | 759 | 2020-01-02 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/3a50266c68c73c9d.parquet` | 0.005 | 295 | 2020-01-03 – 2020-12-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/3a612558fe603d58.parquet` | 0.005 | 286 | 2020-01-03 – 2020-12-01 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/3c2a66b1da43dbc6.parquet` | 0.004 | 212 | 2020-01-05 – 2020-12-03 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/3ef3c069893f50c7.parquet` | 0.030 | 3,981 | 2020-01-07 – 2020-12-26 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/3f41ca21cd87f3e4.parquet` | 0.003 | 28 | 2020-02-21 – 2020-12-16 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/3f5b3e2093b36d0b.parquet` | 0.007 | 444 | 2020-01-06 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/41784011fb597723.parquet` | 0.124 | 19,294 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/428538c321d2a100.parquet` | 0.008 | 668 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/438327e08089c311.parquet` | 0.002 | 3 | 2020-04-26 – 2020-10-12 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/4458b68562ecb036.parquet` | 0.202 | 32,928 | 2020-01-02 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/44b5a8e98384975a.parquet` | 0.002 | 3 | 2020-07-27 – 2020-08-04 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/490643a80ff76874.parquet` | 0.542 | 89,917 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/49ddc227228f7ea1.parquet` | 0.071 | 10,496 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/4a28b79e58ac15ee.parquet` | 0.316 | 50,111 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/4eb45acd970d178e.parquet` | 0.003 | 51 | 2020-03-26 – 2020-10-12 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/4faf4713cd23c6a6.parquet` | 0.005 | 217 | 2020-01-26 – 2020-11-16 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/501a9c638c774d3f.parquet` | 0.067 | 10,324 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/5274132b27261394.parquet` | 0.028 | 3,853 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/5447c61be5cb669c.parquet` | 0.043 | 5,782 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/54c693485b8087f3.parquet` | 0.009 | 795 | 2020-01-06 – 2020-11-15 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/553a83e6643de3cc.parquet` | 0.003 | 24 | 2020-02-14 – 2020-12-04 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/59785245cedf21bb.parquet` | 0.002 | 3 | 2020-04-12 – 2020-06-20 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/5b89da85c783ac9b.parquet` | 0.041 | 5,676 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/5dd3396973433185.parquet` | 0.008 | 675 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/5ec46fdf6b901235.parquet` | 0.006 | 375 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/634586b724b817f7.parquet` | 0.003 | 11 | 2020-02-03 – 2020-05-18 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/6389712dd9ad6d90.parquet` | 0.117 | 18,426 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/641b686548d7e982.parquet` | 0.005 | 210 | 2020-01-08 – 2020-12-23 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/6514ea274a7d8b9e.parquet` | 0.004 | 104 | 2020-01-29 – 2020-11-06 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/65a3429ed9b9a778.parquet` | 0.106 | 16,082 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/65ee1d2ef40f8842.parquet` | 0.004 | 176 | 2020-01-07 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/67d7ea3390d59da2.parquet` | 0.002 | 2 | 2020-09-19 – 2020-09-19 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/67f03ac60aa4d0fa.parquet` | 0.019 | 2,302 | 2020-01-02 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/68c071fcf44eaf8d.parquet` | 0.003 | 41 | 2020-03-27 – 2020-09-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/68da3cf038dc0dcb.parquet` | 0.002 | 3 | 2020-08-05 – 2020-10-06 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/694948949b074c1c.parquet` | 0.003 | 25 | 2020-01-25 – 2020-11-26 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/6a92bffcf3b52b33.parquet` | 0.021 | 2,698 | 2020-01-01 – 2020-12-07 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/6c6d1bd494a2803a.parquet` | 0.005 | 240 | 2020-01-23 – 2020-10-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/6c95feb1578ceaec.parquet` | 0.377 | 53,413 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/6d94b6be2bc0308e.parquet` | 0.218 | 34,200 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/70d2149e0f60779b.parquet` | 0.175 | 26,907 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/728f12e44ea57cab.parquet` | 0.002 | 1 | 2020-06-25 – 2020-06-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/731c5806c61eef63.parquet` | 0.005 | 303 | 2020-01-07 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/7632e93b33236052.parquet` | 0.036 | 5,000 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/7637d53afed66f8b.parquet` | 0.002 | 1 | 2020-09-23 – 2020-09-23 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/76ee0369152e167d.parquet` | 0.008 | 728 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/777663474c7e680e.parquet` | 0.010 | 881 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/7aff846a65252a62.parquet` | 0.005 | 287 | 2020-02-03 – 2020-12-21 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/7df2fe1d55bddb12.parquet` | 0.007 | 581 | 2020-01-09 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/7eddcb6a4500de14.parquet` | 0.002 | 2 | 2020-09-20 – 2020-09-24 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/7edf2503fdf2d7aa.parquet` | 0.006 | 436 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/7ff947433027e328.parquet` | 0.003 | 13 | 2020-01-04 – 2020-08-16 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/8087a37ff82f9b1c.parquet` | 0.021 | 2,355 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/820098317d257c23.parquet` | 0.018 | 2,081 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/8238a7f81634d650.parquet` | 0.125 | 19,490 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/823ba34632210932.parquet` | 0.005 | 256 | 2020-01-03 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/82ee1e984e367719.parquet` | 0.003 | 39 | 2020-01-06 – 2020-11-12 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/8389a30a74d7ccf4.parquet` | 0.003 | 56 | 2020-03-19 – 2020-10-15 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/83b354dc36658df7.parquet` | 0.007 | 583 | 2020-01-07 – 2020-12-06 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/84f9f857978bd63b.parquet` | 0.124 | 18,705 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/87dfcc58324e9c11.parquet` | 0.004 | 111 | 2020-01-16 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/88612749bc7b5608.parquet` | 0.011 | 1,170 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/894a8cba20139d65.parquet` | 0.011 | 1,083 | 2020-01-04 – 2020-12-27 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/8964ed58f82d72c1.parquet` | 0.004 | 157 | 2020-01-01 – 2020-12-11 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/8b45bdd2c3b41378.parquet` | 0.203 | 32,130 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/8bf0f6d7bc07c674.parquet` | 0.002 | 4 | 2020-03-18 – 2020-06-03 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/8c0ed541c8d893dd.parquet` | 0.006 | 441 | 2020-01-04 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/8d2fae0dd3b02478.parquet` | 0.035 | 4,603 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/8ebc6e3c29f8effc.parquet` | 0.006 | 414 | 2020-01-03 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/90227242e721ed35.parquet` | 0.004 | 153 | 2020-01-02 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/92c320021afa6052.parquet` | 0.003 | 7 | 2020-04-09 – 2020-09-05 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/93896092724b1cfd.parquet` | 0.259 | 42,482 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/9440e4f706376c71.parquet` | 0.004 | 162 | 2020-02-02 – 2020-11-06 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/960cbe6d080e668c.parquet` | 0.030 | 3,904 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/9642ee097335f060.parquet` | 0.034 | 4,008 | 2020-01-01 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/9780d8162850b2c1.parquet` | 0.015 | 1,639 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/99c6d9eb67787b13.parquet` | 0.003 | 55 | 2020-01-06 – 2020-12-13 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a005435eaa7efc14.parquet` | 0.003 | 13 | 2020-01-24 – 2020-12-22 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a024054d5f460af8.parquet` | 0.004 | 165 | 2020-05-09 – 2020-12-02 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a050b8c7bb117d18.parquet` | 0.002 | 5 | 2020-01-05 – 2020-11-29 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a083df3b5002be6d.parquet` | 0.222 | 36,012 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a0dffbb3b6c3cc57.parquet` | 0.019 | 1,905 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a13a184532d77cf7.parquet` | 0.070 | 10,527 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a5057027b7777a81.parquet` | 0.004 | 112 | 2020-01-01 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a5f76974f27f980a.parquet` | 0.005 | 208 | 2020-01-02 – 2020-12-22 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a6a877816a4c6246.parquet` | 0.047 | 6,031 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a75ee478857cbef9.parquet` | 0.003 | 14 | 2020-02-24 – 2020-10-23 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a7a8edb8f16272a2.parquet` | 0.008 | 707 | 2020-01-03 – 2020-12-15 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/a8a6269bb0e74737.parquet` | 0.003 | 20 | 2020-01-06 – 2020-12-23 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/aa3ded5b9e43d1be.parquet` | 0.003 | 84 | 2020-04-19 – 2020-11-09 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/aadb1c76cf5cd32f.parquet` | 0.038 | 4,997 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/aceca919e248b80b.parquet` | 0.005 | 288 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/aef34827a3ddd7ce.parquet` | 0.097 | 13,407 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/afc53b6b8572f9f2.parquet` | 0.106 | 14,677 | 2020-01-04 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/b02e73c013092445.parquet` | 0.007 | 591 | 2020-01-14 – 2020-11-24 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/b0ce5f248f61833e.parquet` | 0.018 | 2,170 | 2020-01-01 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/b0fe7355437fb05c.parquet` | 0.002 | 2 | 2020-01-27 – 2020-02-12 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/b1eb8d542c0b261a.parquet` | 0.002 | 2 | 2020-02-13 – 2020-11-29 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/b2f0b82c932dcc79.parquet` | 0.005 | 247 | 2020-01-08 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/b45c7336c182670b.parquet` | 0.004 | 75 | 2020-03-03 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/b59b36a7a814db3e.parquet` | 0.002 | 1 | 2020-03-19 – 2020-03-19 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/b6329a9603a93f4e.parquet` | 0.020 | 2,303 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/b68f680ab2344cdd.parquet` | 0.005 | 298 | 2020-01-22 – 2020-10-13 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/b960ef141b24a5b9.parquet` | 0.880 | 140,744 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/b9bdd4822c9d8906.parquet` | 0.737 | 108,175 | 2020-01-03 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/bc0a283aed11a2ef.parquet` | 0.004 | 158 | 2020-01-05 – 2020-12-21 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/bf3f44b174740e0c.parquet` | 0.008 | 712 | 2020-01-24 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/bfc9bfb034a9394b.parquet` | 0.039 | 5,120 | 2020-01-10 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/c20927867eb1f774.parquet` | 0.003 | 15 | 2020-02-27 – 2020-12-07 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/c22595dec1b41b76.parquet` | 0.004 | 147 | 2020-02-01 – 2020-12-01 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/c321455737469e69.parquet` | 0.009 | 884 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/c4cb1435e12d8d71.parquet` | 0.017 | 1,718 | 2020-01-04 – 2020-12-17 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/c53130ab475b912b.parquet` | 0.016 | 1,526 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/c5bbe72d843b7996.parquet` | 0.316 | 47,266 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/c8ab2acecb1b10d8.parquet` | 0.352 | 60,452 | 2020-01-03 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/c9339649e3b42d13.parquet` | 0.017 | 1,760 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/c9b472bd9d197ca1.parquet` | 0.004 | 157 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/cb2fb82693751f4f.parquet` | 0.004 | 175 | 2020-01-03 – 2020-11-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/ce09753dc9646893.parquet` | 0.004 | 98 | 2020-05-05 – 2020-11-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/d5715654d75c2499.parquet` | 0.003 | 5 | 2020-07-15 – 2020-09-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/d800d6bf91874c0b.parquet` | 0.049 | 6,717 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/d98270fe711e414f.parquet` | 0.053 | 6,272 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/db274532ef05e43d.parquet` | 0.041 | 5,980 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/db999dd2bb637ce6.parquet` | 0.347 | 53,329 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/dbbd5593ad17257d.parquet` | 0.022 | 2,450 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/dcb6e9f05fa1b174.parquet` | 0.099 | 15,671 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/dd0dac57a405be11.parquet` | 0.012 | 1,237 | 2020-01-01 – 2020-12-19 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/dd70df2a57c16c17.parquet` | 0.002 | 4 | 2020-03-01 – 2020-09-05 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/e1f26fbae914ad21.parquet` | 0.099 | 17,523 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/e314018f8e1c8a31.parquet` | 0.007 | 572 | 2020-01-16 – 2020-12-26 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/e336185b5eb79f46.parquet` | 0.038 | 4,790 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/e360262e92c49968.parquet` | 0.003 | 12 | 2020-05-17 – 2020-08-16 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/e37618e486bc92ed.parquet` | 0.018 | 1,986 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/e706f666c38a527d.parquet` | 0.002 | 1 | 2020-08-10 – 2020-08-10 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/ec378461cfd89099.parquet` | 0.007 | 545 | 2020-01-07 – 2020-12-26 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/ece8eccc5c4a2436.parquet` | 0.003 | 59 | 2020-02-01 – 2020-12-08 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/ee1db2ea3e311d07.parquet` | 0.003 | 47 | 2020-04-14 – 2020-11-21 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/eea6180094995217.parquet` | 0.002 | 1 | 2020-10-24 – 2020-10-24 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f115e0d3b38037c8.parquet` | 0.013 | 1,308 | 2020-01-02 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f2b2ce7f77b9bc76.parquet` | 0.036 | 4,661 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f30d12ef3ac62ef5.parquet` | 0.020 | 2,072 | 2020-01-10 – 2020-12-10 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f3762f0b74214aa6.parquet` | 0.125 | 19,967 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f3cb657c908092ea.parquet` | 0.005 | 296 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f5d12bd0590425a5.parquet` | 0.003 | 81 | 2020-03-01 – 2020-10-08 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f73b9bbca0cee64d.parquet` | 0.006 | 391 | 2020-01-03 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f8ae91416c66b15d.parquet` | 0.012 | 1,152 | 2020-01-03 – 2020-12-27 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f8e90e00db1a99ae.parquet` | 0.004 | 110 | 2020-01-02 – 2020-12-26 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f92a733ff5c9733b.parquet` | 0.023 | 2,812 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f962b575b8e91f36.parquet` | 0.201 | 30,005 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f96d3f84ac26ba74.parquet` | 0.002 | 1 | 2020-05-21 – 2020-05-21 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f9b92560716afde8.parquet` | 0.004 | 116 | 2020-03-11 – 2020-10-29 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/f9e27050d07a5e7a.parquet` | 0.004 | 147 | 2020-01-03 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/fa5b2e67ac10eeb2.parquet` | 0.181 | 30,562 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/fc07f1f0744af660.parquet` | 0.002 | 2 | 2020-05-25 – 2020-05-26 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/fc11098d45a6b8a4.parquet` | 0.267 | 46,243 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/ff7d9c696e192fe0.parquet` | 0.006 | 406 | 2020-01-06 – 2020-12-24 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2020/product_type=SP/product=MODIS_SP/ffb5ffbcb7ebb508.parquet` | 0.004 | 170 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/0099c96635da74d9.parquet` | 0.003 | 17 | 2021-01-02 – 2021-11-24 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/031d153630a50082.parquet` | 0.004 | 124 | 2021-02-06 – 2021-11-13 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/035f2e5b3cf5e772.parquet` | 0.005 | 245 | 2021-01-15 – 2021-12-17 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/03f7ee915b955a60.parquet` | 0.030 | 3,760 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/05e1ed4092e12c60.parquet` | 0.135 | 20,262 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/07f1596fff6272ea.parquet` | 0.002 | 8 | 2021-04-15 – 2021-05-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/08caccc9bcff876f.parquet` | 0.003 | 15 | 2021-05-09 – 2021-08-22 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/0b52d918d8cc9e08.parquet` | 0.029 | 3,770 | 2021-01-07 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/0b9917a317090aef.parquet` | 0.004 | 115 | 2021-01-10 – 2021-12-04 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/0ce579a0fd739114.parquet` | 0.004 | 196 | 2021-01-25 – 2021-11-23 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/0e967de6f4d79572.parquet` | 0.005 | 281 | 2021-01-02 – 2021-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/10470b8935467448.parquet` | 0.003 | 10 | 2021-01-21 – 2021-06-21 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/10535fd37e10939a.parquet` | 0.002 | 4 | 2021-03-20 – 2021-11-08 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/108a3544d93f383b.parquet` | 0.015 | 1,495 | 2021-01-04 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/11de9ddacefd179c.parquet` | 0.020 | 2,351 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/12ee4b15acc85cc7.parquet` | 0.004 | 106 | 2021-03-12 – 2021-12-14 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/134f65ec8e9cd57e.parquet` | 0.003 | 31 | 2021-02-28 – 2021-09-19 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/1440a54d6a155fb7.parquet` | 0.004 | 97 | 2021-02-28 – 2021-11-15 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/14fda5f99ed7c04c.parquet` | 0.186 | 27,333 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/17e6359180781f84.parquet` | 0.010 | 941 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/17f0ea55f9ce65fc.parquet` | 0.002 | 2 | 2021-04-17 – 2021-08-07 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/1cc6b9ce2f3826a3.parquet` | 0.075 | 11,146 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/1d103945edf675c3.parquet` | 0.004 | 179 | 2021-01-01 – 2021-12-21 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/1f15ccdefde48eb4.parquet` | 0.033 | 4,277 | 2021-01-09 – 2021-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/214c2f5e288b66cf.parquet` | 0.021 | 2,509 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/2188b67cb40b6ab5.parquet` | 0.003 | 14 | 2021-04-27 – 2021-12-01 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/221e5a0b07eb09c3.parquet` | 0.033 | 4,587 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/28fea0ff327791a5.parquet` | 0.010 | 809 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/29b5e5d75a0b26ae.parquet` | 0.033 | 3,955 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/29f4875b3f45225d.parquet` | 0.004 | 157 | 2021-01-01 – 2021-12-17 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/2c6e7a59e20255fd.parquet` | 0.003 | 71 | 2021-01-01 – 2021-11-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/2dc9e98bb5d35a78.parquet` | 0.004 | 169 | 2021-01-23 – 2021-12-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/2f64cec14ad9c97a.parquet` | 0.003 | 10 | 2021-04-08 – 2021-12-02 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/34f982aff77413ef.parquet` | 0.008 | 723 | 2021-01-02 – 2021-12-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/3916996d2e046459.parquet` | 0.006 | 389 | 2021-01-02 – 2021-12-19 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/3995d4e5da6ed88f.parquet` | 0.004 | 97 | 2021-01-16 – 2021-12-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/3b9a50cc1296a5e7.parquet` | 0.066 | 9,693 | 2021-01-04 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/3be45340fe61af99.parquet` | 0.015 | 1,627 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/3d536624501880c3.parquet` | 0.004 | 90 | 2021-01-14 – 2021-12-02 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/41e2dc1c3ee0508b.parquet` | 0.007 | 521 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/44be587ca1c630dc.parquet` | 0.407 | 58,262 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/4665566090ce0dfa.parquet` | 0.002 | 2 | 2021-03-04 – 2021-07-08 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/4887a464681c22a7.parquet` | 0.111 | 16,477 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/4957384c1b768035.parquet` | 0.010 | 904 | 2021-01-05 – 2021-12-16 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/497098e033deed43.parquet` | 0.056 | 8,390 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/4c65330f2091ce88.parquet` | 0.006 | 392 | 2021-02-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/4e97d17ac7ce9ad4.parquet` | 0.142 | 21,070 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/50082e7d2fdbc6e5.parquet` | 0.004 | 121 | 2021-03-03 – 2021-08-29 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/50a83835d95de45f.parquet` | 0.225 | 36,972 | 2021-01-04 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/52bcc99c31e253ca.parquet` | 0.380 | 55,998 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/52be716d09f9f0ce.parquet` | 0.022 | 2,884 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/5483f3d712a26e01.parquet` | 0.003 | 35 | 2021-01-01 – 2021-12-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/54a1c7d7b68cc489.parquet` | 0.126 | 19,174 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/550ba539fc059c94.parquet` | 0.009 | 766 | 2021-01-01 – 2021-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/5683dcdebea202ed.parquet` | 0.003 | 19 | 2021-05-18 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/574b0307a3ae028c.parquet` | 0.004 | 115 | 2021-01-06 – 2021-11-27 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/583b67b4ed910065.parquet` | 0.007 | 500 | 2021-01-02 – 2021-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/58e6e2efbe296544.parquet` | 0.022 | 2,772 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/590bde504072feb8.parquet` | 0.002 | 1 | 2021-11-30 – 2021-11-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/591b4dbcdcfd3019.parquet` | 0.004 | 117 | 2021-01-03 – 2021-12-24 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/59f3899080931b61.parquet` | 0.004 | 175 | 2021-01-10 – 2021-12-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/5ac177d41517e2e3.parquet` | 0.261 | 46,112 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/5ba0748076d20f47.parquet` | 0.002 | 4 | 2021-05-26 – 2021-08-05 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/5d847f089f5cc930.parquet` | 0.013 | 1,324 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/5d8aff7dfefe235b.parquet` | 0.024 | 2,823 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/61cc1015ab3a4f6e.parquet` | 0.338 | 51,499 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/623e1f13f7569e2f.parquet` | 0.019 | 1,994 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/6240f8bda126c9d0.parquet` | 0.008 | 774 | 2021-01-20 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/631c2d2ad6f98fe5.parquet` | 0.059 | 10,092 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/64090aa9631983a3.parquet` | 0.007 | 621 | 2021-02-26 – 2021-11-20 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/642a5d9229efa470.parquet` | 0.006 | 460 | 2021-01-04 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/64d77a3de1622aa7.parquet` | 0.052 | 7,031 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/655672dcdc89374c.parquet` | 0.008 | 607 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/65b9eeb8320c28f3.parquet` | 0.006 | 453 | 2021-01-09 – 2021-12-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/667c0c01a8047e9f.parquet` | 0.003 | 10 | 2021-03-18 – 2021-08-03 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/66aaaf857d0d6ac1.parquet` | 0.011 | 940 | 2021-01-01 – 2021-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/6cd31b5608a38784.parquet` | 0.005 | 205 | 2021-01-04 – 2021-12-26 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/6d2ffdf1aaaa22fe.parquet` | 0.158 | 23,575 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/6e77a58846c6b959.parquet` | 0.026 | 3,189 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/6fb69ed2cb456c77.parquet` | 0.160 | 26,742 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/738a8eb9d8ac5de2.parquet` | 0.017 | 1,715 | 2021-01-01 – 2021-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/7410378cdc4c0f00.parquet` | 0.003 | 36 | 2021-03-27 – 2021-10-08 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/7462c6079ccbebd6.parquet` | 0.109 | 17,473 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/749c404d4111ce48.parquet` | 0.061 | 9,183 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/7666adf929715b8d.parquet` | 0.004 | 139 | 2021-01-02 – 2021-12-18 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/76822b146a180704.parquet` | 0.004 | 80 | 2021-02-20 – 2021-11-17 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/7799701aea80db52.parquet` | 0.691 | 96,694 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/7822ea675b584f7d.parquet` | 0.076 | 10,196 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/782aec261c3e6e52.parquet` | 0.013 | 1,310 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/78eeee99b82f72f3.parquet` | 0.004 | 142 | 2021-01-11 – 2021-10-14 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/7a83c40836eae239.parquet` | 0.007 | 426 | 2021-01-03 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/7b2037ca7ce97a46.parquet` | 0.182 | 29,885 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/7cf1e498c0073786.parquet` | 0.011 | 1,164 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/8053a1830235826b.parquet` | 0.040 | 5,586 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/8129b3365bc37d8d.parquet` | 0.002 | 3 | 2021-07-25 – 2021-08-05 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/818bd03abb72429a.parquet` | 0.004 | 101 | 2021-01-03 – 2021-12-15 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/82ffb1ba4ef3b078.parquet` | 0.015 | 1,631 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/830f3432fca649b4.parquet` | 0.220 | 34,412 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/846a3b04cc46d463.parquet` | 0.002 | 2 | 2021-05-14 – 2021-11-06 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/84c766a4a85c336b.parquet` | 0.014 | 1,531 | 2021-01-01 – 2021-12-27 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/84c76a1336287982.parquet` | 0.002 | 2 | 2021-09-21 – 2021-11-24 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/853c19ac92b0bf55.parquet` | 0.003 | 21 | 2021-02-27 – 2021-08-17 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/85f088eed33edd8f.parquet` | 0.002 | 4 | 2021-02-11 – 2021-10-20 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/87e5a7d70e47c62a.parquet` | 0.901 | 143,822 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/882840a2289a3fd5.parquet` | 0.004 | 196 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/898517217ec673cb.parquet` | 0.002 | 2 | 2021-12-15 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/898fb9a90dca001b.parquet` | 0.003 | 22 | 2021-01-04 – 2021-12-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/8b161cf55ed96ef7.parquet` | 0.584 | 96,652 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/8bcad9fae7fba40e.parquet` | 0.067 | 9,833 | 2021-01-05 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/8cf1b499ca21a7c8.parquet` | 0.073 | 11,057 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/8d45e1afb0deec10.parquet` | 0.003 | 35 | 2021-01-23 – 2021-12-16 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/8e65c9a9fda43c6a.parquet` | 0.007 | 528 | 2021-01-02 – 2021-12-18 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/90bc31e3d3119696.parquet` | 0.005 | 240 | 2021-03-10 – 2021-11-12 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/92caebcd90a73061.parquet` | 0.003 | 11 | 2021-03-07 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/934bd1fa2dd69901.parquet` | 0.923 | 149,735 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/93c7e08dddba5c76.parquet` | 0.389 | 66,597 | 2021-01-04 – 2021-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/9594c75b91656e8a.parquet` | 0.184 | 22,135 | 2021-01-01 – 2021-12-14 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/95dc9b27c683e9c6.parquet` | 0.007 | 568 | 2021-03-22 – 2021-10-14 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/9649de47c36e21bb.parquet` | 0.005 | 294 | 2021-01-01 – 2021-12-24 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/98ea2cad26a4ccad.parquet` | 0.003 | 49 | 2021-02-21 – 2021-11-09 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/9c07c40ef346d552.parquet` | 0.006 | 390 | 2021-02-22 – 2021-11-07 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/a3daf45844880d9d.parquet` | 0.006 | 392 | 2021-01-01 – 2021-12-27 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/a607e2f8c115d2bb.parquet` | 0.006 | 399 | 2021-01-01 – 2021-12-19 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/a645be899ac86184.parquet` | 0.091 | 12,093 | 2021-01-04 – 2021-12-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/a687fad84b9e94b0.parquet` | 0.083 | 12,748 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/a6d84443ae33afd3.parquet` | 0.005 | 214 | 2021-01-13 – 2021-12-27 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/a87e01485ccac69d.parquet` | 0.008 | 739 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/a9bda27459133de0.parquet` | 0.003 | 9 | 2021-03-31 – 2021-11-13 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/aab4ce046763b488.parquet` | 0.003 | 44 | 2021-01-09 – 2021-11-20 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/adc51766316eeb45.parquet` | 0.027 | 3,335 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ade757b8996f6168.parquet` | 0.100 | 16,368 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/b0f77ba580e5c050.parquet` | 0.057 | 6,953 | 2021-01-28 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/b241e12c4af6a6a5.parquet` | 0.007 | 519 | 2021-02-04 – 2021-11-09 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/b29064cd300b13a0.parquet` | 0.051 | 7,188 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/b2c02ce9545f2fa1.parquet` | 0.002 | 4 | 2021-09-02 – 2021-09-02 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/b58584ef0e0d5c84.parquet` | 0.006 | 412 | 2021-01-23 – 2021-12-27 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/b5cb4e425a797c6d.parquet` | 0.277 | 47,537 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/b795fba86abbb723.parquet` | 0.028 | 3,881 | 2021-01-01 – 2021-12-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/b9b9d596d8b58a9f.parquet` | 0.003 | 35 | 2021-01-23 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ba43c95d7cceb55a.parquet` | 0.003 | 50 | 2021-04-14 – 2021-10-21 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/bb3f8e71b62a85cb.parquet` | 0.005 | 275 | 2021-01-03 – 2021-12-16 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/bc94642039f7cc01.parquet` | 0.005 | 286 | 2021-02-01 – 2021-11-16 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/bd518c06ae399a80.parquet` | 0.005 | 289 | 2021-01-17 – 2021-11-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/bf51c26d82b601cc.parquet` | 0.003 | 53 | 2021-01-13 – 2021-12-29 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/c12c2fa6cfce7795.parquet` | 0.003 | 5 | 2021-05-03 – 2021-10-06 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/c29d4b600c836c8f.parquet` | 0.014 | 1,451 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/c372c3ab2ec93bfc.parquet` | 0.053 | 7,264 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/c47f2d98bdb6986c.parquet` | 0.003 | 69 | 2021-02-20 – 2021-10-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/c763ab091b5f31ed.parquet` | 0.188 | 27,419 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/c8a0ebf400a42bb1.parquet` | 0.002 | 4 | 2021-07-04 – 2021-10-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/c8dd98d5f6185a9a.parquet` | 0.048 | 6,994 | 2021-01-08 – 2021-12-04 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/caabf044548ba036.parquet` | 0.008 | 658 | 2021-01-01 – 2021-12-08 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/cab4be46df190451.parquet` | 0.004 | 93 | 2021-01-18 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/cd1ff0832bf27748.parquet` | 0.003 | 30 | 2021-04-11 – 2021-11-02 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/cdd1d38e880b1a51.parquet` | 0.020 | 1,886 | 2021-01-02 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ce1eaf1bccd56573.parquet` | 0.002 | 1 | 2021-02-23 – 2021-02-23 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/cf3d5157c7d55f31.parquet` | 0.032 | 4,244 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/d099b62db850087b.parquet` | 0.036 | 4,488 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/d14ad396645038b0.parquet` | 0.278 | 46,526 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/d454e6efc48323ba.parquet` | 0.040 | 4,700 | 2021-01-05 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/d60b48abe588d972.parquet` | 0.002 | 1 | 2021-06-03 – 2021-06-03 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/d6e105c4399b2c26.parquet` | 0.005 | 236 | 2021-02-22 – 2021-11-17 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/d85a455fa9850668.parquet` | 0.003 | 66 | 2021-02-26 – 2021-10-29 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/d929949dad3f0b08.parquet` | 0.005 | 310 | 2021-01-22 – 2021-11-22 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/dae22a762bca0c6c.parquet` | 0.004 | 185 | 2021-02-04 – 2021-11-01 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/daf29b3d5c5e74ec.parquet` | 0.052 | 7,697 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/db92cd3264df42de.parquet` | 0.019 | 1,894 | 2021-01-03 – 2021-12-30 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/de64f9a0dd990f4e.parquet` | 0.004 | 180 | 2021-01-16 – 2021-12-17 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/dfd93c3a43901953.parquet` | 0.003 | 46 | 2021-04-12 – 2021-10-08 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/e370234a635a3281.parquet` | 0.099 | 15,349 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/e3a6d3c8a276f2d0.parquet` | 0.002 | 2 | 2021-09-30 – 2021-10-20 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/e45d1653a953c25a.parquet` | 0.002 | 1 | 2021-10-19 – 2021-10-19 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/e616aa646fe54953.parquet` | 0.004 | 215 | 2021-01-12 – 2021-12-23 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/e6e30176d81cc735.parquet` | 0.004 | 174 | 2021-01-01 – 2021-12-05 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/e8618e546dc640ab.parquet` | 0.009 | 648 | 2021-01-04 – 2021-12-04 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ea0048afd0f11e50.parquet` | 0.007 | 623 | 2021-01-09 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/eadbe38b2486552c.parquet` | 0.007 | 569 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/eb3a24f783b15ecd.parquet` | 0.004 | 84 | 2021-02-11 – 2021-12-11 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ecdea5c468b604fc.parquet` | 0.047 | 7,356 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ed40b4d35438da0f.parquet` | 0.036 | 4,538 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ed40d881be9bd255.parquet` | 0.003 | 23 | 2021-01-06 – 2021-11-23 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ed57ac6666be3e26.parquet` | 0.122 | 17,787 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ee2b425ed3a98027.parquet` | 0.016 | 1,905 | 2021-02-05 – 2021-12-22 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ef3b3479d14354ba.parquet` | 0.270 | 44,026 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/efff069cbed9792d.parquet` | 0.015 | 1,612 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/f15e9ea441cc0269.parquet` | 0.008 | 636 | 2021-01-10 – 2021-12-27 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/f30ab403e0ac536a.parquet` | 0.002 | 9 | 2021-03-13 – 2021-11-08 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/f580776a70f7fc0b.parquet` | 0.005 | 265 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/f6afcb5136df0bbf.parquet` | 0.004 | 109 | 2021-01-04 – 2021-12-06 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/f785c7326557b5c4.parquet` | 0.002 | 2 | 2021-02-26 – 2021-03-04 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/f84a8895190bc2e8.parquet` | 0.003 | 35 | 2021-01-10 – 2021-12-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/f8a42c1fd7a95b45.parquet` | 0.002 | 2 | 2021-12-23 – 2021-12-26 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/f98e81f2f283c1dc.parquet` | 0.004 | 173 | 2021-01-01 – 2021-12-25 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/fa4e6472bb28ead3.parquet` | 0.093 | 15,482 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/fb425da71c8c7830.parquet` | 0.136 | 20,133 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/fb64843004818176.parquet` | 0.007 | 537 | 2021-02-22 – 2021-11-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/fc150001317e02a3.parquet` | 0.004 | 141 | 2021-02-27 – 2021-11-20 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/fc9b2e05ac6557e4.parquet` | 0.016 | 1,826 | 2021-01-03 – 2021-12-28 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/fcb7c07f06577398.parquet` | 0.004 | 124 | 2021-01-05 – 2021-11-03 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/fcfebeb35021141d.parquet` | 0.160 | 23,450 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/fd3db280f07ef11f.parquet` | 0.007 | 503 | 2021-02-07 – 2021-11-21 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/feb3dda0563f9099.parquet` | 0.005 | 260 | 2021-02-01 – 2021-12-02 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ff3f5e9337312ebe.parquet` | 0.003 | 79 | 2021-02-15 – 2021-12-24 |
| `data/processed/cell_shards/sensor_family=MODIS/year=2021/product_type=SP/product=MODIS_SP/ff90c6305da3ff0e.parquet` | 0.004 | 213 | 2021-01-02 – 2021-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/0053f5e567304a94.parquet` | 0.292 | 40,743 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/0065242fab8caffb.parquet` | 0.138 | 17,665 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/012fc6c5535f6cfa.parquet` | 0.008 | 559 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/04b84c5cec77a8b0.parquet` | 0.003 | 61 | 2020-01-02 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/0533f5804f7ecc57.parquet` | 0.003 | 46 | 2020-01-16 – 2020-10-14 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/05b6f8e7fa3b4ee6.parquet` | 0.067 | 8,400 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/062d39e9629cb031.parquet` | 0.003 | 5 | 2020-02-07 – 2020-05-14 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/0635d43382e5af4d.parquet` | 1.408 | 180,027 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/065ef156da3d17d1.parquet` | 0.007 | 422 | 2020-01-04 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/066b94692c9aa3cf.parquet` | 0.995 | 143,678 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/06d32380b656d4e3.parquet` | 0.295 | 40,673 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/09172dd0475d544d.parquet` | 0.380 | 61,858 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/0b7d8a44660997ff.parquet` | 0.002 | 2 | 2020-08-28 – 2020-11-23 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/0bc3f2030e739cf8.parquet` | 0.008 | 545 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/0c9a11c299e09134.parquet` | 0.002 | 7 | 2020-02-16 – 2020-09-26 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/0e6e4593bb8b67f4.parquet` | 0.038 | 4,368 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/0e8b15acae4ba594.parquet` | 0.006 | 400 | 2020-01-07 – 2020-12-04 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/104443c688be5e1b.parquet` | 0.269 | 37,713 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/12b4512c6b19692d.parquet` | 0.025 | 2,717 | 2020-01-01 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/1462d223eec472d4.parquet` | 0.003 | 13 | 2020-01-31 – 2020-12-10 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/15fe2184004fc1f2.parquet` | 0.036 | 3,526 | 2020-01-01 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/16e389b5106898a6.parquet` | 0.002 | 1 | 2020-04-21 – 2020-04-21 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/17150daf6f86b551.parquet` | 1.089 | 181,005 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/171c6a26b12b3870.parquet` | 0.002 | 4 | 2020-03-13 – 2020-04-05 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/177d2a3587117430.parquet` | 0.230 | 31,739 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/19939606aa4f729d.parquet` | 0.010 | 889 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/1a5becc97d3f023c.parquet` | 0.010 | 947 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/1b4f86fe869c7233.parquet` | 0.079 | 10,341 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/1bd9067e610bb29c.parquet` | 0.010 | 903 | 2020-01-01 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/1d167653e1aa61fd.parquet` | 0.011 | 968 | 2020-01-01 – 2020-12-26 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/1d3854b0ca94c7af.parquet` | 0.004 | 143 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/1e01b86dfd26abd6.parquet` | 0.004 | 182 | 2020-01-02 – 2020-12-16 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/20181ed1f0e4bdf0.parquet` | 0.012 | 1,083 | 2020-01-01 – 2020-12-18 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/203fbaf34bb9907b.parquet` | 0.212 | 27,362 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/21353e664e3c870f.parquet` | 0.026 | 2,926 | 2020-01-03 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/226ddd5c6c7ca321.parquet` | 0.332 | 46,981 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/23aef13042744df7.parquet` | 0.052 | 6,062 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/24834b12eb57fa1d.parquet` | 0.008 | 477 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/26888bba1c661309.parquet` | 0.025 | 2,889 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/2a90eff24e74f0a5.parquet` | 0.020 | 2,181 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/2cf76263f0f756db.parquet` | 0.020 | 2,096 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/2e734f206dbc456b.parquet` | 0.040 | 4,821 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/319acde75610f5a9.parquet` | 0.018 | 1,716 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/32b53ca70bae874b.parquet` | 0.912 | 126,716 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/3611b606917cb969.parquet` | 0.012 | 1,236 | 2020-01-01 – 2020-12-18 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/37d57d9189edb87c.parquet` | 0.012 | 1,148 | 2020-01-01 – 2020-12-27 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/37feeae4841f39f0.parquet` | 0.326 | 46,816 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/385825295246bf85.parquet` | 0.003 | 5 | 2020-11-28 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/39695719b050484b.parquet` | 0.034 | 4,117 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/39ed6ceeb837adec.parquet` | 0.004 | 127 | 2020-01-02 – 2020-12-17 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/3b25419c0ff63b92.parquet` | 0.007 | 584 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/3c4c6fb5ef31ad28.parquet` | 0.542 | 78,293 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/3d5b08376c6eddd3.parquet` | 0.038 | 4,465 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/3eb0fdad766138e4.parquet` | 0.011 | 879 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/3ec6d14e3175bc63.parquet` | 1.208 | 160,141 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/3f18f7b1479dec04.parquet` | 0.004 | 73 | 2020-01-25 – 2020-10-01 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/3f4dacf10d386673.parquet` | 0.005 | 295 | 2020-01-16 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/41ecfb53a3f2b4e7.parquet` | 0.004 | 78 | 2020-02-10 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/4230fe96c86c1977.parquet` | 0.002 | 4 | 2020-06-07 – 2020-10-09 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/4245a7a22705e4b5.parquet` | 0.653 | 89,664 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/42747370b5fb0013.parquet` | 0.002 | 1 | 2020-10-09 – 2020-10-09 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/4362b2f32bac867f.parquet` | 0.180 | 24,218 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/43d0cf42a58db379.parquet` | 0.071 | 10,209 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/47303c9883f235d4.parquet` | 0.023 | 2,659 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/48280896e37e2c40.parquet` | 0.016 | 1,423 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/4a1844ebfb8f019b.parquet` | 0.005 | 207 | 2020-01-10 – 2020-12-21 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/4a5844ff02ab1c49.parquet` | 0.002 | 2 | 2020-05-14 – 2020-05-23 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/4ab75de59f6262e2.parquet` | 0.005 | 254 | 2020-01-01 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/4e0e03c01df9d941.parquet` | 0.203 | 28,704 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/5069e18337cc5b9b.parquet` | 0.114 | 15,936 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/5703461def7e26b1.parquet` | 0.014 | 1,284 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/57f5aaba7104b93e.parquet` | 0.009 | 787 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/59aace70fc929b6a.parquet` | 0.002 | 1 | 2020-08-24 – 2020-08-24 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/5b56ef13ecc5c60d.parquet` | 0.002 | 2 | 2020-09-13 – 2020-09-18 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/5d06ada7f7f43440.parquet` | 2.076 | 269,003 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/61700c0b25ae8e08.parquet` | 0.002 | 1 | 2020-07-04 – 2020-07-04 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/62c5c6af016b2c7e.parquet` | 0.002 | 2 | 2020-04-24 – 2020-07-24 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/63b2ec0692a25008.parquet` | 0.015 | 1,466 | 2020-01-03 – 2020-12-11 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/63b9aafa2e40eb4f.parquet` | 0.002 | 1 | 2020-04-13 – 2020-04-13 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/666e85de27dcba47.parquet` | 0.002 | 1 | 2020-09-21 – 2020-09-21 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/66808fcf3d0b6d5a.parquet` | 0.015 | 1,351 | 2020-01-01 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/66a1877ea3bf6b42.parquet` | 0.064 | 8,491 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/677ceeca4e7d9c94.parquet` | 0.072 | 10,861 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/67fd382e53c820bf.parquet` | 0.930 | 143,936 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/68c0e101809deaca.parquet` | 0.004 | 97 | 2020-01-02 – 2020-12-12 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/6b501031c3efaf2d.parquet` | 0.015 | 1,472 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/6c0b3e80a4b2141f.parquet` | 0.090 | 12,606 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/6d23b8b80906d22a.parquet` | 0.019 | 2,104 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/6fe1a6c1d3c6912e.parquet` | 0.008 | 539 | 2020-01-01 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7182bde80adf3cb7.parquet` | 0.002 | 6 | 2020-01-24 – 2020-08-14 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/739893b383c62a26.parquet` | 0.003 | 54 | 2020-01-01 – 2020-10-23 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7440d78f2dacfb1f.parquet` | 0.004 | 121 | 2020-03-11 – 2020-12-09 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/756ed6c42c999f18.parquet` | 0.019 | 1,929 | 2020-01-01 – 2020-12-24 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/75c7e603e2bfe36b.parquet` | 0.053 | 7,190 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/77404d72ac35c131.parquet` | 0.003 | 23 | 2020-03-24 – 2020-11-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/78e5565e51eb7d3e.parquet` | 0.327 | 50,768 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7941f6a2e5217f71.parquet` | 0.112 | 15,558 | 2020-01-24 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/79ae51c179e245d1.parquet` | 0.030 | 3,490 | 2020-01-01 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7ba17b4c1874a055.parquet` | 0.231 | 32,490 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7cd0eeb09c2b9770.parquet` | 0.009 | 753 | 2020-01-08 – 2020-12-23 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7cd2d11c42b968ac.parquet` | 0.004 | 66 | 2020-01-04 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7cffbb96e3b77b79.parquet` | 0.006 | 316 | 2020-01-11 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7db34a7ffeade2a3.parquet` | 0.043 | 5,170 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7dc305c878478c3a.parquet` | 0.008 | 556 | 2020-01-01 – 2020-12-27 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7e42bd9e3a7d46fe.parquet` | 0.007 | 578 | 2020-01-06 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7e65af44b7e483fd.parquet` | 0.009 | 686 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7ecb4b31606a3eff.parquet` | 0.003 | 15 | 2020-01-06 – 2020-11-16 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/7edcdb2316d3c9f1.parquet` | 0.009 | 675 | 2020-01-01 – 2020-12-25 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/8012d51898f90c9c.parquet` | 0.096 | 15,709 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/88b841c761ee4a40.parquet` | 0.002 | 2 | 2020-09-06 – 2020-11-07 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/88fb325df033e77b.parquet` | 0.115 | 17,291 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/89cc3a22f34b8c5a.parquet` | 0.607 | 90,239 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/89eecc81edd7f453.parquet` | 0.011 | 1,008 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/8a2310f8ccc59574.parquet` | 0.007 | 405 | 2020-01-02 – 2020-12-23 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/8a4d042c620f8771.parquet` | 0.078 | 9,773 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/8a9cff0eac192abd.parquet` | 0.003 | 15 | 2020-01-27 – 2020-12-07 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/8b4aa1165fd60dd3.parquet` | 0.013 | 1,228 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/8e19170fe3e5b432.parquet` | 0.269 | 36,841 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/8f0e83ed7f7c0942.parquet` | 0.390 | 55,249 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/8fdc25616624492c.parquet` | 0.021 | 2,183 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/93bfc7fe8dfcee22.parquet` | 0.004 | 89 | 2020-01-03 – 2020-12-25 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/93e12d7ff27a40ec.parquet` | 0.013 | 1,248 | 2020-01-04 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/940b841fc958b7fd.parquet` | 0.002 | 1 | 2020-06-22 – 2020-06-22 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/947ca0d47e545a5e.parquet` | 0.003 | 30 | 2020-01-07 – 2020-06-15 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/9642daf0361045cd.parquet` | 0.140 | 18,953 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/965386fb006e5dcc.parquet` | 0.085 | 11,931 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/9a40196927d5f6bc.parquet` | 0.003 | 10 | 2020-02-10 – 2020-10-24 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/9cbceb2421fb056a.parquet` | 0.002 | 1 | 2020-03-31 – 2020-03-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/9e0cbe88078c26b8.parquet` | 0.026 | 2,946 | 2020-01-03 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/9e8c39abbfdf71f5.parquet` | 2.554 | 351,328 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/9f07d321cc88bb89.parquet` | 0.164 | 23,642 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a085cc684d582506.parquet` | 0.837 | 113,297 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a0a5d85e0cd88e7e.parquet` | 0.059 | 7,783 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a1e673769fb124c1.parquet` | 0.025 | 2,872 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a29e4e9d9aa8787c.parquet` | 0.019 | 1,982 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a32875d8084e3c8e.parquet` | 0.003 | 23 | 2020-02-13 – 2020-10-06 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a578570e9ff6a127.parquet` | 0.014 | 1,460 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a5aa810b1382f6c4.parquet` | 0.333 | 45,941 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a627cc2bd62c2002.parquet` | 0.003 | 24 | 2020-01-08 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a8bdfa040b74a14a.parquet` | 0.003 | 10 | 2020-02-06 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a9240acaa07f5926.parquet` | 0.815 | 106,463 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a94caf665b49bb6e.parquet` | 0.025 | 2,774 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a9c30522044e10c9.parquet` | 0.095 | 12,115 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/a9da618ddbe9aa1d.parquet` | 0.229 | 31,577 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/aa5fcb018725e6cb.parquet` | 0.645 | 92,040 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/aa6494c5d7763300.parquet` | 0.024 | 2,422 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/aa7c285ed7222b97.parquet` | 0.003 | 18 | 2020-03-29 – 2020-07-17 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/adc493d9a295670b.parquet` | 0.003 | 16 | 2020-03-03 – 2020-07-03 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/ae4ac76726e9e2ae.parquet` | 0.633 | 89,622 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/aebc3e0b2346489f.parquet` | 0.003 | 17 | 2020-01-05 – 2020-09-10 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/b168d90d2d0f51db.parquet` | 0.077 | 9,573 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/b290f6ca21f9d2de.parquet` | 0.016 | 1,570 | 2020-01-04 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/b333e9e8c08cb1c0.parquet` | 0.003 | 17 | 2020-01-04 – 2020-12-24 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/b405238c8cb8b2fa.parquet` | 0.002 | 5 | 2020-02-19 – 2020-10-17 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/b4e33c3b8f0e483b.parquet` | 0.198 | 25,711 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/b6351f74a05ce905.parquet` | 0.337 | 46,500 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/b6f495f1951188a5.parquet` | 0.003 | 9 | 2020-02-07 – 2020-07-21 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/b7ece38dd8588c83.parquet` | 0.013 | 1,165 | 2020-01-03 – 2020-12-16 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/b963bf1bfe719507.parquet` | 0.046 | 5,730 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/b981e18d0ce3850d.parquet` | 0.007 | 436 | 2020-02-04 – 2020-11-14 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/bc38c6bd03b3de15.parquet` | 0.050 | 5,803 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/bfa559830f07c430.parquet` | 0.072 | 9,229 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/bfde9f7e3407a9ff.parquet` | 0.019 | 2,165 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/c20e90a5eb8327df.parquet` | 0.004 | 156 | 2020-01-11 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/c2ea60cd89fa16b6.parquet` | 0.127 | 15,995 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/c2f462aede0db716.parquet` | 0.002 | 6 | 2020-05-24 – 2020-11-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/c36d45f6f34a94dc.parquet` | 0.068 | 7,578 | 2020-01-02 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/c696e791ab6bfe65.parquet` | 0.141 | 19,962 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/ccc4a9fb744d16fb.parquet` | 0.003 | 29 | 2020-01-24 – 2020-05-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/cd171e0d9481b4ff.parquet` | 0.535 | 76,861 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/cd4e06298bb57aeb.parquet` | 0.011 | 989 | 2020-01-03 – 2020-12-27 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/cda2a6d86304b5d5.parquet` | 0.006 | 462 | 2020-01-06 – 2020-12-18 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/cdcb8a09a58a2390.parquet` | 0.364 | 52,627 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/cdd8846bc0964c01.parquet` | 0.329 | 46,800 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/ce792e6f11d7282d.parquet` | 0.247 | 34,307 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/d06f55139ee77bbd.parquet` | 0.027 | 2,905 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/d0fcb98acca8d24a.parquet` | 0.645 | 96,022 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/d148279b9aaf41b4.parquet` | 0.005 | 253 | 2020-01-06 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/d3107eda0cc04959.parquet` | 0.024 | 2,284 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/d38d9273dab3052f.parquet` | 0.026 | 3,100 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/d3b06ed40a80d3e7.parquet` | 0.112 | 15,690 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/d5b8e4553b5a751e.parquet` | 0.006 | 399 | 2020-01-02 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/d6d66b774d6a108b.parquet` | 0.008 | 655 | 2020-01-02 – 2020-12-06 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/d79eff0d23d8fc31.parquet` | 0.009 | 740 | 2020-01-01 – 2020-12-16 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/d88ef2acaba124a0.parquet` | 0.008 | 562 | 2020-01-04 – 2020-12-23 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/d8d8e23891d48133.parquet` | 0.034 | 3,910 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/daf19d921613b10b.parquet` | 0.021 | 2,222 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/dafe79568bb2b3f4.parquet` | 0.003 | 18 | 2020-03-21 – 2020-09-25 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/ddbec55836224ac7.parquet` | 0.019 | 1,873 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/dec259b5163a7a9b.parquet` | 0.024 | 2,618 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/ded070d7328ac5c6.parquet` | 0.002 | 3 | 2020-09-09 – 2020-09-10 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/e05c84b8a9b36c63.parquet` | 0.007 | 518 | 2020-01-02 – 2020-12-13 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/e05d5a58862bbe99.parquet` | 0.007 | 546 | 2020-01-01 – 2020-12-25 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/e0b9642bb0f4e9f2.parquet` | 0.011 | 1,046 | 2020-01-02 – 2020-12-06 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/e36e7542cf6c7225.parquet` | 0.006 | 339 | 2020-01-06 – 2020-12-19 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/e4b3f0c87280b1c1.parquet` | 0.085 | 10,897 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/e62345c49f3066e9.parquet` | 0.009 | 777 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/e6d5afb3b905dcb0.parquet` | 0.003 | 23 | 2020-01-03 – 2020-08-20 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/e865c3b9fb2607d8.parquet` | 0.005 | 231 | 2020-01-17 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/e936344cab2675b7.parquet` | 0.025 | 2,694 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/e97e7129816f75f7.parquet` | 0.304 | 41,774 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/ea9f1a34eb0cf836.parquet` | 0.060 | 7,314 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/ead706c0e2541faa.parquet` | 0.171 | 21,768 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/eb9092e734276336.parquet` | 0.007 | 465 | 2020-02-02 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/eb995e9890ce0c6d.parquet` | 0.020 | 1,991 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/ed93b2c18a218549.parquet` | 0.131 | 18,571 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/ee32bf4af597b3bf.parquet` | 0.219 | 30,398 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/ee57fd97dbc21497.parquet` | 0.079 | 10,295 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/efd3477b7e87c281.parquet` | 0.004 | 67 | 2020-01-04 – 2020-12-08 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/efff0ade789adb46.parquet` | 0.003 | 14 | 2020-06-24 – 2020-10-09 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/f0283792712fb200.parquet` | 0.070 | 9,645 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/f041c8f510197923.parquet` | 0.002 | 6 | 2020-02-07 – 2020-11-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/f1000e18f530a1c1.parquet` | 0.003 | 9 | 2020-04-04 – 2020-10-15 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/f1591005685d2abb.parquet` | 0.119 | 15,328 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/f4513c44468f5a76.parquet` | 0.008 | 576 | 2020-01-02 – 2020-12-18 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/f46cab941c1e9436.parquet` | 0.011 | 935 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/f56e09877f0af891.parquet` | 0.004 | 155 | 2020-01-12 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/f6774f3e313fcee3.parquet` | 0.028 | 3,365 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/f74a61ad35a9b566.parquet` | 0.057 | 7,503 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/f9039dc2ad91d6e1.parquet` | 0.002 | 1 | 2020-03-10 – 2020-03-10 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/fa56bcc9e884164a.parquet` | 0.623 | 89,726 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/fa9f30d52587dc21.parquet` | 0.003 | 25 | 2020-01-05 – 2020-12-16 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_NOAA20_SP/fb8856e1bc5b3f88.parquet` | 0.640 | 86,904 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0091bee275e46dcb.parquet` | 0.964 | 136,399 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0379a9bbe3303dd9.parquet` | 0.003 | 11 | 2020-01-04 – 2020-11-14 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/03ce01a94743a566.parquet` | 0.023 | 2,408 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/03e80bff703076c3.parquet` | 0.112 | 15,516 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/05612e05d709f029.parquet` | 0.051 | 6,807 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/05cd1e63b7da41dd.parquet` | 0.020 | 1,969 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/06492aeaeb054535.parquet` | 0.006 | 357 | 2020-01-02 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/073e31b4d0eeb864.parquet` | 2.038 | 264,165 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0774da1d7e1537c4.parquet` | 0.002 | 4 | 2020-01-17 – 2020-08-15 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/087ce274983119de.parquet` | 0.002 | 2 | 2020-10-10 – 2020-12-16 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/08c3ad5a18a1a8e5.parquet` | 0.326 | 46,004 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0962e9094bf8c680.parquet` | 0.007 | 551 | 2020-01-02 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0a6a801b30631449.parquet` | 0.314 | 44,901 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0b189c1272011478.parquet` | 0.003 | 21 | 2020-01-23 – 2020-09-25 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0bb1c7354d07381c.parquet` | 0.006 | 323 | 2020-01-02 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0bb70bdb5b120920.parquet` | 0.003 | 7 | 2020-01-18 – 2020-04-05 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0bf0215ee915fa6a.parquet` | 0.002 | 2 | 2020-03-19 – 2020-07-06 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0da19c9f71b20aec.parquet` | 0.078 | 9,726 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0db6228718fe7be0.parquet` | 0.006 | 398 | 2020-01-25 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/0f0c0ec227ab4898.parquet` | 0.076 | 9,369 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/10bc787069cd0b6a.parquet` | 0.013 | 1,220 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/11553a074f282e66.parquet` | 0.321 | 45,898 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/11a06f0d0a683bd6.parquet` | 0.019 | 1,845 | 2020-01-01 – 2020-12-26 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/127b0930d07f539a.parquet` | 0.223 | 31,157 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/12b47586199400d5.parquet` | 0.002 | 5 | 2020-09-25 – 2020-11-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/157c1cd0229bb31a.parquet` | 0.195 | 28,029 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/17485e9d8f217950.parquet` | 0.004 | 125 | 2020-01-02 – 2020-12-23 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/18be3567844ca602.parquet` | 0.004 | 89 | 2020-02-10 – 2020-12-12 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/1b646aac521c45b1.parquet` | 0.026 | 3,034 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/1bb78ed8c285d95a.parquet` | 0.263 | 35,909 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/1bdc4053280045dc.parquet` | 0.015 | 1,509 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/1e843455790198ad.parquet` | 0.028 | 3,264 | 2020-01-04 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/1f56574a56144a97.parquet` | 0.023 | 2,229 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/1faff18494399751.parquet` | 0.009 | 700 | 2020-01-02 – 2020-12-22 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/218255f64d96cc79.parquet` | 0.003 | 25 | 2020-04-21 – 2020-08-17 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/2243deee6c5cf663.parquet` | 0.005 | 288 | 2020-01-15 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/23a1f48028306acc.parquet` | 0.049 | 5,648 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/267ce00b40effded.parquet` | 0.011 | 882 | 2020-01-08 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/26fbb8c01899f8cb.parquet` | 0.078 | 10,161 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/2a6c497ef414475b.parquet` | 0.006 | 402 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/2b7d933103d6be64.parquet` | 0.012 | 1,201 | 2020-01-01 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/2dc1e1b051a62620.parquet` | 0.021 | 2,169 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/2de1474478265ebd.parquet` | 0.007 | 510 | 2020-01-04 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/2e0d1d0745fcf588.parquet` | 0.003 | 44 | 2020-02-19 – 2020-10-02 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/2faba0f453632f35.parquet` | 0.009 | 718 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/3029a8a47606b7a1.parquet` | 0.283 | 39,593 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/315c9bda938e043e.parquet` | 0.004 | 82 | 2020-01-01 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/319f695f2f247d3c.parquet` | 0.085 | 11,962 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/32bed9ce7437a610.parquet` | 0.216 | 29,856 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/36ec054506fd44df.parquet` | 0.026 | 2,813 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/37f3d17bfdf940d5.parquet` | 0.228 | 31,299 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/395bc3de95e9d1aa.parquet` | 0.005 | 183 | 2020-01-08 – 2020-12-23 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/3a9d326e586938e5.parquet` | 0.002 | 1 | 2020-09-19 – 2020-09-19 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/4084ff4564963aa4.parquet` | 0.009 | 758 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/40aaf383dc4dcdad.parquet` | 0.014 | 1,279 | 2020-01-02 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/420d4f744a9a45d0.parquet` | 0.011 | 1,016 | 2020-01-03 – 2020-12-06 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/44df73b98bb23460.parquet` | 0.005 | 224 | 2020-01-06 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/4642842ea6496247.parquet` | 0.356 | 52,118 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/4668f57d1d383ceb.parquet` | 0.003 | 39 | 2020-01-21 – 2020-12-08 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/47fa50a015e950ae.parquet` | 0.003 | 11 | 2020-05-16 – 2020-09-10 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/4857ed182d9e01d6.parquet` | 0.113 | 16,690 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/496637cbd26d4848.parquet` | 0.036 | 3,541 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/4a58f073a3f18cad.parquet` | 0.077 | 9,917 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/4a61fee2b889e5a7.parquet` | 0.119 | 15,198 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/4aafe2c208c2efc2.parquet` | 0.084 | 10,671 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/50e3bbad65fcc6f1.parquet` | 0.071 | 10,021 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/520f3fe4d9e26290.parquet` | 0.375 | 60,235 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/53655503a61c6cff.parquet` | 0.024 | 2,550 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/5373e6f8b0185552.parquet` | 0.002 | 2 | 2020-02-08 – 2020-02-13 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/564149cc628e2e1d.parquet` | 0.320 | 49,001 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/582df5aa2f821f95.parquet` | 0.008 | 529 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/5b394793af8c0548.parquet` | 0.895 | 124,400 | 2020-01-01 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/5e38c2a82d3f7d44.parquet` | 0.003 | 23 | 2020-03-24 – 2020-11-08 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/5f4501f3e9ea3eb8.parquet` | 0.019 | 2,010 | 2020-01-01 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/5f6fbc301da1e9b2.parquet` | 0.002 | 1 | 2020-05-18 – 2020-05-18 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/5f906a659642c68f.parquet` | 0.040 | 4,812 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/5fc1f8effc4c357c.parquet` | 0.592 | 89,059 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/61c708e7c7fffa0d.parquet` | 0.626 | 88,583 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/62ac7947ced63ff8.parquet` | 0.029 | 3,392 | 2020-01-03 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/6349a9050f1294a8.parquet` | 0.003 | 18 | 2020-01-01 – 2020-09-21 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/63ecaa0c4e691417.parquet` | 0.002 | 2 | 2020-03-08 – 2020-08-20 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/6476f4551f3c8d51.parquet` | 0.263 | 36,696 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/64a2fe7482a37750.parquet` | 0.822 | 110,896 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/66149faaf5053d04.parquet` | 0.003 | 64 | 2020-01-04 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/662003e7eff32a4f.parquet` | 0.011 | 1,084 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/66603da7b019677b.parquet` | 0.002 | 9 | 2020-04-24 – 2020-10-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/6782b5583750825e.parquet` | 0.064 | 8,443 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/67986978764f9220.parquet` | 0.019 | 1,991 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/683824f742f4391d.parquet` | 0.004 | 65 | 2020-01-10 – 2020-12-26 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/68f30f1707721742.parquet` | 0.025 | 2,840 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/6a90141e33eeac7a.parquet` | 0.133 | 16,943 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/6ef2cdf17a5cf8f2.parquet` | 0.018 | 1,874 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/6f1a424746e82c5e.parquet` | 0.071 | 9,013 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/710604ccdf9e05f6.parquet` | 1.376 | 175,446 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/714f53b20646713d.parquet` | 0.003 | 25 | 2020-01-07 – 2020-10-24 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/71709148124fdd95.parquet` | 0.002 | 1 | 2020-10-01 – 2020-10-01 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/72b3eb62de0155e8.parquet` | 0.906 | 138,873 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/72b5f4bac625944a.parquet` | 0.067 | 8,220 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/72e7be4edc08a0f6.parquet` | 0.134 | 18,665 | 2020-01-01 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/733e8f3c0a85e81e.parquet` | 0.002 | 6 | 2020-03-11 – 2020-12-02 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/75f3ef1ad40f6ea6.parquet` | 0.007 | 574 | 2020-01-05 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/768e024e5d420ea3.parquet` | 0.070 | 10,543 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/769b9077e1e92452.parquet` | 0.015 | 1,390 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/76c91ca1b28c70d1.parquet` | 0.038 | 4,445 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/77285dcd80d03de5.parquet` | 0.002 | 1 | 2020-05-14 – 2020-05-14 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/783cf79b0207d096.parquet` | 0.003 | 8 | 2020-08-02 – 2020-10-09 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/7913112a1c492040.parquet` | 0.069 | 7,719 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/799a697edc259838.parquet` | 0.033 | 3,764 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/79b243f92e2dd956.parquet` | 0.004 | 153 | 2020-02-05 – 2020-10-26 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/7b469b1935479332.parquet` | 0.010 | 919 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/7e3d3873c6cfe21f.parquet` | 0.302 | 41,534 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/7f116a68c2cff6ea.parquet` | 0.008 | 680 | 2020-01-18 – 2020-12-21 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/8023c76843b48808.parquet` | 0.795 | 103,887 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/80a7ac2381d45d97.parquet` | 0.019 | 2,139 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/80c526a615f644bc.parquet` | 0.010 | 903 | 2020-01-02 – 2020-12-26 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/80c843450cafc851.parquet` | 0.009 | 703 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/81e2ae8cd377669d.parquet` | 0.003 | 9 | 2020-01-28 – 2020-08-13 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/824ef10e71396b93.parquet` | 0.128 | 18,143 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/8421ed2d021d6631.parquet` | 0.249 | 32,717 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/8491489ae5edd373.parquet` | 0.003 | 63 | 2020-01-04 – 2020-12-07 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/86667c93d4c0b976.parquet` | 0.011 | 938 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/893d85c864219f2d.parquet` | 0.013 | 1,123 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/8a8f14e93dec93a2.parquet` | 0.004 | 101 | 2020-01-03 – 2020-12-25 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/8de11ee793edf9da.parquet` | 0.004 | 124 | 2020-01-01 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/8df5a34d7a787189.parquet` | 0.010 | 890 | 2020-01-01 – 2020-12-27 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/8e1bc029f0a06177.parquet` | 0.232 | 31,679 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/8e44f7c36fe80851.parquet` | 0.019 | 1,888 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/8fb50e0af9406e8d.parquet` | 0.003 | 12 | 2020-02-13 – 2020-06-08 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/9064fed436486119.parquet` | 0.022 | 2,511 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/918e90089a86beef.parquet` | 0.016 | 1,531 | 2020-01-01 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/93dedf3d86b03354.parquet` | 0.006 | 396 | 2020-01-06 – 2020-11-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/9401622931c83614.parquet` | 0.008 | 494 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/94596077aadf8c96.parquet` | 0.007 | 539 | 2020-01-04 – 2020-12-25 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/96aa5081dbfac149.parquet` | 0.007 | 470 | 2020-01-01 – 2020-12-11 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/97be0e46c465fae8.parquet` | 0.004 | 177 | 2020-01-05 – 2020-12-27 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/9c7dec6c007959ca.parquet` | 0.009 | 685 | 2020-01-01 – 2020-12-15 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/9d5381a33de7ac3d.parquet` | 0.004 | 107 | 2020-03-21 – 2020-12-09 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/9ec84ac61aac835d.parquet` | 0.007 | 530 | 2020-01-01 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/9fb3e449d949f79a.parquet` | 0.010 | 879 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/a27b7dcbe4c19167.parquet` | 0.002 | 7 | 2020-05-24 – 2020-11-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/a2838516c1e090c2.parquet` | 0.036 | 4,174 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/a5019588975a3f6c.parquet` | 0.026 | 2,995 | 2020-01-04 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/a52999e34a5b2568.parquet` | 0.643 | 87,936 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/a7192ba1d3b15a16.parquet` | 0.056 | 7,292 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/a9300b5532f58e8c.parquet` | 0.112 | 15,405 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/a9626f9b7048216d.parquet` | 0.012 | 1,176 | 2020-01-03 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/aa45a1911f773297.parquet` | 0.025 | 2,775 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/acadde03530841f8.parquet` | 0.002 | 1 | 2020-05-29 – 2020-05-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/af33c4f4586e92e4.parquet` | 0.003 | 16 | 2020-02-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/af3bd4f277d798c4.parquet` | 0.016 | 1,469 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b0befb9be59116b6.parquet` | 0.605 | 87,077 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b207579eaedbe875.parquet` | 0.393 | 54,346 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b38ad765421fb1fa.parquet` | 0.339 | 46,633 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b3f3a47de44332df.parquet` | 0.007 | 434 | 2020-02-04 – 2020-11-25 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b439740bad7a0411.parquet` | 0.167 | 21,357 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b5180f66c3854362.parquet` | 0.094 | 11,854 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b53ca48edbb43418.parquet` | 0.003 | 13 | 2020-04-23 – 2020-12-02 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b6ce3460fcb248be.parquet` | 0.002 | 4 | 2020-08-29 – 2020-11-11 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b6fc54216abf93a0.parquet` | 0.132 | 19,410 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b79afe4367401c70.parquet` | 0.010 | 869 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b828202c5cfa8d34.parquet` | 0.006 | 458 | 2020-01-08 – 2020-12-15 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b940a1ffc909f3d1.parquet` | 0.527 | 75,465 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/b9969f741f284f9a.parquet` | 0.026 | 2,818 | 2020-01-03 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/bf90524c85c61f6d.parquet` | 0.629 | 93,816 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/bfde5a0de704ee7c.parquet` | 0.024 | 2,568 | 2020-01-01 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/c221d95d6436d537.parquet` | 0.002 | 8 | 2020-01-31 – 2020-12-11 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/c261e2e6f458d2a9.parquet` | 0.007 | 533 | 2020-03-08 – 2020-12-27 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/c6b0a4a73083eb7b.parquet` | 0.067 | 8,983 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/c6fdbe18a984e73c.parquet` | 0.002 | 6 | 2020-01-18 – 2020-12-19 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/c8535bed3960fe29.parquet` | 0.002 | 7 | 2020-06-08 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/c9bb63fcec96f726.parquet` | 0.003 | 24 | 2020-02-12 – 2020-07-06 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/cb8ef49ff1a0ad0c.parquet` | 0.292 | 40,149 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/ccd52312ab717141.parquet` | 0.024 | 2,743 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/ceecac5892aa341b.parquet` | 1.044 | 171,161 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/d00a5172c5701e45.parquet` | 0.005 | 216 | 2020-01-29 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/d108c71016fde3c5.parquet` | 2.518 | 345,517 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/d10cbf2a1bc26d35.parquet` | 0.003 | 5 | 2020-05-23 – 2020-10-15 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/d130afe8351e0325.parquet` | 0.032 | 3,878 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/d5b800c2dcdca91c.parquet` | 0.002 | 2 | 2020-09-09 – 2020-09-09 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/d803daf8d8a6cac3.parquet` | 0.003 | 24 | 2020-03-04 – 2020-06-13 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/d845365bb420cdfd.parquet` | 0.005 | 251 | 2020-01-01 – 2020-12-25 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/d8a18545fb0ca91a.parquet` | 0.004 | 83 | 2020-02-04 – 2020-11-02 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/d94a4957888ee65b.parquet` | 0.014 | 1,407 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/dc0f928acc40c83c.parquet` | 0.020 | 2,157 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/dc7bb4876e719ffd.parquet` | 0.081 | 11,258 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/dca9273270a607f3.parquet` | 0.044 | 5,438 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/de4c87854dcd99c5.parquet` | 0.003 | 8 | 2020-03-10 – 2020-12-10 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/e23cbfa0e6501f7a.parquet` | 0.196 | 25,303 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/e2859906552abebe.parquet` | 0.008 | 577 | 2020-01-10 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/e3e91285b3de47c5.parquet` | 0.011 | 917 | 2020-01-03 – 2020-12-26 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/e53a4cf6f17768bb.parquet` | 0.003 | 20 | 2020-01-11 – 2020-12-24 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/e5ba3220b2d7ef22.parquet` | 0.041 | 4,915 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/e68adfe19357db27.parquet` | 0.008 | 491 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/e7db887ee6a17033.parquet` | 0.011 | 1,057 | 2020-01-02 – 2020-12-22 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/e7efb33b05af3d5f.parquet` | 0.023 | 2,293 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/e7f0550ce7fc5e1e.parquet` | 0.003 | 23 | 2020-02-12 – 2020-12-22 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/e85b519a1bfd127d.parquet` | 0.123 | 15,156 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/e8986da5a5b9909b.parquet` | 0.174 | 23,387 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/eb54f1bf766bc888.parquet` | 0.540 | 76,644 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/ebec048ac63266c7.parquet` | 0.014 | 1,374 | 2020-01-21 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/eca64ac1deb18924.parquet` | 0.057 | 7,364 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/eda154e9bfbcebe6.parquet` | 0.050 | 5,780 | 2020-01-04 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/edb75f51d1ff3bfd.parquet` | 0.158 | 22,635 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/eeb45c599ff9d984.parquet` | 0.209 | 26,831 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/f1008ff6a105038f.parquet` | 0.003 | 20 | 2020-01-02 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/f1f513304b843125.parquet` | 0.632 | 90,136 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/f2c9eedef400ba18.parquet` | 0.110 | 15,259 | 2020-01-04 – 2020-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/f44300d2e489c03f.parquet` | 0.059 | 7,042 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/f5de05bdcce010cb.parquet` | 0.004 | 99 | 2020-01-06 – 2020-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/f8fd99e49ec04449.parquet` | 0.324 | 46,072 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/f90260fc25e2ecf7.parquet` | 1.196 | 158,245 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/fab005cc5ae4ad1b.parquet` | 0.094 | 15,204 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/fb1be5656e52dc8e.parquet` | 0.012 | 1,136 | 2020-01-07 – 2020-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/fc3619b6974d2a52.parquet` | 0.020 | 2,042 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/fc83ca7d1591619b.parquet` | 0.006 | 323 | 2020-01-01 – 2020-12-27 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/fe5dfbc22392beb5.parquet` | 0.006 | 333 | 2020-01-04 – 2020-12-19 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/febc23e685ca0b7c.parquet` | 0.634 | 85,929 | 2020-01-01 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2020/product_type=SP/product=VIIRS_SNPP_SP/fecf17bc2abddda2.parquet` | 0.009 | 698 | 2020-01-02 – 2020-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/025030d692a04b55.parquet` | 0.003 | 17 | 2021-02-10 – 2021-12-07 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/0a11188cd162da47.parquet` | 2.277 | 317,857 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/0dd5fde094c08c6c.parquet` | 0.007 | 414 | 2021-01-02 – 2021-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/0e0a463532022218.parquet` | 0.009 | 633 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/0f4dfd591a8b9304.parquet` | 0.409 | 57,625 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/1860c7e7bacc3c81.parquet` | 1.273 | 169,610 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/29e38cb70f6c7aab.parquet` | 0.018 | 1,755 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/2e36044590a4b2ba.parquet` | 0.003 | 26 | 2021-01-12 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/30c4d15dfb516962.parquet` | 0.281 | 32,594 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/38742b470a27b2c4.parquet` | 0.199 | 26,644 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/48e843a9623f1220.parquet` | 0.843 | 111,702 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/5662d6597901d3fc.parquet` | 0.003 | 26 | 2021-02-10 – 2021-12-02 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/58474de684ba0b84.parquet` | 0.108 | 15,007 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/59c8a7c646d9f271.parquet` | 0.002 | 1 | 2021-05-08 – 2021-05-08 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/6092dfd4748cb050.parquet` | 0.135 | 19,241 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/6b7f89f70f19387e.parquet` | 0.004 | 88 | 2021-01-06 – 2021-12-30 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/739ad76b311123f3.parquet` | 0.014 | 1,244 | 2021-01-01 – 2021-12-23 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/7a207da0c4def58a.parquet` | 0.092 | 10,275 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/7c955e66410b8d56.parquet` | 0.003 | 12 | 2021-01-11 – 2021-12-16 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/8cd09756c850d08b.parquet` | 0.018 | 1,816 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/af80aa2e4bba999d.parquet` | 0.302 | 42,491 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/b13ad417019b6018.parquet` | 0.006 | 326 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/b36259aa7b11f81b.parquet` | 0.029 | 3,199 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/c643b31d6b0d2070.parquet` | 0.003 | 23 | 2021-01-25 – 2021-10-08 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/cad821cd356f82a8.parquet` | 0.328 | 45,383 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/cb95fecd5531664d.parquet` | 0.021 | 2,172 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/d343cc2b56e9af2c.parquet` | 0.008 | 598 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/d5bfc47e1e589897.parquet` | 0.193 | 27,049 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/d88f976a437c4a04.parquet` | 0.017 | 1,695 | 2021-01-15 – 2021-12-27 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/e044696f32b68976.parquet` | 0.013 | 1,326 | 2021-01-01 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/e4aec0170d663705.parquet` | 0.015 | 1,416 | 2021-01-03 – 2021-12-31 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/e76a86f63a018526.parquet` | 0.010 | 802 | 2021-01-01 – 2021-12-28 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/eee3f835e1534f98.parquet` | 0.007 | 466 | 2021-01-09 – 2021-12-22 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/f7ed23079a1e5947.parquet` | 0.010 | 775 | 2021-01-28 – 2021-12-29 |
| `data/processed/cell_shards/sensor_family=VIIRS/year=2021/product_type=SP/product=VIIRS_NOAA20_SP/fdfdeb22aa341eb6.parquet` | 0.005 | 204 | 2021-02-16 – 2021-12-04 |
| `data/processed/daily_cell.parquet` | 210.961 | 24,755,782 | 2023-01-01 – 2026-11-14 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/00222c9a915b29e0.parquet` | 0.004 | 1 | 2023-08-13 – 2023-08-13 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/0074aeb20b870b51.parquet` | 0.006 | 7 | 2023-01-24 – 2023-09-18 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/01ac37c06f5e421e.parquet` | 6.699 | 126,650 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/03767bae20dfbd20.parquet` | 0.146 | 2,310 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/03922cd6cb871100.parquet` | 0.023 | 263 | 2023-01-01 – 2023-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/04946e77fb5ed90f.parquet` | 0.032 | 405 | 2023-01-12 – 2023-12-22 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/0561b192a1eab5ea.parquet` | 2.876 | 52,156 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/05d79adfd87c113d.parquet` | 0.013 | 118 | 2023-03-05 – 2023-10-08 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/08fe1fc3daf0e19f.parquet` | 0.008 | 36 | 2023-03-20 – 2023-10-12 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/0b58ae606bb89f40.parquet` | 2.398 | 44,459 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/0c7e5e5dfd86e0eb.parquet` | 0.023 | 262 | 2023-01-04 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/0cb4fcfd4dd23b2a.parquet` | 0.034 | 472 | 2023-01-06 – 2023-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/0ce42d184500002e.parquet` | 0.030 | 363 | 2023-01-08 – 2023-12-17 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/0dce1042800393bf.parquet` | 0.228 | 3,688 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/0e76a65c50155007.parquet` | 0.900 | 16,473 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/0e9a6f6b2fbe050b.parquet` | 0.008 | 32 | 2023-02-07 – 2023-09-11 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/1125bdfaf0e62d08.parquet` | 0.007 | 17 | 2023-01-08 – 2023-10-04 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/11e7942578828973.parquet` | 0.024 | 284 | 2023-06-12 – 2023-12-26 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/12028bb8d1e10059.parquet` | 0.041 | 545 | 2023-01-02 – 2023-11-17 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/14d29d5a2bdf940e.parquet` | 0.017 | 176 | 2023-03-17 – 2023-12-09 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/19c9e86711ce3e2b.parquet` | 0.016 | 159 | 2023-01-01 – 2023-11-08 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/1abf0bb20405fdd2.parquet` | 0.019 | 203 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/1c0741a51d48df86.parquet` | 0.153 | 2,633 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/1de90f930cdcf793.parquet` | 0.034 | 419 | 2023-01-02 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/1fb807df7a7e4f58.parquet` | 1.287 | 23,868 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/23413fd9e092afb1.parquet` | 1.102 | 20,609 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/248217436e3ee262.parquet` | 0.022 | 251 | 2023-01-23 – 2023-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/281c690c44b20575.parquet` | 0.009 | 45 | 2023-01-17 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/28919f3b0c707645.parquet` | 0.009 | 48 | 2023-02-08 – 2023-11-11 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/2951db7c95c156a3.parquet` | 0.005 | 4 | 2023-06-28 – 2023-07-10 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/2a066979f520468a.parquet` | 0.057 | 840 | 2023-03-11 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/2aa0a0e02f7fbbef.parquet` | 12.119 | 220,343 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/2ad905afb885e9c5.parquet` | 0.280 | 4,888 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/2b4d62ec36ef7c0c.parquet` | 0.020 | 202 | 2023-01-09 – 2023-12-25 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/3206d73ec3bed6c3.parquet` | 1.901 | 34,891 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/34a2f66a36a6bad9.parquet` | 0.145 | 2,310 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/34f14fd4493d6f2c.parquet` | 0.392 | 6,808 | 2023-01-04 – 2023-12-23 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/3571932b19d45167.parquet` | 0.020 | 216 | 2023-01-18 – 2023-12-12 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/36d81c350dc6c456.parquet` | 0.040 | 544 | 2023-02-03 – 2023-12-20 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/3871917b2befc1c0.parquet` | 0.009 | 46 | 2023-04-21 – 2023-08-25 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/3a48c750d7b69057.parquet` | 0.094 | 1,421 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/3bbae504e75a9773.parquet` | 0.614 | 11,010 | 2023-01-01 – 2023-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/3bbfae2931cc5aaa.parquet` | 0.025 | 298 | 2023-01-04 – 2023-11-07 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/3bc768dab08d6d4e.parquet` | 5.223 | 95,249 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/40482ace6f7d8eac.parquet` | 0.006 | 8 | 2023-05-17 – 2023-10-03 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/412d1daf4a0a03dd.parquet` | 0.010 | 58 | 2023-02-24 – 2023-10-13 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/4281b3d0539c4996.parquet` | 0.006 | 9 | 2023-08-17 – 2023-11-27 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/4319928b4230d193.parquet` | 0.006 | 6 | 2023-03-18 – 2023-09-28 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/44a390c1e89590bf.parquet` | 0.005 | 2 | 2023-05-20 – 2023-06-17 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/44ecb7bc91fff3bb.parquet` | 0.112 | 1,861 | 2023-02-25 – 2023-11-19 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/45ac1fdb4cf80a1a.parquet` | 0.036 | 451 | 2023-01-10 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/4875b604fab12df3.parquet` | 0.213 | 3,460 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/49a6f2ca3d1d17c9.parquet` | 19.613 | 357,737 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/4a73ac25af23fd40.parquet` | 0.083 | 1,240 | 2023-01-03 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/4d76a9f2d1c67704.parquet` | 0.004 | 1 | 2023-02-27 – 2023-02-27 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/4e0cb1b5e48b350a.parquet` | 0.012 | 92 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/4f7d61a2006cb6bf.parquet` | 0.141 | 2,338 | 2023-01-02 – 2023-12-22 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/4fd7b9787d8cc897.parquet` | 3.078 | 57,803 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/5040ec7db4cdcadf.parquet` | 5.338 | 99,825 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/5057e9d749bc1ad6.parquet` | 0.220 | 3,701 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/512c39ce3c152144.parquet` | 1.747 | 32,121 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/52370600c5d5d08b.parquet` | 0.020 | 218 | 2023-01-17 – 2023-10-25 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/5292012653d7c1f1.parquet` | 23.944 | 453,749 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/53a118b022b0e786.parquet` | 1.131 | 20,791 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/54f1b8c22c0e7806.parquet` | 0.007 | 20 | 2023-02-21 – 2023-11-15 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/563870a828859dde.parquet` | 0.167 | 2,631 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/56b5a874125d929e.parquet` | 1.592 | 29,370 | 2023-01-04 – 2023-12-25 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/56d357856275cb6e.parquet` | 0.860 | 14,904 | 2023-01-03 – 2023-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/56ff289495ab5745.parquet` | 0.193 | 3,262 | 2023-01-04 – 2023-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/580c4b3dabfde958.parquet` | 0.007 | 28 | 2023-01-19 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/581404a36f34c2cb.parquet` | 0.009 | 43 | 2023-01-10 – 2023-11-21 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/5e719f68ef2bbe34.parquet` | 0.037 | 527 | 2023-06-17 – 2023-12-26 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/5e8a073d41fbabf6.parquet` | 0.010 | 54 | 2023-01-21 – 2023-12-26 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/5e8adcf443794b0e.parquet` | 0.155 | 2,513 | 2023-01-03 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/5fbbaed773ac85af.parquet` | 0.004 | 1 | 2023-06-26 – 2023-06-26 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/60db294bce92dc66.parquet` | 0.025 | 304 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/6119557d2370c16c.parquet` | 0.014 | 130 | 2023-01-13 – 2023-11-12 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/61f0ee0113d09e55.parquet` | 0.047 | 657 | 2023-01-03 – 2023-11-10 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/666bf8bf58ed9573.parquet` | 0.010 | 67 | 2023-04-29 – 2023-09-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/6673a80077fbb463.parquet` | 0.007 | 17 | 2023-01-08 – 2023-11-08 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/678d5cffd57e7415.parquet` | 0.032 | 393 | 2023-01-03 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/67d0a17cf0f677d7.parquet` | 0.014 | 127 | 2023-05-09 – 2023-10-13 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/6836fca0e50ab963.parquet` | 0.017 | 170 | 2023-02-21 – 2023-11-06 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/69fd0a1487462d05.parquet` | 0.041 | 554 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/6e275b2e2bc2734c.parquet` | 0.011 | 78 | 2023-01-23 – 2023-12-14 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/6e7334b27cdbb481.parquet` | 0.251 | 4,254 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/72add122fdb21099.parquet` | 0.021 | 235 | 2023-01-02 – 2023-12-07 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/7331f1e759680fa2.parquet` | 0.076 | 1,155 | 2023-01-04 – 2023-12-27 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/737940f33947726b.parquet` | 0.005 | 5 | 2023-05-02 – 2023-12-14 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/7431f9f35d6d79c3.parquet` | 18.851 | 356,343 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/7581219280b3ca0f.parquet` | 0.941 | 17,027 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/76f955e273b02cf2.parquet` | 0.004 | 1 | 2023-05-09 – 2023-05-09 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/778b8ce9e4595bb7.parquet` | 0.012 | 92 | 2023-01-01 – 2023-12-27 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/78379a2bdc7f2c16.parquet` | 0.016 | 151 | 2023-01-17 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/7935cd52c76d7d75.parquet` | 0.030 | 368 | 2023-01-14 – 2023-12-18 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/7941a622b09dbd4a.parquet` | 0.066 | 954 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/7980218e9db7e02c.parquet` | 0.006 | 14 | 2023-01-06 – 2023-04-16 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/7aa7cae818bb2d54.parquet` | 4.252 | 78,425 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/7d846307cb069bd0.parquet` | 0.410 | 7,340 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/7ec312b572defa8e.parquet` | 0.013 | 106 | 2023-01-14 – 2023-12-07 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/7fdd158b3c160b36.parquet` | 0.007 | 26 | 2023-02-08 – 2023-11-02 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/80690e2d049a76d1.parquet` | 7.065 | 134,306 | 2023-01-01 – 2023-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/80d710e871678a09.parquet` | 0.016 | 156 | 2023-01-20 – 2023-10-13 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/817be776eaf82396.parquet` | 0.004 | 1 | 2023-09-21 – 2023-09-21 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/8187c4556080b628.parquet` | 2.295 | 41,967 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/852a420e5847862c.parquet` | 0.004 | 1 | 2023-03-31 – 2023-03-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/88a5d8705631e819.parquet` | 8.497 | 159,640 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/89c8c7445c9856fb.parquet` | 0.062 | 898 | 2023-01-03 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/89e3e55dceec06b2.parquet` | 0.676 | 12,447 | 2023-01-02 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/8a242b95b7f0b620.parquet` | 21.417 | 395,733 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/8c792c5adefc41f5.parquet` | 0.410 | 7,330 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/8dc29693d1a72562.parquet` | 0.115 | 1,762 | 2023-01-01 – 2023-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/8e87027f08a99595.parquet` | 0.008 | 40 | 2023-04-10 – 2023-09-21 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/8f819c75522f4049.parquet` | 0.663 | 11,760 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/90f7c1d3cb7a61c2.parquet` | 0.008 | 33 | 2023-02-17 – 2023-05-08 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/9496ec23bc037c71.parquet` | 0.041 | 561 | 2023-01-06 – 2023-10-08 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/97d1633f3b2081e4.parquet` | 0.053 | 761 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/9c4905e1e9b906bd.parquet` | 0.014 | 127 | 2023-01-12 – 2023-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/9cc8ad803efd2b8f.parquet` | 0.005 | 3 | 2023-06-19 – 2023-09-07 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/9d1798330de72e2b.parquet` | 0.019 | 201 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/9da264704a543071.parquet` | 0.513 | 9,205 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/a065497bda6fe06f.parquet` | 0.323 | 5,307 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/a0d8f6a8ed219fb8.parquet` | 0.009 | 52 | 2023-02-13 – 2023-12-08 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/a499d02ee4c50bea.parquet` | 0.008 | 33 | 2023-04-25 – 2023-08-26 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/a49f89f0246c44ed.parquet` | 0.026 | 315 | 2023-01-01 – 2023-11-07 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/a61358c743149494.parquet` | 0.466 | 8,444 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/a7291a7ea0dfe49f.parquet` | 0.088 | 1,379 | 2023-02-01 – 2023-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/a72966617d91e296.parquet` | 0.070 | 1,039 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/a7c4997c4cc1cdae.parquet` | 0.006 | 8 | 2023-02-17 – 2023-11-03 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/aab2d3d3f24db2d2.parquet` | 0.006 | 15 | 2023-01-02 – 2023-12-07 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/acf3493988c53a5b.parquet` | 3.857 | 73,528 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/b0c10540f732b96e.parquet` | 0.057 | 832 | 2023-01-10 – 2023-11-08 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/b56b8386b9a9f2f1.parquet` | 0.005 | 2 | 2023-03-08 – 2023-10-14 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/b67d19b4a73ee5b4.parquet` | 0.234 | 3,877 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/b8533cdb9538ab5a.parquet` | 0.071 | 1,062 | 2023-01-02 – 2023-12-26 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/b94a6e0136439a7f.parquet` | 0.136 | 2,177 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/ba5f922c0854aa88.parquet` | 0.117 | 1,912 | 2023-01-02 – 2023-12-18 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/bbf837357f6c30a5.parquet` | 0.019 | 218 | 2023-01-01 – 2023-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/bc2cd71fe9752e7c.parquet` | 0.518 | 9,051 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/bd445a011036523a.parquet` | 5.266 | 94,000 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/bdb9145cb4f3f37a.parquet` | 0.019 | 213 | 2023-01-10 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/be1dae456266cc57.parquet` | 0.005 | 2 | 2023-06-08 – 2023-07-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/bfb298e49312f542.parquet` | 0.039 | 544 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/c21b1a7a3e8713ce.parquet` | 0.033 | 416 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/c245863250e83d17.parquet` | 0.025 | 289 | 2023-02-04 – 2023-11-10 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/c25998c0a85d65ff.parquet` | 2.155 | 39,551 | 2023-01-07 – 2023-12-24 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/c27e74ae573b1078.parquet` | 0.022 | 243 | 2023-02-23 – 2023-11-08 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/c29eb660241b520d.parquet` | 0.004 | 1 | 2023-04-11 – 2023-04-11 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/c409279c340eb881.parquet` | 3.199 | 60,428 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/c6fdcc1816c9b1e0.parquet` | 0.004 | 1 | 2023-11-25 – 2023-11-25 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/c7a009dd4babd1ea.parquet` | 3.602 | 66,739 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/c88e87057cb64132.parquet` | 0.778 | 13,908 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/c916aa42d42beda6.parquet` | 0.004 | 1 | 2023-02-17 – 2023-02-17 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/c9d0d7349aa888d6.parquet` | 10.124 | 191,327 | 2023-01-03 – 2023-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/cb18a32cef42ca17.parquet` | 0.176 | 2,802 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/cc4313836cb3a500.parquet` | 0.566 | 10,571 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/ccaae79e3d3a128c.parquet` | 1.338 | 25,863 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/cdb2c3d705e06ffc.parquet` | 17.513 | 324,003 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/cf501b6c049ae547.parquet` | 0.004 | 1 | 2023-07-03 – 2023-07-03 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/cfd063af9a9fac39.parquet` | 0.007 | 22 | 2023-01-06 – 2023-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d0400958248a03c9.parquet` | 3.253 | 60,620 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d169b78734d3555f.parquet` | 0.801 | 14,702 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d26cf5df74712657.parquet` | 0.007 | 18 | 2023-01-30 – 2023-12-22 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d377a699ec76a1b9.parquet` | 2.145 | 39,837 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d3a67ad64ac179da.parquet` | 0.044 | 605 | 2023-01-02 – 2023-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d3ab3fce511cb22f.parquet` | 0.007 | 17 | 2023-02-16 – 2023-12-18 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d3c0b9a91f0a47a2.parquet` | 1.822 | 34,643 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d4142ae054d317d0.parquet` | 3.603 | 67,683 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d73f371e3a40c39c.parquet` | 0.097 | 1,486 | 2023-01-02 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d8ef31ce361c1eea.parquet` | 0.093 | 1,437 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d91f8987d40769ae.parquet` | 0.574 | 10,449 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d9cf5f0505d43d9f.parquet` | 0.766 | 13,781 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/d9da1d0b8bbb08a6.parquet` | 1.822 | 35,038 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/da97f0f8363676f0.parquet` | 0.082 | 1,277 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/db2eabb9c2a24bbd.parquet` | 0.005 | 3 | 2023-05-14 – 2023-07-02 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/db949c681fe926c2.parquet` | 1.424 | 26,204 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/e09af31cecabe489.parquet` | 2.661 | 47,910 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/e22842f3c33fac80.parquet` | 0.882 | 15,893 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/e4436c7ea535a2d6.parquet` | 1.905 | 35,119 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/e5a5b296f8a2c625.parquet` | 0.009 | 45 | 2023-04-19 – 2023-12-27 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/e6b221dde0ba12c0.parquet` | 0.092 | 1,441 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/e7156e80fd48b1fe.parquet` | 0.013 | 98 | 2023-01-05 – 2023-11-17 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/e7905d04f40836b3.parquet` | 0.868 | 16,038 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/e7d91c2c785e9093.parquet` | 0.123 | 1,913 | 2023-01-03 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/ea7725b8fa801d32.parquet` | 3.331 | 62,363 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/ed2e6b02775111a8.parquet` | 0.054 | 782 | 2023-04-29 – 2023-11-19 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/ed93d68eabc731d8.parquet` | 0.351 | 5,767 | 2023-01-04 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/eeade66db6b67387.parquet` | 0.022 | 242 | 2023-02-13 – 2023-12-25 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f0261fdc7a9e9904.parquet` | 0.005 | 2 | 2023-08-13 – 2023-08-13 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f0eee63455b698c4.parquet` | 0.262 | 4,267 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f290a541f92ccc4e.parquet` | 0.025 | 282 | 2023-01-05 – 2023-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f380acedb8f57787.parquet` | 0.062 | 923 | 2023-01-03 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f4b7c482eafdf112.parquet` | 3.198 | 58,074 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f5455d4aefb0f510.parquet` | 1.262 | 22,771 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f70ebc2945b1f2e6.parquet` | 0.005 | 2 | 2023-03-12 – 2023-03-12 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f7ce215d1c62aa89.parquet` | 0.004 | 1 | 2023-08-01 – 2023-08-01 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f8144ccb2e117969.parquet` | 0.151 | 2,391 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f872b70fd5b1dee5.parquet` | 0.017 | 165 | 2023-02-25 – 2023-10-10 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f8ce1f8852f5ff83.parquet` | 4.122 | 74,676 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f924f28708a27e7c.parquet` | 0.058 | 838 | 2023-01-04 – 2023-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f949b51133a8a6c8.parquet` | 0.004 | 1 | 2023-05-15 – 2023-05-15 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f9507c0aca5a346b.parquet` | 2.280 | 42,962 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/f9ca8d566bbcc6a6.parquet` | 0.035 | 463 | 2023-01-02 – 2023-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/fceca05df167be16.parquet` | 0.346 | 6,088 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/fd88121d96cb61c3.parquet` | 0.127 | 2,011 | 2023-01-10 – 2023-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/fdcf846a69a3430b.parquet` | 0.005 | 4 | 2023-02-18 – 2023-11-17 |
| `data/processed/observations/sensor_family=MODIS/year=2023/product_type=SP/product=MODIS_SP/fe2c4c2a6316d7c6.parquet` | 0.123 | 2,023 | 2023-01-05 – 2023-12-06 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/00d0372fe989913a.parquet` | 13.899 | 255,336 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/0181c2d29f79f865.parquet` | 0.028 | 347 | 2025-01-12 – 2025-12-07 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/0279e37a04d285c8.parquet` | 4.434 | 83,118 | 2025-01-03 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/0481b9da2ed144e5.parquet` | 0.009 | 54 | 2025-01-10 – 2025-12-26 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/07d2d6fcee164eb9.parquet` | 0.076 | 1,158 | 2025-01-03 – 2025-12-23 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/0a7c1089dc37e784.parquet` | 0.006 | 13 | 2025-01-12 – 2025-10-16 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/0bdc777c5ca29425.parquet` | 0.066 | 1,004 | 2025-01-03 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/0beae9be942f70fb.parquet` | 0.402 | 6,737 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/0c654dd2aafaffb0.parquet` | 1.043 | 18,821 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/0cba9f2c6b800b6a.parquet` | 0.482 | 8,440 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/0cef32d9418b8f8c.parquet` | 1.796 | 34,408 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/0d34de5e262320c4.parquet` | 0.009 | 46 | 2025-01-02 – 2025-12-24 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/0e3c8f55a69b5dda.parquet` | 0.266 | 4,662 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/15c5f744fc09ad89.parquet` | 0.027 | 323 | 2025-02-06 – 2025-12-15 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/15d3c7083f0a0ab4.parquet` | 1.292 | 23,937 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/16ec714914615651.parquet` | 0.005 | 6 | 2025-01-04 – 2025-11-10 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/1be05e3fda587a90.parquet` | 0.018 | 190 | 2025-01-02 – 2025-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/1c6ff6564ea86d5e.parquet` | 0.004 | 1 | 2025-10-03 – 2025-10-03 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/1e45e76246ce9611.parquet` | 0.008 | 41 | 2025-03-08 – 2025-09-24 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/1e97fcfb71f3311d.parquet` | 0.034 | 437 | 2025-01-02 – 2025-12-27 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/202aa7bbf84847ab.parquet` | 0.013 | 107 | 2025-01-07 – 2025-12-17 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/21e23acd6eed10d7.parquet` | 3.291 | 61,348 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/24991d7c0743cbca.parquet` | 0.042 | 573 | 2025-01-31 – 2025-12-14 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/2583365e1f2ad315.parquet` | 0.004 | 1 | 2025-12-23 – 2025-12-23 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/25948df95aeaaaff.parquet` | 0.867 | 15,840 | 2025-01-07 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/275f6f9bfc0ad1a5.parquet` | 0.072 | 1,092 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/277de29b269c3177.parquet` | 0.369 | 6,407 | 2025-01-11 – 2025-12-14 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/28caa2e42e02d15d.parquet` | 2.654 | 48,121 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/29767129a90cc7ce.parquet` | 7.122 | 128,408 | 2025-01-02 – 2025-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/2a2462aadb340f83.parquet` | 0.023 | 272 | 2025-01-16 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/2b66b321d04b9e8d.parquet` | 0.026 | 304 | 2025-01-05 – 2025-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/2d6714b63fe2c966.parquet` | 0.073 | 1,107 | 2025-01-19 – 2025-12-22 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/2df4da69e5245c15.parquet` | 0.005 | 2 | 2025-06-05 – 2025-08-23 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/2ea6253ae3de583e.parquet` | 0.009 | 56 | 2025-01-12 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/30d49a226a6b2c93.parquet` | 0.209 | 3,516 | 2025-01-02 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/32a9c129357ffe2e.parquet` | 0.023 | 262 | 2025-02-11 – 2025-11-06 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/32ade6c0623549ac.parquet` | 2.826 | 51,787 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/335c49c6fc27cc13.parquet` | 0.857 | 15,512 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/347ea0945c8b13a8.parquet` | 0.018 | 184 | 2025-01-17 – 2025-11-11 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/36aef9f956c8daff.parquet` | 0.030 | 374 | 2025-02-10 – 2025-11-20 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/378fafb07c3a2eaf.parquet` | 0.286 | 4,649 | 2025-01-04 – 2025-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/387c760cd159ed7a.parquet` | 5.609 | 105,663 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/388591bf0f22670f.parquet` | 0.550 | 9,499 | 2025-01-02 – 2025-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/393b474f4bd8e782.parquet` | 0.005 | 1 | 2025-01-28 – 2025-01-28 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/3ae4371aaafe82ef.parquet` | 0.608 | 10,936 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/3b0237c9c40d38fb.parquet` | 0.014 | 130 | 2025-01-08 – 2025-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/3bb68910080770e9.parquet` | 0.006 | 13 | 2025-05-31 – 2025-10-01 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/3c293b2b3ef31b1a.parquet` | 0.012 | 90 | 2025-03-04 – 2025-10-17 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/3c7a27a71b81edda.parquet` | 0.039 | 524 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/3d5e4ef19bc9e07a.parquet` | 0.007 | 23 | 2025-05-26 – 2025-08-27 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/3edeb48d65ed4678.parquet` | 0.009 | 50 | 2025-02-08 – 2025-09-22 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/3ee75d20f7e0aeec.parquet` | 0.035 | 462 | 2025-01-18 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/3f3d4c03fab4ffa9.parquet` | 0.023 | 280 | 2025-01-11 – 2025-12-27 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/3f906e9954fe287c.parquet` | 0.006 | 7 | 2025-02-04 – 2025-12-08 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/4050b8443a881c21.parquet` | 1.678 | 30,618 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/4331c618dfb7c130.parquet` | 0.125 | 1,988 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/45f7830dd7b624ae.parquet` | 0.903 | 16,641 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/4667ccb07d037935.parquet` | 5.629 | 102,582 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/496a9e5a92b391be.parquet` | 0.464 | 8,621 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/4abcc564d3863fc7.parquet` | 1.107 | 20,788 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/4cbe172b1bb43eaf.parquet` | 0.005 | 3 | 2025-06-27 – 2025-08-16 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/4d7e3fd428e76e42.parquet` | 0.004 | 1 | 2025-02-17 – 2025-02-17 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/4de270aab36629e4.parquet` | 0.865 | 16,372 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/50e38e2c3cbb23ab.parquet` | 0.005 | 2 | 2025-07-22 – 2025-08-09 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/510a791483272301.parquet` | 6.151 | 109,845 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/52fc66d5423d192a.parquet` | 0.200 | 3,468 | 2025-01-04 – 2025-12-24 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/55967e17e922e0a9.parquet` | 8.150 | 153,134 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/55bc91d310a8e55a.parquet` | 0.050 | 709 | 2025-01-08 – 2025-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/55ccaaab0b150dcd.parquet` | 0.013 | 115 | 2025-01-14 – 2025-11-05 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/55f04f43d1942d57.parquet` | 0.172 | 2,924 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/582db1b41a4f231f.parquet` | 0.104 | 1,636 | 2025-02-26 – 2025-11-02 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/584d84172f97967d.parquet` | 2.626 | 49,459 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/59c901402506a2d0.parquet` | 2.235 | 42,120 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/5c5dfb6792684b30.parquet` | 0.044 | 612 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/5f4bf2b7fc4a3ae5.parquet` | 1.766 | 31,739 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/5f60a9a027903861.parquet` | 0.162 | 2,626 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/600f78e9de94b1da.parquet` | 0.017 | 163 | 2025-04-07 – 2025-10-09 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/6067ec6921274b71.parquet` | 0.105 | 1,708 | 2025-01-01 – 2025-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/61ab4f76ed710397.parquet` | 0.127 | 2,029 | 2025-01-02 – 2025-12-19 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/61e7df0548f44455.parquet` | 0.688 | 12,572 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/637fda03b1f34c19.parquet` | 0.004 | 1 | 2025-10-12 – 2025-10-12 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/653744009f3f6faa.parquet` | 0.005 | 2 | 2025-04-16 – 2025-06-07 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/65968b485f73a208.parquet` | 2.866 | 53,086 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/664c111f988cab4f.parquet` | 13.022 | 236,731 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/667c28400d0d4820.parquet` | 0.004 | 1 | 2025-11-19 – 2025-11-19 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/66f712d4c03b5d76.parquet` | 0.181 | 3,042 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/6922c40315809726.parquet` | 0.890 | 15,458 | 2025-01-14 – 2025-12-09 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/6a1c8e9bd9066856.parquet` | 0.008 | 31 | 2025-03-07 – 2025-09-15 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/6bb1c9fbab907612.parquet` | 0.035 | 458 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/6dfa44ae76ca1315.parquet` | 0.133 | 2,247 | 2025-01-04 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/6f64cc5bcc266e10.parquet` | 0.285 | 4,867 | 2025-01-01 – 2025-11-28 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/70ab2ce694c3fdff.parquet` | 0.048 | 684 | 2025-02-03 – 2025-12-25 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/70ab49d4e2c19346.parquet` | 0.823 | 14,816 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/7201198ac66e90d9.parquet` | 0.005 | 3 | 2025-02-26 – 2025-04-20 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/73735f0594ff95c3.parquet` | 0.006 | 13 | 2025-01-02 – 2025-11-22 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/75f02159688dcf50.parquet` | 0.435 | 7,863 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/7702833afa3ca3df.parquet` | 0.332 | 5,799 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/7756f33a741a6482.parquet` | 0.017 | 170 | 2025-01-27 – 2025-12-16 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/77dd50eed4fb9cb5.parquet` | 0.268 | 4,334 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/7c9bd96ae41894fe.parquet` | 0.005 | 4 | 2025-01-30 – 2025-11-20 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/827cd6829f262e63.parquet` | 2.167 | 40,924 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/8299da04b4924d43.parquet` | 0.050 | 747 | 2025-01-07 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/83c1408fa6c53ac5.parquet` | 8.485 | 156,313 | 2025-01-05 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/84e2154d329cd5e8.parquet` | 0.025 | 289 | 2025-01-05 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/857d7011b126c755.parquet` | 1.119 | 20,155 | 2025-01-01 – 2025-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/85ade3fb61f5243c.parquet` | 0.067 | 991 | 2025-02-08 – 2025-10-13 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/85f4bdd083cf5c0d.parquet` | 0.014 | 117 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/88f5b2ee627e56d8.parquet` | 0.124 | 1,924 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/8de6f39d93a45a75.parquet` | 0.043 | 614 | 2025-01-09 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/8e08c0fa40b12c1f.parquet` | 0.006 | 7 | 2025-01-11 – 2025-07-01 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/8e70fcc14fe91eb0.parquet` | 15.587 | 295,922 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/90aa19ffb7b892a0.parquet` | 9.794 | 186,254 | 2025-01-07 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/91fca5d086694f0f.parquet` | 0.017 | 171 | 2025-01-09 – 2025-11-13 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/92f144290d3106dc.parquet` | 0.005 | 5 | 2025-01-14 – 2025-10-01 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/93e59c11395b2e39.parquet` | 0.005 | 3 | 2025-05-01 – 2025-07-01 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/93f5005958b73e89.parquet` | 0.019 | 198 | 2025-01-24 – 2025-12-09 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/95e3eef5fdf35cb2.parquet` | 0.197 | 3,210 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/965b6ad596f185cd.parquet` | 0.008 | 41 | 2025-02-10 – 2025-10-13 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/9788c972eeac0c66.parquet` | 0.019 | 195 | 2025-01-19 – 2025-10-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/97d66d4996fc0b57.parquet` | 0.019 | 195 | 2025-01-16 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/97f564dc7a839623.parquet` | 0.017 | 163 | 2025-01-25 – 2025-12-15 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/9a33572bad3b370a.parquet` | 0.199 | 3,451 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/9c797b93971196fd.parquet` | 0.036 | 467 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/9d5ad184441891b0.parquet` | 0.703 | 12,691 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/9d7a907dd7751d99.parquet` | 6.733 | 128,583 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/9d7c0640509651ca.parquet` | 0.418 | 7,060 | 2025-01-06 – 2025-12-24 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/a13f3029cc9b16ab.parquet` | 0.005 | 4 | 2025-04-13 – 2025-04-28 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/a23befa1ef56788b.parquet` | 0.336 | 5,696 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/a46d02932e1eacec.parquet` | 0.010 | 68 | 2025-01-07 – 2025-12-23 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/a4cfd3b6cc7cd7c7.parquet` | 0.004 | 1 | 2025-08-07 – 2025-08-07 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/a53d14fc8eefcfad.parquet` | 0.046 | 649 | 2025-02-10 – 2025-12-14 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/a54ee2e639aba571.parquet` | 0.024 | 272 | 2025-01-02 – 2025-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/a5d26dd3dc2a5278.parquet` | 0.063 | 936 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/a6521e70d96e7e52.parquet` | 2.551 | 47,189 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/a66a6859bb8eb8c0.parquet` | 0.060 | 865 | 2025-01-09 – 2025-11-06 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/a7d473990a68d7b1.parquet` | 5.124 | 94,917 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/aafa1f1e9fd96f1c.parquet` | 0.030 | 382 | 2025-02-21 – 2025-11-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/abc0978703fa95d2.parquet` | 0.308 | 5,123 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/ac74a09f2e72f239.parquet` | 0.005 | 4 | 2025-06-03 – 2025-12-19 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/ae52e7f99a7746a0.parquet` | 21.328 | 403,442 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/aebc19cae497326c.parquet` | 0.041 | 567 | 2025-02-02 – 2025-12-13 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/af0b6771a3b914bb.parquet` | 1.901 | 35,068 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/af2187bf9d18a30d.parquet` | 0.006 | 11 | 2025-01-11 – 2025-11-28 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/b141bcdf3aa3f0cc.parquet` | 0.027 | 335 | 2025-01-05 – 2025-12-16 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/b2438e73f3f534b6.parquet` | 0.006 | 13 | 2025-03-25 – 2025-11-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/b27ab0fdd57d2405.parquet` | 0.012 | 91 | 2025-02-26 – 2025-11-23 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/b8e2e7fcd9dd9833.parquet` | 0.008 | 30 | 2025-03-29 – 2025-10-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/b9fc2e4dcc5c0e24.parquet` | 0.073 | 1,091 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/bb1cdebe544273cd.parquet` | 0.006 | 8 | 2025-01-27 – 2025-10-07 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/bfa9b3b8f9475401.parquet` | 0.017 | 175 | 2025-05-14 – 2025-08-18 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/c0a1298ecae2a91b.parquet` | 0.005 | 2 | 2025-06-09 – 2025-06-14 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/c3acfc214475446a.parquet` | 0.069 | 1,042 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/c6688846570ccfe6.parquet` | 0.015 | 135 | 2025-01-09 – 2025-12-26 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/c6f190564b44cf70.parquet` | 1.482 | 28,092 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/c6fb45c117ca4474.parquet` | 0.063 | 916 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/c7df10cc6cc9935d.parquet` | 0.188 | 3,093 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/c9fbbdb02955d99e.parquet` | 0.005 | 3 | 2025-04-10 – 2025-04-13 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/ca660ab0fcafc5ce.parquet` | 0.011 | 73 | 2025-02-12 – 2025-09-26 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/ca662da492b1431a.parquet` | 0.803 | 14,610 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/cb75421b45d5a509.parquet` | 1.014 | 17,847 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/cb7d961f4fc446a6.parquet` | 0.096 | 1,438 | 2025-01-06 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/cb93c6c428836de4.parquet` | 0.004 | 1 | 2025-01-29 – 2025-01-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/cf9ac2fa0297b9da.parquet` | 0.022 | 251 | 2025-01-23 – 2025-12-28 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/d121ff332e3908a9.parquet` | 0.016 | 146 | 2025-01-24 – 2025-11-27 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/d177a5f68f1b4038.parquet` | 0.158 | 2,603 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/d346fedd19b94f32.parquet` | 0.012 | 94 | 2025-01-17 – 2025-09-12 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/d3dcd145e1805224.parquet` | 2.633 | 49,280 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/d5e96a420d8d6952.parquet` | 0.538 | 9,461 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/d68e1d429a9f48d9.parquet` | 3.601 | 64,966 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/d793c5c938e3bc16.parquet` | 2.091 | 38,847 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/d80ba9bd5b051bcb.parquet` | 0.050 | 727 | 2025-01-13 – 2025-12-20 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/d918899cc9bc18e2.parquet` | 0.397 | 6,665 | 2025-01-08 – 2025-12-29 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/d969aba6f4472ce8.parquet` | 1.517 | 28,270 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/da25f27a62566f14.parquet` | 0.097 | 1,512 | 2025-01-11 – 2025-11-25 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/daf3494b7bc76fc1.parquet` | 2.043 | 37,623 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/dc8b4793f2d93d71.parquet` | 0.005 | 4 | 2025-02-24 – 2025-11-13 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/df5feac756815b3b.parquet` | 0.005 | 3 | 2025-05-23 – 2025-05-23 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/e0993fc50fa65a96.parquet` | 0.069 | 1,036 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/e1980b868799462d.parquet` | 0.027 | 342 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/e4fd291315a73681.parquet` | 0.040 | 548 | 2025-01-07 – 2025-10-18 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/e51d1757af271449.parquet` | 0.041 | 561 | 2025-01-04 – 2025-12-23 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/e524fb2e06bc651b.parquet` | 0.020 | 219 | 2025-01-31 – 2025-12-25 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/e584b41594bc33a1.parquet` | 0.959 | 17,125 | 2025-01-02 – 2025-12-25 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/e71ed6eacf4778a3.parquet` | 0.022 | 245 | 2025-01-01 – 2025-12-23 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/e8a8135649981c5e.parquet` | 0.311 | 5,076 | 2025-01-02 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/e9d89ba7b75d399c.parquet` | 0.078 | 1,188 | 2025-01-04 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/eb72821c320e7e4b.parquet` | 0.006 | 14 | 2025-02-25 – 2025-07-27 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/eda701fd06ce8753.parquet` | 0.106 | 1,617 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/f006b6d5302db2ac.parquet` | 0.016 | 151 | 2025-03-10 – 2025-10-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/f1bcc947123ba04c.parquet` | 0.077 | 1,208 | 2025-01-03 – 2025-11-23 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/f36753389a10bd0b.parquet` | 0.086 | 1,358 | 2025-01-14 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/f50856b555f4dcfe.parquet` | 0.160 | 2,655 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/f54cee7838d50ccb.parquet` | 0.859 | 15,865 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/f618b8dda9af1b74.parquet` | 0.005 | 6 | 2025-02-23 – 2025-11-01 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/f790284a97dae085.parquet` | 0.188 | 3,176 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/f7c43c539c1e2c5b.parquet` | 0.062 | 921 | 2025-01-04 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/f87bff742b46b89e.parquet` | 0.007 | 17 | 2025-07-20 – 2025-12-27 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/fc9f75afe1fe9595.parquet` | 0.012 | 93 | 2025-01-11 – 2025-11-13 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/fca6bc90a91bffb8.parquet` | 0.107 | 1,719 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/fd06e5ef176b86f6.parquet` | 0.065 | 944 | 2025-01-04 – 2025-12-30 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/fd17ca6cdf6aa845.parquet` | 0.013 | 118 | 2025-01-18 – 2025-11-26 |
| `data/processed/observations/sensor_family=MODIS/year=2025/product_type=SP/product=MODIS_SP/fdd9ee986eeea65a.parquet` | 0.203 | 3,258 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/0038ca911c20ab72.parquet` | 0.062 | 831 | 2023-01-07 – 2023-12-18 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/017ec82dd5f9c58f.parquet` | 0.203 | 3,030 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/01938d9fd863e667.parquet` | 0.181 | 2,710 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/01b039d05e39e816.parquet` | 0.298 | 4,520 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/040985966f696848.parquet` | 4.720 | 83,061 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/059b535f779955a4.parquet` | 36.574 | 651,235 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/05b5fa9d8285afcf.parquet` | 98.367 | 1,782,338 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/05d46f378ed52002.parquet` | 0.014 | 115 | 2023-01-08 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/06cfbb2468e0c5fe.parquet` | 0.052 | 677 | 2023-01-03 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/084ef54ab9fb3ca3.parquet` | 3.104 | 54,039 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/089c15bd1a396cfd.parquet` | 0.075 | 1,007 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/0920be35cb994ded.parquet` | 0.025 | 272 | 2023-01-04 – 2023-12-23 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/093485428202ed6c.parquet` | 0.038 | 475 | 2023-01-08 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/0b84fdbe0662cf24.parquet` | 33.707 | 591,145 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/0c6d2a764b2e4eb8.parquet` | 0.979 | 16,585 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/0d141825e60d43e8.parquet` | 2.792 | 49,445 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/0f816f3ca59d41bf.parquet` | 0.797 | 12,677 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/0f9f8a9f5ba348f2.parquet` | 0.007 | 22 | 2023-06-25 – 2023-09-14 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/10d2453bd4360074.parquet` | 0.005 | 1 | 2023-01-30 – 2023-01-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/159b18d180be7acf.parquet` | 3.379 | 58,742 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/16c0cf17803d39e6.parquet` | 0.066 | 945 | 2023-01-07 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/16cc5e6862846b9e.parquet` | 0.538 | 8,538 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/17403601435ce080.parquet` | 0.069 | 968 | 2023-01-02 – 2023-12-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/1d68675d72350c6f.parquet` | 0.005 | 4 | 2023-03-17 – 2023-05-02 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/1e3b0e9d06f7bc03.parquet` | 0.016 | 139 | 2023-01-18 – 2023-10-17 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/1e4395350b409706.parquet` | 0.080 | 1,114 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/1f2b8ebcf2f7e9ef.parquet` | 0.005 | 2 | 2023-03-05 – 2023-03-05 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/2163b8392f0567bf.parquet` | 0.013 | 90 | 2023-01-11 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/2167cefa41ef8e82.parquet` | 0.050 | 628 | 2023-01-02 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/2260bdc92dd428d1.parquet` | 31.623 | 560,862 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/2529e6acb9eaef61.parquet` | 0.085 | 1,184 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/25b7a54c55b963f9.parquet` | 0.059 | 788 | 2023-01-03 – 2023-12-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/269286600a9b84c5.parquet` | 2.295 | 38,959 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/293ba247c7d58190.parquet` | 1.914 | 33,504 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/2a156476bda23982.parquet` | 0.045 | 616 | 2023-01-03 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/2a9cae4539ea71ee.parquet` | 0.083 | 1,151 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/2acc7091861a5a48.parquet` | 0.071 | 952 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/2d7899fbd4ab2c53.parquet` | 0.088 | 1,232 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/3285f4df1900a742.parquet` | 0.169 | 2,567 | 2023-01-02 – 2023-11-09 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/3318256dddc121e4.parquet` | 0.007 | 16 | 2023-03-28 – 2023-10-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/331db55f078a726b.parquet` | 0.056 | 770 | 2023-01-03 – 2023-12-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/337fe7f7d84e3b00.parquet` | 0.498 | 8,253 | 2023-01-01 – 2023-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/38834592fdf58fea.parquet` | 1.458 | 24,560 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/38d6ce3b54086c17.parquet` | 0.007 | 19 | 2023-01-16 – 2023-06-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/3c3ca0c83d010bf3.parquet` | 5.986 | 105,777 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/3dfd1327b92164cd.parquet` | 4.780 | 85,723 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/3e461852e85b2c26.parquet` | 0.072 | 971 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/400ce79a0606a48d.parquet` | 0.817 | 13,262 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/41517399bf2f8cc0.parquet` | 11.034 | 193,777 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/415b440018d68b7e.parquet` | 0.005 | 1 | 2023-06-17 – 2023-06-17 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/432a9c56a29ba600.parquet` | 0.208 | 3,178 | 2023-01-01 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/4339cade9f648828.parquet` | 0.015 | 125 | 2023-01-20 – 2023-12-26 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/447800658d5b8ab9.parquet` | 0.005 | 1 | 2023-08-18 – 2023-08-18 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/45ce059b21a92cab.parquet` | 0.006 | 8 | 2023-03-12 – 2023-12-20 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/45f907e2022e709e.parquet` | 4.314 | 75,313 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/4709be92431d66f9.parquet` | 0.006 | 10 | 2023-04-22 – 2023-10-22 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/47e575ba29f69ecd.parquet` | 0.181 | 2,670 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/496c03d1573a0a66.parquet` | 0.456 | 7,267 | 2023-01-02 – 2023-12-20 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/4ab212f77168a855.parquet` | 1.887 | 32,607 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/4c82b68298eee5eb.parquet` | 0.007 | 12 | 2023-02-01 – 2023-09-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/4dd6194ed144fcf5.parquet` | 0.780 | 12,884 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/4e0ddb49a0250a26.parquet` | 0.061 | 807 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/4e9d4fa089fd02cc.parquet` | 0.142 | 2,148 | 2023-01-02 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/4ead39b4d7b12b32.parquet` | 0.077 | 1,048 | 2023-02-10 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/50b6b2683ca7aca9.parquet` | 7.397 | 131,262 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/5141a646b0381060.parquet` | 0.010 | 57 | 2023-01-24 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/51e6899129cbefa3.parquet` | 0.005 | 4 | 2023-04-15 – 2023-08-21 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/52dc53d4bc2b76c5.parquet` | 0.359 | 5,364 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/53a94992190cc2d0.parquet` | 14.246 | 254,644 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/547b279ea20db86e.parquet` | 0.006 | 9 | 2023-03-21 – 2023-10-26 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/56b0928742b421b2.parquet` | 0.006 | 9 | 2023-01-29 – 2023-12-16 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/573f24313570fc16.parquet` | 0.272 | 4,111 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/57805fe30d35232a.parquet` | 0.202 | 3,012 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/59b71b27277ea30f.parquet` | 0.709 | 11,906 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/5a6545d28ab74491.parquet` | 23.524 | 413,791 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/5abf70d5939cff1b.parquet` | 9.425 | 163,741 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/5b207c59f9eb81be.parquet` | 2.045 | 35,895 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/5c3da6bd8e4544cc.parquet` | 6.518 | 115,048 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/5d5233a45644d58a.parquet` | 0.014 | 115 | 2023-01-27 – 2023-12-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/5e3f2b8a76e9c787.parquet` | 0.055 | 743 | 2023-01-09 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/5e88d1aba57d6aa2.parquet` | 0.101 | 1,417 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/5f256612888a2f32.parquet` | 3.004 | 52,355 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/638ec770e5e62357.parquet` | 47.646 | 840,560 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/64a10e1a730c71ee.parquet` | 14.189 | 248,763 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/65d2bacf0f4af379.parquet` | 15.831 | 279,812 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/6602b246c6ec2f01.parquet` | 0.127 | 1,873 | 2023-01-02 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/667245b31d3fecb7.parquet` | 0.005 | 2 | 2023-07-25 – 2023-08-03 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/66b6116f36b4a3a8.parquet` | 10.652 | 190,945 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/68c62bee3b4f790c.parquet` | 101.999 | 1,804,078 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/6be56ae077b84937.parquet` | 0.851 | 13,501 | 2023-01-01 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/6c0e23a0c3a78dc0.parquet` | 0.014 | 109 | 2023-01-02 – 2023-12-01 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/6c1f1504d1ebc816.parquet` | 0.005 | 2 | 2023-02-03 – 2023-02-03 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/6c4c7c5fd9f637e6.parquet` | 0.007 | 18 | 2023-02-24 – 2023-09-16 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/6d7b3b63e685aea8.parquet` | 0.244 | 3,656 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/6eb42fb42ff3dd1b.parquet` | 10.646 | 187,052 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/6f8bd398c5171147.parquet` | 0.233 | 3,706 | 2023-01-03 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/70212fa9f622ef40.parquet` | 0.416 | 6,645 | 2023-01-10 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/710cc0cd60443bef.parquet` | 0.005 | 2 | 2023-05-20 – 2023-06-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/723251ddd5e16090.parquet` | 0.046 | 625 | 2023-01-01 – 2023-12-18 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/72963fa6849366a7.parquet` | 0.007 | 21 | 2023-03-05 – 2023-09-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/7371ff193d61ef26.parquet` | 1.642 | 28,757 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/75c8621ba58da62f.parquet` | 4.555 | 78,995 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/76d484f348165bd7.parquet` | 2.894 | 51,222 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/779b6d51707b5565.parquet` | 0.018 | 163 | 2023-03-17 – 2023-11-05 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/77dba2c6c0f0d787.parquet` | 11.350 | 200,797 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/7a63aca06aa70468.parquet` | 0.668 | 10,700 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/7d18805dc7503d52.parquet` | 0.078 | 1,073 | 2023-01-02 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/7dd3e604ddbefdd8.parquet` | 0.159 | 2,418 | 2023-01-30 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/7f0ae6410b99651a.parquet` | 0.011 | 66 | 2023-01-02 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/7f12a1cef8e8a52a.parquet` | 0.124 | 1,743 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/822a083533e2b0d6.parquet` | 0.249 | 3,786 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/83233d8127879207.parquet` | 0.214 | 3,156 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/8430d2d75e190f60.parquet` | 0.903 | 14,446 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/84d92c7e8188f4fe.parquet` | 2.003 | 35,148 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/85cbac5388411021.parquet` | 2.540 | 44,211 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/86eeabca81e54e45.parquet` | 0.066 | 920 | 2023-01-02 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/87baa450e92b055e.parquet` | 1.549 | 25,615 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/8821f165dc6ea8d9.parquet` | 0.005 | 1 | 2023-03-05 – 2023-03-05 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/882ba73f2bb3cbe0.parquet` | 0.057 | 774 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/88e9e26e929d23f0.parquet` | 0.640 | 10,648 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/89718633ed38351a.parquet` | 0.493 | 8,184 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/89ffe0b32d3841f4.parquet` | 0.005 | 3 | 2023-02-03 – 2023-02-09 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/8a0f1bc063574846.parquet` | 22.622 | 390,873 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/8a436b14a94b85be.parquet` | 42.715 | 760,968 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/8d287db8babba6c9.parquet` | 12.550 | 222,441 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/8d306f1d6847f257.parquet` | 0.006 | 6 | 2023-02-26 – 2023-07-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/8d47d7df18397101.parquet` | 0.020 | 203 | 2023-01-01 – 2023-12-26 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/8e5de9c4ee8ea110.parquet` | 0.062 | 906 | 2023-01-07 – 2023-12-10 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/8e765b26f30d8b2c.parquet` | 15.593 | 275,464 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/8fa6e7b93ea3f266.parquet` | 0.005 | 3 | 2023-03-19 – 2023-03-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/933de1c74f056af0.parquet` | 0.160 | 2,449 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/9418343a558a7b09.parquet` | 0.006 | 6 | 2023-01-04 – 2023-06-14 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/9468f70981559430.parquet` | 0.112 | 1,625 | 2023-01-04 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/9691d09a98ad666e.parquet` | 0.156 | 2,505 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/97d7410cf47d7ad5.parquet` | 19.249 | 340,586 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/99a0c530ff618823.parquet` | 2.152 | 37,874 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/99cbef09f8dd95be.parquet` | 0.010 | 61 | 2023-03-15 – 2023-11-17 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/9c6460211d17c5a8.parquet` | 3.602 | 63,772 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/9cffb4eb4f229421.parquet` | 9.773 | 172,762 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/9e230698fa67a284.parquet` | 0.382 | 5,938 | 2023-01-12 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/a06446755d82645a.parquet` | 0.021 | 220 | 2023-01-11 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/a2481060608a1f9f.parquet` | 77.528 | 1,372,737 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/a260a0cd4a60cd5c.parquet` | 0.005 | 4 | 2023-04-12 – 2023-05-09 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/a2663bab79bbead1.parquet` | 0.007 | 12 | 2023-02-19 – 2023-11-14 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/a28ccf92367778a8.parquet` | 0.037 | 432 | 2023-01-02 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/a50ac86fb7a5b3e5.parquet` | 0.387 | 6,071 | 2023-01-01 – 2023-12-23 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/a56937b3487724af.parquet` | 0.465 | 7,531 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/a58885cbcd69ee09.parquet` | 2.498 | 42,690 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/a68281d1838bbcb6.parquet` | 0.197 | 2,994 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/a78b5ffbf25a531d.parquet` | 3.821 | 68,161 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/acdec93c86d29094.parquet` | 0.035 | 432 | 2023-01-03 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/ad854c888cc02c20.parquet` | 0.007 | 21 | 2023-01-21 – 2023-09-09 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/adc090fd3590cb05.parquet` | 23.573 | 421,559 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/afa5246ab8c230a9.parquet` | 7.662 | 134,359 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/b12a1534ee84561c.parquet` | 6.868 | 122,958 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/b228d279c84bc354.parquet` | 0.135 | 2,108 | 2023-01-01 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/b4b2dffa5abf88c4.parquet` | 0.150 | 2,397 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/b50a17403ecd70b0.parquet` | 0.058 | 779 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/b742db376536ad50.parquet` | 0.232 | 3,515 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/b7c3a9d8f37a853d.parquet` | 0.194 | 2,846 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/b8595d783d19c01b.parquet` | 5.661 | 98,684 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/b9aef2f13f836716.parquet` | 0.921 | 15,216 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/bc8c1fc0b5d75a35.parquet` | 0.147 | 2,186 | 2023-03-09 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/bcfa4f7bc4a53b58.parquet` | 0.017 | 159 | 2023-01-21 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c017b9d476ace22b.parquet` | 0.056 | 838 | 2023-01-01 – 2023-11-12 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c052a126471e73e1.parquet` | 3.666 | 62,467 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c0b74ae6ebcfe193.parquet` | 0.640 | 11,227 | 2023-01-09 – 2023-12-17 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c2790173b3b83f77.parquet` | 3.144 | 54,421 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c2f8adb318d57cc3.parquet` | 0.006 | 8 | 2023-05-02 – 2023-12-10 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c4b88abdf525e0d0.parquet` | 0.205 | 3,019 | 2023-01-03 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c6b7eb6f984ffef5.parquet` | 0.005 | 2 | 2023-04-16 – 2023-04-16 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c765ac5cc813c077.parquet` | 0.006 | 8 | 2023-03-09 – 2023-11-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c8c2e105a7225be9.parquet` | 0.092 | 1,311 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c8cdd7365041f978.parquet` | 14.495 | 250,312 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c9407e9aace251ab.parquet` | 12.128 | 211,795 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/c9a661280abeb03e.parquet` | 0.006 | 6 | 2023-01-11 – 2023-12-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/ca79b73f7bffed03.parquet` | 0.005 | 1 | 2023-10-08 – 2023-10-08 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/cc388c03c5ef8638.parquet` | 25.617 | 444,367 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/ce22bbef687b1442.parquet` | 0.042 | 514 | 2023-01-03 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/cf9ddf4384f26cb9.parquet` | 2.858 | 50,400 | 2023-01-01 – 2023-12-26 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/cfd34cab02d9447b.parquet` | 2.359 | 39,847 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d0bfd5095bd1e300.parquet` | 12.382 | 218,527 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d0ff05c8f1fb1f40.parquet` | 0.467 | 7,596 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d2137191a2255aa5.parquet` | 0.006 | 6 | 2023-04-19 – 2023-06-09 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d2b2b3c1b0f97ebf.parquet` | 18.540 | 320,740 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d33fa9dab427711c.parquet` | 19.736 | 353,844 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d469e852f887a1c1.parquet` | 0.016 | 140 | 2023-01-11 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d4bf9c5e72b6dcd1.parquet` | 0.607 | 9,616 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d55855ec1bdfe8e9.parquet` | 5.016 | 88,440 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d5c264857f0bee0d.parquet` | 0.221 | 3,384 | 2023-01-03 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d6998c109044a3e4.parquet` | 0.163 | 2,521 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d70ee3ce5651efdb.parquet` | 0.005 | 2 | 2023-05-11 – 2023-05-11 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d716e72f0ab2b94b.parquet` | 0.041 | 510 | 2023-01-07 – 2023-12-10 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d71c028543a6d4d4.parquet` | 0.660 | 10,603 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d97473bbd3004379.parquet` | 5.259 | 92,096 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/d9bffee2d235ac92.parquet` | 0.007 | 13 | 2023-05-01 – 2023-10-26 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/dcbc353f45ef799c.parquet` | 75.223 | 1,312,648 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/dd49382443306626.parquet` | 1.352 | 22,779 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/df43ffc63beb0f40.parquet` | 0.005 | 1 | 2023-05-14 – 2023-05-14 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/dfc1f2f884019b4a.parquet` | 20.312 | 358,486 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/dff1b67c15164809.parquet` | 9.984 | 180,200 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/e20186be55c08cb7.parquet` | 4.436 | 76,684 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/e2c72ba2ab4fd5e9.parquet` | 0.551 | 8,600 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/e3749e135eb203a1.parquet` | 0.005 | 1 | 2023-01-08 – 2023-01-08 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/e4ccd4706e45f23b.parquet` | 0.402 | 6,344 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/e523708a7ee234dd.parquet` | 91.811 | 1,681,190 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/e61b7fcf9c40cbf2.parquet` | 0.919 | 15,328 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/e6b38c9489f1c64a.parquet` | 0.005 | 1 | 2023-03-24 – 2023-03-24 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/ec6228c0921e9ccf.parquet` | 0.199 | 3,016 | 2023-01-03 – 2023-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/f08a16794422f422.parquet` | 0.227 | 3,479 | 2023-01-15 – 2023-12-22 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/f0f2f8d4628bf925.parquet` | 0.015 | 129 | 2023-04-10 – 2023-11-20 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/f796fe11f6b00a4b.parquet` | 0.516 | 9,126 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/f840486c28e1eb87.parquet` | 49.641 | 881,084 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/f9386844f6e478b7.parquet` | 0.364 | 5,560 | 2023-01-01 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/fc3722f439237ddc.parquet` | 0.097 | 1,356 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/fc44496740d920b3.parquet` | 1.833 | 31,025 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/fca5ceccf25213cc.parquet` | 0.132 | 1,934 | 2023-01-01 – 2023-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/fdcf509d1c0dda9b.parquet` | 1.053 | 17,937 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA20_SP/ffb825dab0a1f708.parquet` | 0.633 | 10,322 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_NOAA21_SP/5cbd85edddfe6f59.parquet` | 1010.030 | 18,110,940 | 2023-03-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/0aaa7ff19aa40a37.parquet` | 0.006 | 12 | 2023-01-15 – 2023-12-03 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/0fe7807d623fc70f.parquet` | 0.070 | 1,014 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/15c57b9d8b53741b.parquet` | 0.106 | 1,500 | 2023-01-03 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/1ce9f9c33e948884.parquet` | 95.540 | 1,754,727 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/1ea84da327571710.parquet` | 12.487 | 220,903 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/1f81fd40476a4845.parquet` | 0.224 | 3,369 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/21f166ae85d9efe0.parquet` | 5.704 | 99,568 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/26312eee20d8631f.parquet` | 0.005 | 4 | 2023-03-30 – 2023-12-02 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/2926bfa76790f105.parquet` | 0.004 | 1 | 2023-06-01 – 2023-06-01 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/2b318950cca14c68.parquet` | 0.630 | 10,475 | 2023-01-02 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/3050290b85495b19.parquet` | 79.107 | 1,404,205 | 2023-01-03 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/3458bea814a285ce.parquet` | 10.076 | 182,532 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/36bab8f13757fdb6.parquet` | 0.007 | 15 | 2023-02-25 – 2023-07-01 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/3d63a9820e10d791.parquet` | 0.040 | 482 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/3f7a4e42dd74c99a.parquet` | 0.099 | 1,405 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/458d24cd12446b62.parquet` | 0.012 | 75 | 2023-01-19 – 2023-12-20 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/484f51f123a3532f.parquet` | 0.210 | 3,234 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/48d8039e6fadba65.parquet` | 0.148 | 2,235 | 2023-01-29 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/4c77520309cebc80.parquet` | 0.006 | 10 | 2023-03-01 – 2023-08-17 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/4c86da5ae237a62e.parquet` | 12.911 | 229,064 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/52dfda75f3169b0f.parquet` | 0.637 | 10,409 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/53ae5c395a46b740.parquet` | 9.850 | 171,695 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/546e28ec76c46ccf.parquet` | 0.029 | 338 | 2023-01-01 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/5abfb56882d6e9fa.parquet` | 2.987 | 52,178 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/620bb520df48d462.parquet` | 0.057 | 794 | 2023-01-14 – 2023-12-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/66570a1c96754582.parquet` | 103.695 | 1,836,008 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/66f1a6eec62e6cda.parquet` | 0.195 | 2,950 | 2023-01-03 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/67a5ed1f7a6f9065.parquet` | 0.062 | 928 | 2023-02-16 – 2023-10-24 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/67e6b717fcb3590d.parquet` | 0.053 | 696 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/6b08cc687933ab0b.parquet` | 102.112 | 1,855,272 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/6d0269b825426d82.parquet` | 0.186 | 2,799 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/6d66e3fcbc47e591.parquet` | 2.546 | 44,457 | 2023-01-01 – 2023-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/6e12f8324f76ef5b.parquet` | 0.617 | 9,831 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/6e413ae8001a72a6.parquet` | 0.067 | 891 | 2023-01-02 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/7075abf309938d3c.parquet` | 0.614 | 9,764 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/732a43e09bb607e2.parquet` | 0.504 | 8,326 | 2023-01-02 – 2023-12-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/76642427592489fb.83a016b2e34e487daeb7b9db763afe79.tmp.parquet` | 0.000 | ASSUMED/unavailable | ASSUMED/unavailable |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/7a9e3e4bc12a44f3.parquet` | 1.909 | 33,076 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/7bb506b708415b5b.parquet` | 0.007 | 15 | 2023-03-26 – 2023-11-14 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/7ce7fc80e402f598.parquet` | 0.091 | 1,289 | 2023-01-04 – 2023-12-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/7e101ddbb78c6949.parquet` | 6.774 | 121,297 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/841dc9ad9d4b3dba.parquet` | 0.154 | 2,295 | 2023-03-09 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/8685a563f3f769ed.parquet` | 0.005 | 2 | 2023-04-03 – 2023-09-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/87d6f317ab30ca0c.parquet` | 0.013 | 96 | 2023-01-07 – 2023-12-22 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/8a79c474e59faed6.parquet` | 0.006 | 7 | 2023-03-12 – 2023-12-01 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/8ccf29fa0bf562bb.parquet` | 24.660 | 429,027 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/93e83e221591d6c5.parquet` | 19.848 | 356,191 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/951b5e389e9b18df.parquet` | 5.384 | 94,780 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/9bc2beb142d76f0a.parquet` | 76.879 | 1,345,502 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/9cee367f54377c0a.parquet` | 0.008 | 28 | 2023-01-16 – 2023-02-23 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/9d939fda05979862.parquet` | 0.034 | 388 | 2023-01-07 – 2023-12-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/a4123c7e948b1b5f.parquet` | 0.169 | 2,565 | 2023-01-02 – 2023-12-23 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/ab27189a0e5b0748.parquet` | 0.007 | 15 | 2023-04-13 – 2023-10-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/abef274308b13ac9.parquet` | 3.084 | 54,947 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/aced92c42c478266.parquet` | 1.814 | 30,763 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/adabca8297ef98c7.parquet` | 0.007 | 12 | 2023-01-25 – 2023-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/ae992a28cbd5e4bb.parquet` | 0.012 | 93 | 2023-04-21 – 2023-11-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/b5f21dd19933f550.parquet` | 0.081 | 1,136 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/b78d60d94ab7ce6b.parquet` | 4.449 | 77,072 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/b8160613e9bdf5da.parquet` | 0.970 | 16,480 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/bb22ba62fc4d7516.parquet` | 0.237 | 3,819 | 2023-01-03 – 2023-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/bb4cda4c3cf53c64.parquet` | 0.701 | 11,700 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/c1fb3832535244b1.parquet` | 0.007 | 16 | 2023-03-08 – 2023-12-16 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/c5cbc088c506ed56.parquet` | 0.646 | 10,424 | 2023-01-01 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/cc5a3d61d98de95b.parquet` | 0.929 | 15,507 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/cc5dfafbb98fc3f8.parquet` | 0.079 | 1,095 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/d23843e4b3a7c1dc.parquet` | 0.074 | 1,019 | 2023-01-01 – 2023-12-26 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/d32316db7fcafa0e.parquet` | 0.011 | 77 | 2023-01-08 – 2023-11-19 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/d329a0f661efeb3e.parquet` | 0.063 | 864 | 2023-01-04 – 2023-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/d6689298d324e512.parquet` | 0.063 | 875 | 2023-01-03 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/dcfd4817c459c386.parquet` | 31.458 | 558,235 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/de11a857ede6b731.parquet` | 0.005 | 1 | 2023-11-04 – 2023-11-04 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/df912c67cf3e2f2d.parquet` | 0.149 | 2,261 | 2023-01-02 – 2023-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/e19822786a6913a6.parquet` | 0.005 | 3 | 2023-02-14 – 2023-03-18 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/ead47e3efc0f3e97.parquet` | 0.191 | 2,842 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/f2ebbade6b3125c5.parquet` | 9.744 | 172,399 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/f61321d67f5ff110.parquet` | 0.005 | 4 | 2023-04-17 – 2023-07-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/f8f66f7a5ceb66a2.parquet` | 4.583 | 80,670 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/fcccf523ef3c1352.parquet` | 0.158 | 2,531 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/fd27220ce2961e08.parquet` | 0.011 | 68 | 2023-03-25 – 2023-11-17 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/fe459f14e3c80c13.parquet` | 0.013 | 103 | 2023-01-30 – 2023-12-07 |
| `data/processed/observations/sensor_family=VIIRS/year=2023/product_type=SP/product=VIIRS_SNPP_SP/fe64e0de9cea43e5.parquet` | 11.579 | 204,834 | 2023-01-01 – 2023-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2024/product_type=SP/product=VIIRS_NOAA20_SP/685424c86bb26820.parquet` | 123.148 | 2,175,601 | 2024-01-01 – 2024-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/01d63fb888f28513.parquet` | 0.128 | 1,874 | 2025-01-06 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/032f7c5bbd9d9e35.parquet` | 3.981 | 68,869 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/03d3be2f57e71b6b.parquet` | 0.084 | 1,166 | 2025-01-09 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/06d84e03c1238403.parquet` | 0.006 | 10 | 2025-01-01 – 2025-08-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/0728e3ae6776388b.parquet` | 4.124 | 72,110 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/07f1eefca9cdc7bd.parquet` | 0.007 | 16 | 2025-03-04 – 2025-11-19 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/0a793300261bc54d.parquet` | 1.796 | 30,761 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/0c26eb9ef027ead5.parquet` | 0.158 | 2,392 | 2025-01-01 – 2025-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/0d4b91eddb7ad97a.parquet` | 3.132 | 53,646 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/0df349b4aac0c0dc.parquet` | 4.708 | 81,875 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/0f97c4df2ff53070.parquet` | 5.133 | 90,094 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/1082ed792bcf9a38.parquet` | 0.292 | 4,536 | 2025-01-03 – 2025-12-16 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/10bd6785e4855cae.parquet` | 1.597 | 26,916 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/1128793e1382d85f.parquet` | 1.962 | 33,975 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/15050a14ab9d986f.parquet` | 0.093 | 1,292 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/17bbf73ddfc6c610.parquet` | 0.495 | 7,793 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/18d7ec7f0a972d95.parquet` | 0.070 | 1,011 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/19bc6214e0d32ac1.parquet` | 1.424 | 24,651 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/1d55b4eef3cb025f.parquet` | 0.019 | 185 | 2025-02-23 – 2025-10-20 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/1d8e35159abfc9a8.parquet` | 1.129 | 18,905 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/2069f4d220c223a1.parquet` | 0.213 | 3,144 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/2085ea9b916e91c1.parquet` | 27.936 | 485,403 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/22ca2b1b2be07183.parquet` | 13.098 | 231,124 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/2378ad8b742d7080.parquet` | 12.556 | 220,086 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/24806d3f4791a39f.parquet` | 0.511 | 9,040 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/24929aca96c37298.parquet` | 0.267 | 3,897 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/26263cc4bb285c52.parquet` | 0.180 | 2,750 | 2025-01-04 – 2025-12-24 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/26eddb1ffac54470.parquet` | 6.672 | 117,919 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/26edff91a866dded.parquet` | 0.279 | 4,177 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/275b7089083de3e8.parquet` | 4.026 | 72,303 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/27abe32738c29f3a.parquet` | 0.073 | 1,012 | 2025-01-05 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/29fffde6fdcedf8b.parquet` | 0.006 | 5 | 2025-04-16 – 2025-07-01 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/2b08921233bd1abc.parquet` | 0.071 | 962 | 2025-01-04 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/2b16788b21539e9c.parquet` | 0.025 | 279 | 2025-01-04 – 2025-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/2c1c1072172f44f5.parquet` | 12.204 | 214,871 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/2cac73a372c5ac39.parquet` | 0.074 | 1,041 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/2f95583ca969fa34.parquet` | 0.248 | 3,729 | 2025-01-05 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/3213a88ad5149387.parquet` | 0.007 | 13 | 2025-02-08 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/32b260c64d1ad1bb.parquet` | 1.031 | 17,582 | 2025-01-04 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/3347cc6c1133ad9f.parquet` | 5.180 | 90,797 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/34ecfc1781a53e1c.parquet` | 2.806 | 49,492 | 2025-01-01 – 2025-12-24 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/351b0dc4a8e229e5.parquet` | 0.015 | 134 | 2025-01-12 – 2025-12-22 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/3543302faedb1088.parquet` | 0.024 | 269 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/365bb489901498e9.parquet` | 0.142 | 2,136 | 2025-01-25 – 2025-12-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/378ec32fb5e9b5de.parquet` | 1.110 | 18,828 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/38358f90be5012d8.parquet` | 0.561 | 9,142 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/386e13fe73b4401d.parquet` | 0.005 | 3 | 2025-02-11 – 2025-09-13 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/39933890d05a6bd0.parquet` | 1.789 | 31,355 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/3a805467c50b3dd5.parquet` | 0.008 | 28 | 2025-01-13 – 2025-10-21 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/3abad0d62a305397.parquet` | 0.088 | 1,243 | 2025-01-02 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/3cde920f6e3d2be5.parquet` | 0.006 | 5 | 2025-01-23 – 2025-09-18 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/3d1bb911fc2fd6bc.parquet` | 0.142 | 2,099 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/3ee788ab235d4e84.parquet` | 0.053 | 703 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/402d4d834cba4cdc.parquet` | 7.999 | 141,560 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/4053790ee4f42dce.parquet` | 0.147 | 2,226 | 2025-01-14 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/405aa5d2d97b5205.parquet` | 0.858 | 14,035 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/41a76b0f5f2d3d3c.parquet` | 10.345 | 181,394 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/422c41443ffa34b2.parquet` | 1.762 | 31,077 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/4771079f72ee8b44.parquet` | 42.065 | 749,438 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/4799f637ceee1dbd.parquet` | 0.350 | 5,451 | 2025-01-03 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/4ad0b21d128ef369.parquet` | 0.015 | 125 | 2025-01-01 – 2025-12-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/4b619b0b239b8bca.parquet` | 0.014 | 121 | 2025-04-09 – 2025-10-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/4c98bd6452e0cff8.parquet` | 3.683 | 63,228 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/4da2f632aa606a5b.parquet` | 1.179 | 19,955 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/4e56a0f844501d40.parquet` | 3.121 | 54,403 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/503e92465d71893c.parquet` | 0.020 | 205 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/50628979fea90aa6.parquet` | 0.522 | 8,550 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/5070a3a770d47200.parquet` | 48.670 | 860,439 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/5106a0b9679e6940.parquet` | 0.113 | 1,690 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/51f1643fc6c53bd0.parquet` | 3.309 | 57,552 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/53b88924c3d12373.parquet` | 8.422 | 146,839 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/54b790b43318ccd4.parquet` | 1.176 | 19,410 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/597b4d4186f21f00.parquet` | 0.030 | 343 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/5b8ab410d5192133.parquet` | 1.474 | 24,622 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/5d5492e33a60350d.parquet` | 0.665 | 10,599 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/5e7a61be4bd06994.parquet` | 0.013 | 102 | 2025-01-08 – 2025-11-24 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/5fdee7bedb47cdec.parquet` | 0.200 | 2,963 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/646f3328fe7d8cc8.parquet` | 5.256 | 91,254 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/66a98e5dae0104e9.parquet` | 0.410 | 6,352 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/679ad9c5f94bae1e.parquet` | 0.006 | 6 | 2025-07-29 – 2025-10-02 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/67c6db4e679e4d30.parquet` | 0.053 | 704 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/680f3e758a744b01.parquet` | 0.927 | 15,333 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/6902ee1c41af312b.parquet` | 0.054 | 737 | 2025-01-10 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/6925ce50be20ff84.parquet` | 0.602 | 10,163 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/698af50031c66da3.parquet` | 0.005 | 3 | 2025-04-02 – 2025-08-02 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/6e13f97180c91e53.parquet` | 0.143 | 2,093 | 2025-01-01 – 2025-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/6e6f3c38d8174c17.parquet` | 0.006 | 5 | 2025-02-21 – 2025-11-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/6ef69e04e424ddb5.parquet` | 6.083 | 107,648 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/70326b123e3afc27.parquet` | 0.043 | 583 | 2025-01-11 – 2025-12-19 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/70741a7bcc17152c.parquet` | 0.049 | 614 | 2025-01-10 – 2025-12-24 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/7501e8411cf95885.parquet` | 0.005 | 1 | 2025-03-09 – 2025-03-09 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/7523b202595e0f0b.parquet` | 110.066 | 1,950,010 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/7936900552963b1c.parquet` | 1.198 | 20,245 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/79d9df9bb626d7c6.parquet` | 0.005 | 3 | 2025-04-06 – 2025-07-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/7aa478183587bb21.parquet` | 13.971 | 247,143 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/7b458373c89dc512.parquet` | 0.021 | 223 | 2025-01-15 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/7c1a428929cba7a9.parquet` | 0.068 | 923 | 2025-01-02 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/7d965482d8242593.parquet` | 0.013 | 88 | 2025-01-05 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/7d979d09043b9b90.parquet` | 0.320 | 4,855 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/7eae2c2d8f3bdb11.parquet` | 0.005 | 2 | 2025-04-27 – 2025-05-02 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/7f7deb383a06060b.parquet` | 0.064 | 865 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/81ad85eafbe912b7.parquet` | 0.215 | 3,333 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/835f1a13adc023c7.parquet` | 12.726 | 224,606 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/84608642c75c7b9c.parquet` | 31.176 | 553,570 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/8cb3b1cc9c14315b.parquet` | 28.246 | 493,475 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/8cdc091e7de63b5a.parquet` | 0.581 | 9,429 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/8d289a104086cd39.parquet` | 0.005 | 2 | 2025-08-30 – 2025-11-25 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/8ede3ecaf49369ad.parquet` | 0.200 | 3,155 | 2025-01-02 – 2025-12-26 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/9042e45cbc6125b8.parquet` | 33.411 | 585,993 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/9090c384b56c8d33.parquet` | 0.830 | 13,428 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/914ef85ab57de37c.parquet` | 4.687 | 83,317 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/918f39bd104a0429.parquet` | 0.019 | 189 | 2025-01-04 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/920c6ea04550290f.parquet` | 0.044 | 551 | 2025-01-12 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/92aa044285fb5299.parquet` | 0.259 | 3,928 | 2025-01-03 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/94b21be10e95dce5.parquet` | 18.234 | 323,475 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/95558e745ed1d34a.parquet` | 0.181 | 2,902 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/961ceaa679945e6d.parquet` | 39.616 | 706,266 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/97cc40b39e8e998b.parquet` | 0.005 | 2 | 2025-05-12 – 2025-05-12 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/99afa4930d835c6f.parquet` | 0.229 | 3,544 | 2025-01-06 – 2025-12-24 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/9a8eb1246a625638.parquet` | 0.061 | 836 | 2025-01-02 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/9cac18f1c97e7855.parquet` | 0.054 | 687 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/9caf1f658c4d449f.parquet` | 8.355 | 148,693 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/9d4a64fe5526b566.parquet` | 1.732 | 29,493 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/a00b354e71a826ab.parquet` | 0.348 | 5,465 | 2025-01-10 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/a12a729988951016.parquet` | 0.270 | 4,007 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/a2657cf591fe1bb6.parquet` | 0.082 | 1,234 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/a33371fdbc0840db.parquet` | 4.139 | 72,058 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/a3419440c225ace2.parquet` | 16.054 | 281,781 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/a4113ebee472f5ce.parquet` | 0.006 | 10 | 2025-04-07 – 2025-05-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/a46a5beabc6d3108.parquet` | 15.746 | 272,810 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/a7150251c73a6cfd.parquet` | 0.587 | 9,382 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/a80005688168625a.parquet` | 2.555 | 44,513 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/a91ad3ca1590c451.parquet` | 0.226 | 3,410 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/a9e9c44bda220b43.parquet` | 12.087 | 213,611 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/aa0f055c1f71e2e9.parquet` | 0.083 | 1,131 | 2025-01-08 – 2025-11-03 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/af3b4dc84f13d979.parquet` | 0.294 | 4,762 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/af73d83a5b2845fd.parquet` | 0.469 | 7,670 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b14d963ee06d5e7e.parquet` | 0.154 | 2,176 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b16b31224f6b7a3c.parquet` | 69.144 | 1,247,851 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b2015b7b3d4cc18a.parquet` | 0.147 | 2,187 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b22a0c4d62fc8c89.parquet` | 16.788 | 300,399 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b29d5dec3241fc5b.parquet` | 0.131 | 2,029 | 2025-01-04 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b2e57e2ad354241e.parquet` | 0.804 | 13,862 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b33722fd533aac2c.parquet` | 0.010 | 49 | 2025-01-08 – 2025-11-08 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b4ec5de54e804198.parquet` | 8.066 | 141,860 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b6205425b9e280a4.parquet` | 0.007 | 14 | 2025-01-03 – 2025-10-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b65df1cea573589b.parquet` | 0.013 | 90 | 2025-03-09 – 2025-11-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b8d818d4cbb148d7.parquet` | 0.086 | 1,222 | 2025-01-06 – 2025-12-10 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/b931307a55ae562b.parquet` | 37.317 | 655,554 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/bac0eebd04b46467.parquet` | 24.251 | 426,032 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/bd4682b3020ebc59.parquet` | 0.152 | 2,253 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/bd7db6d0bc20fc9c.parquet` | 0.005 | 1 | 2025-03-20 – 2025-03-20 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/be4d567e24d9ca6f.parquet` | 0.297 | 4,585 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/bf3663113b3558a6.parquet` | 4.762 | 83,673 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/bf7e7934baa95b34.parquet` | 1.946 | 33,867 | 2025-01-04 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c042344db0de162a.parquet` | 9.779 | 170,323 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c12900112965fdde.parquet` | 0.044 | 558 | 2025-01-03 – 2025-12-26 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c1861553d8393721.parquet` | 0.006 | 5 | 2025-05-13 – 2025-10-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c1da74c88c36b40c.parquet` | 0.471 | 7,307 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c24c4c0c4a102c72.parquet` | 2.586 | 44,597 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c3cf3b043f3f7ebd.parquet` | 0.089 | 1,252 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c4db6f754067ec2b.parquet` | 0.273 | 4,066 | 2025-01-03 – 2025-12-24 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c4f87c241bfa23d4.parquet` | 0.210 | 3,136 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c5a4f103936fa9f2.parquet` | 0.007 | 21 | 2025-03-27 – 2025-08-16 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c5aa71e2b827d97b.parquet` | 0.159 | 2,426 | 2025-01-27 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c61e27045c046a9f.parquet` | 48.950 | 853,909 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c711556580de9536.parquet` | 0.014 | 111 | 2025-01-05 – 2025-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c7df55c6a9900028.parquet` | 6.106 | 108,968 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/c95a2de0e34615e6.parquet` | 0.008 | 25 | 2025-01-02 – 2025-10-03 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/ca53ca0e644f3b3f.parquet` | 0.006 | 5 | 2025-09-06 – 2025-09-06 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/cd8e4f9a572ec16a.parquet` | 0.311 | 4,814 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/cef88a5cf8f1a42d.parquet` | 0.789 | 13,110 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/cfb889ad79f90403.parquet` | 1.471 | 24,180 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/d0a09ead8bc228c6.parquet` | 0.005 | 2 | 2025-09-23 – 2025-10-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/d1a2a34d2189be94.parquet` | 0.013 | 99 | 2025-01-03 – 2025-12-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/d2fbea62e73d0be7.parquet` | 0.005 | 1 | 2025-01-25 – 2025-01-25 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/d3b21058dbe66c59.parquet` | 0.005 | 1 | 2025-05-02 – 2025-05-02 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/d500156cebb2ae95.parquet` | 0.087 | 1,229 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/d6119a8095b7b22f.parquet` | 0.007 | 22 | 2025-02-20 – 2025-12-17 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/d6150591a21b69fe.parquet` | 0.200 | 3,177 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/d87718597015ee3e.parquet` | 5.572 | 94,458 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/da7c1851b3ba2483.parquet` | 70.861 | 1,255,715 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/da84397fee1fcf23.parquet` | 0.039 | 491 | 2025-01-07 – 2025-12-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/ddeb2a85996f47a8.parquet` | 0.006 | 7 | 2025-10-28 – 2025-11-11 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/de5070952e2c81db.parquet` | 0.008 | 34 | 2025-05-01 – 2025-09-19 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/e22bb653c46909f4.parquet` | 0.027 | 313 | 2025-02-17 – 2025-11-02 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/e57e8154383e3824.parquet` | 0.362 | 5,542 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/e5fb8637d5bff6a2.parquet` | 2.392 | 40,408 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/e6738cb89d0fdd1e.parquet` | 27.179 | 480,973 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/e67f269df00d5fe5.parquet` | 0.114 | 1,720 | 2025-01-01 – 2025-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/e6b4d04e303041e9.parquet` | 1.501 | 25,195 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/e6bf9f22e828bfb1.parquet` | 0.007 | 23 | 2025-01-24 – 2025-02-02 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/e809964b92c38e6e.parquet` | 3.726 | 65,261 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/e8d7a1de5b44e1d7.parquet` | 1.596 | 27,948 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/ea4abfa150d72632.parquet` | 0.005 | 1 | 2025-02-25 – 2025-02-25 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/eaef83a8ccf25b73.parquet` | 0.086 | 1,175 | 2025-01-11 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/ebd566053a5cea82.parquet` | 0.513 | 8,494 | 2025-01-03 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/ec3747caf4359871.parquet` | 0.010 | 53 | 2025-01-04 – 2025-12-19 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/ee905ed2b7751039.parquet` | 2.622 | 45,140 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/ef7ce2d67175c23d.parquet` | 0.280 | 4,348 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/ef91a409e9264e39.parquet` | 5.721 | 100,967 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f2a0b434f0626977.parquet` | 0.137 | 2,032 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f2f7911f81579c90.parquet` | 50.629 | 925,148 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f3772e0085bdffb5.parquet` | 0.035 | 412 | 2025-01-13 – 2025-12-26 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f43e5b12e4a148cd.parquet` | 0.005 | 1 | 2025-08-30 – 2025-08-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f5ab682cdca9811e.parquet` | 0.009 | 43 | 2025-01-09 – 2025-05-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f5c096c54e118a80.parquet` | 0.092 | 1,319 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f5cb23aff3da91ca.parquet` | 1.187 | 20,212 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f6947a02778efe20.parquet` | 0.030 | 363 | 2025-01-10 – 2025-11-18 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f8ad33601aa6412e.parquet` | 0.215 | 3,132 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f90a10ae98b1cd69.parquet` | 0.006 | 5 | 2025-05-05 – 2025-12-25 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f9920cc1ec4c899a.parquet` | 0.458 | 7,435 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/f9b6f64cec3b96ee.parquet` | 0.006 | 8 | 2025-01-26 – 2025-08-21 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/fa098f7ef584892a.parquet` | 0.006 | 9 | 2025-02-27 – 2025-11-21 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/faa372658da4430c.parquet` | 0.006 | 5 | 2025-03-23 – 2025-11-21 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/fb78a8c4b93a3c2e.parquet` | 0.006 | 6 | 2025-02-14 – 2025-04-04 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA20_SP/ff308f4c22147856.parquet` | 0.661 | 10,503 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_NOAA21_SP/55e9ca96bf5a1b08.parquet` | 990.149 | 17,674,069 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/00711d1a9464c286.parquet` | 0.898 | 14,765 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/014f9f8341ddaf8c.parquet` | 0.019 | 201 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/0492a83084564205.parquet` | 0.202 | 3,017 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/066699cff0b13857.parquet` | 0.005 | 2 | 2025-01-01 – 2025-07-14 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/06bb92affbf91b8d.parquet` | 0.030 | 350 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/06dfc21706c9d1ee.parquet` | 0.028 | 324 | 2025-01-13 – 2025-11-07 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/0832fd05743a696b.parquet` | 5.340 | 93,817 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/09ec64a90bdf3f07.parquet` | 0.211 | 3,133 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/0a45d1e811601902.parquet` | 49.220 | 861,621 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/0aa90771510a29fa.parquet` | 17.917 | 318,413 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/0d0185b899288439.parquet` | 24.199 | 426,258 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/0f732d05c25427bd.parquet` | 0.005 | 1 | 2025-09-23 – 2025-09-23 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/0f8153847cb3d706.parquet` | 26.848 | 470,596 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/140c321f22ab5e91.parquet` | 0.011 | 65 | 2025-01-03 – 2025-12-13 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/1421e1b97564b10c.parquet` | 1.347 | 23,226 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/15edb756bd2eb718.parquet` | 4.706 | 83,798 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/1957a79dc9ad269e.parquet` | 8.336 | 145,670 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/1eb038fd9f0558fa.parquet` | 0.136 | 2,032 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/1eddbecf3349bbed.parquet` | 0.004 | 1 | 2025-05-28 – 2025-05-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/2113456685a14936.parquet` | 0.006 | 8 | 2025-04-13 – 2025-11-21 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/21d53d27cab37ec2.parquet` | 1.504 | 25,187 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/23e42f98b1eb322d.parquet` | 0.104 | 1,531 | 2025-02-06 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/2825682ba69a28d5.parquet` | 0.007 | 14 | 2025-02-25 – 2025-11-21 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/283450f45eaa8fc9.parquet` | 0.114 | 1,741 | 2025-01-19 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/28f0c0c1c4c7d67d.parquet` | 0.007 | 19 | 2025-01-24 – 2025-02-04 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/29275edac123b54d.parquet` | 0.006 | 11 | 2025-03-11 – 2025-07-11 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/2a92299b9669a40a.parquet` | 3.994 | 69,650 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/2b399819df4f3bf6.parquet` | 0.005 | 3 | 2025-01-29 – 2025-05-16 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/2b9113841fa7cda9.parquet` | 0.012 | 82 | 2025-02-19 – 2025-11-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/2ec03cc6b853ebb1.parquet` | 0.154 | 2,353 | 2025-01-09 – 2025-12-21 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/2fea1a1a3329f24c.parquet` | 0.789 | 13,600 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/2ff46cb57f0e9511.parquet` | 0.085 | 1,217 | 2025-01-03 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/313abf4f3d83b4a2.parquet` | 0.074 | 1,098 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/315c715b0968e987.parquet` | 3.753 | 65,853 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/319482bbb305fa2e.parquet` | 0.058 | 750 | 2025-01-02 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/33bfcae735228808.parquet` | 0.477 | 7,208 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/346fc3da6341588c.parquet` | 0.284 | 4,438 | 2025-01-15 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/354c5b71e23e720a.parquet` | 0.004 | 1 | 2025-06-17 – 2025-06-17 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/355907d23959e496.parquet` | 5.282 | 93,341 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/3567046b2a34590e.parquet` | 0.020 | 196 | 2025-02-09 – 2025-10-20 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/35e0e9d18942f8f4.parquet` | 0.016 | 142 | 2025-01-14 – 2025-12-16 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/360b34df8be511cd.parquet` | 0.007 | 22 | 2025-03-27 – 2025-08-16 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/36bb788c80b99e66.parquet` | 0.007 | 21 | 2025-01-13 – 2025-09-19 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/36c4586183921358.parquet` | 0.012 | 88 | 2025-01-04 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/374ebc5e3d2bcf88.parquet` | 31.197 | 554,222 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/39f8022d64cf8785.parquet` | 0.023 | 264 | 2025-01-10 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/3b165f03c5a72533.parquet` | 40.234 | 718,447 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/3b6c81e4b313c071.parquet` | 9.777 | 170,674 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/3bceadf6ba493712.parquet` | 0.050 | 663 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/3ddd7aa26ca1a93d.parquet` | 10.383 | 182,528 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/3f27ea51990199c4.parquet` | 14.181 | 251,388 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/40af5953adbd2200.parquet` | 48.612 | 862,158 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/4152c946959b2f8e.parquet` | 1.420 | 23,349 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/41a5ee766403f8d7.parquet` | 16.072 | 282,660 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/429fc3fe6c45a76d.parquet` | 1.541 | 26,042 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/430c88c9a100d0dc.parquet` | 0.353 | 5,519 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/44282524a4430968.parquet` | 0.006 | 5 | 2025-06-14 – 2025-09-07 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/4ac8558610ab032b.parquet` | 0.143 | 2,098 | 2025-01-01 – 2025-12-08 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/4d68bfa379f1c03c.parquet` | 0.004 | 1 | 2025-09-22 – 2025-09-22 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/4e280d8a970c2aeb.parquet` | 0.007 | 13 | 2025-02-20 – 2025-12-17 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/4ea3574e89575f33.parquet` | 0.035 | 416 | 2025-01-07 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/50551e186d5c7980.parquet` | 0.007 | 17 | 2025-01-03 – 2025-10-03 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/507e397c7d5d8f6e.parquet` | 0.486 | 8,618 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/527419d261a00fc9.parquet` | 0.135 | 2,018 | 2025-01-09 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/531ca0e1f483bb14.parquet` | 1.121 | 18,815 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/583e252e30da7966.parquet` | 0.074 | 1,061 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/5915eb0f2b96108f.parquet` | 2.523 | 43,368 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/59492c931307fc12.parquet` | 0.057 | 757 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/5aec6e44d45785c6.parquet` | 69.297 | 1,251,438 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/5b9b55b3919d0805.parquet` | 0.006 | 9 | 2025-01-09 – 2025-09-13 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/5c9296fc3ec3d6b3.parquet` | 0.284 | 4,282 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/5cf48742b96a51c8.parquet` | 0.005 | 3 | 2025-02-25 – 2025-08-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/5de7a88a7d612b90.parquet` | 0.068 | 990 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/5e0f78c74650cb7c.parquet` | 0.013 | 108 | 2025-01-07 – 2025-11-24 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/5f15b8661aeecfde.parquet` | 0.183 | 2,957 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/5fe0f45aa5bb752d.parquet` | 1.540 | 27,096 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/5ff47410e915fc21.parquet` | 0.474 | 7,456 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/603da90a74a3a84e.parquet` | 3.122 | 53,579 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/608a890b9cb07c3d.parquet` | 0.004 | 1 | 2025-08-25 – 2025-08-25 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/619fdef8ce36f639.parquet` | 0.043 | 549 | 2025-01-06 – 2025-12-11 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/62a498fc39aa56f6.parquet` | 0.037 | 448 | 2025-01-12 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/65949b0c91a92f0b.parquet` | 0.300 | 4,683 | 2025-01-03 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/66cac7de8a188337.parquet` | 8.090 | 142,877 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/68b50f6c1916b818.parquet` | 0.012 | 95 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/6a61d5af3b05e14d.parquet` | 2.327 | 39,421 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/6a7b0763646b654f.parquet` | 1.165 | 19,777 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/6b7a86e96f5168b3.parquet` | 0.004 | 1 | 2025-02-25 – 2025-02-25 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/6c0af3ab75ae448b.parquet` | 0.309 | 4,813 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/6ca403d8f72659b8.parquet` | 0.008 | 25 | 2025-01-03 – 2025-10-08 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/6f2f582833522d11.parquet` | 7.875 | 139,554 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/6f806e46af87254c.parquet` | 0.271 | 3,988 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/70acf1794ef2ee4f.parquet` | 0.786 | 13,081 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7186c03b9404d53b.parquet` | 2.558 | 44,708 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/72af425a7f21f676.parquet` | 4.639 | 80,802 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/73fd5d67faacfbf5.parquet` | 0.076 | 1,027 | 2025-01-04 – 2025-11-04 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/741b5507d2a87aed.parquet` | 50.006 | 916,099 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/747568e7a5388ebf.parquet` | 3.087 | 53,898 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/766e64e3946b1648.parquet` | 1.761 | 31,033 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/774edc5d65bf5eaa.parquet` | 0.132 | 1,942 | 2025-01-06 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/77c478493dca9f5d.parquet` | 2.146 | 37,656 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/78a3ccf45adb03d0.parquet` | 0.181 | 2,768 | 2025-01-02 – 2025-12-20 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/78d52b42ba4fb2bc.parquet` | 11.948 | 210,803 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7925355f8d39630c.parquet` | 0.006 | 7 | 2025-02-06 – 2025-09-08 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/793dd2a836ca4f9e.parquet` | 2.013 | 35,337 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7a825549fe786459.parquet` | 12.802 | 225,878 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7aa14d18c9811edd.parquet` | 6.910 | 122,502 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7befdbb79f07d251.parquet` | 2.803 | 49,442 | 2025-01-01 – 2025-12-24 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7c37aa9007f5c2e3.parquet` | 0.004 | 1 | 2025-02-09 – 2025-02-09 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7c5103cb29909dc0.parquet` | 0.963 | 16,062 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7c8095142af10dea.parquet` | 0.064 | 840 | 2025-01-10 – 2025-12-26 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7dccf929d3f2ec7f.parquet` | 1.081 | 18,406 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7e0480de7f73c29d.parquet` | 5.220 | 90,750 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7e3c0242780233ea.parquet` | 26.874 | 476,575 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/7f7fd5387cf42b28.parquet` | 0.010 | 53 | 2025-01-04 – 2025-11-23 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/80e5856d94f08470.parquet` | 0.089 | 1,254 | 2025-01-01 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/8298d39267639d90.parquet` | 1.173 | 19,930 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/82a9f49ba3178697.parquet` | 0.006 | 8 | 2025-01-15 – 2025-12-18 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/836aed3a9e3d4329.parquet` | 0.140 | 1,969 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/86227fac4975e118.parquet` | 0.477 | 7,814 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/871c1e89c94806e8.parquet` | 0.038 | 478 | 2025-01-07 – 2025-11-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/873de26773700332.parquet` | 0.215 | 3,249 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/885e6340b39b8748.parquet` | 0.679 | 10,840 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/88c40098eb56fadd.parquet` | 0.255 | 3,870 | 2025-01-02 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/890e861a4cb1f6db.parquet` | 36.705 | 646,376 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/8aea46fdd93bb8c0.parquet` | 1.791 | 30,751 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/8b2b09fc7690b319.parquet` | 0.006 | 6 | 2025-01-22 – 2025-12-23 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/8c1a29637a5a9400.parquet` | 0.006 | 11 | 2025-04-08 – 2025-05-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/8c40557cd7377178.parquet` | 0.004 | 1 | 2025-05-12 – 2025-05-12 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/8c67906df28f77eb.parquet` | 70.887 | 1,260,755 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/8cfedd7f2181cef5.parquet` | 0.005 | 4 | 2025-01-29 – 2025-10-18 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/8d26160d5f1d56d0.parquet` | 0.066 | 921 | 2025-01-07 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/8dbce724d29d495e.parquet` | 0.005 | 1 | 2025-04-27 – 2025-04-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/8eefa32d27f58bff.parquet` | 0.009 | 47 | 2025-01-09 – 2025-05-27 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/8f6ccfb675dcaae0.parquet` | 0.142 | 2,148 | 2025-01-14 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9411018e3751512d.parquet` | 0.396 | 6,125 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9516c59c7dab0510.parquet` | 0.005 | 1 | 2025-03-09 – 2025-03-09 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/95d16b9295528d5d.parquet` | 0.545 | 9,000 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9631c4c6ee50b282.parquet` | 3.898 | 67,522 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/968576fd61507e0c.parquet` | 2.031 | 35,400 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/96c424783218e45d.parquet` | 0.353 | 5,571 | 2025-01-10 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/97f1422a43fc478b.parquet` | 0.004 | 1 | 2025-08-13 – 2025-08-13 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9818fb9fff05347e.parquet` | 4.162 | 72,929 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9961ea9d5932ad59.parquet` | 1.072 | 18,301 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9a0241db1791e187.parquet` | 0.818 | 13,253 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9b0e953e5667d535.parquet` | 2.521 | 43,511 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9c5b15dda062a16e.parquet` | 0.089 | 1,269 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9c92b61715929b67.parquet` | 0.209 | 3,246 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9c95486e1b9aa6e9.parquet` | 12.845 | 227,320 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9e0ad97d1bdc7dab.parquet` | 0.005 | 4 | 2025-05-01 – 2025-10-03 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9e231863813cf036.parquet` | 1.205 | 20,419 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/9f0327c4188b76cd.parquet` | 0.046 | 584 | 2025-01-08 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/a017ef920c027930.parquet` | 0.006 | 13 | 2025-03-09 – 2025-10-19 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/a094b37ec2006870.parquet` | 0.087 | 1,181 | 2025-01-10 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/a1532772127dea46.parquet` | 0.333 | 5,066 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/a312e2baf2f27fca.parquet` | 0.204 | 3,260 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/a4cd88d142cd66d0.parquet` | 0.039 | 516 | 2025-01-06 – 2025-12-19 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/a5e4391bfb26a027.parquet` | 3.729 | 64,117 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/a60b12a99ae84184.parquet` | 0.006 | 5 | 2025-07-12 – 2025-10-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/a6f5066bc491da89.parquet` | 5.763 | 101,805 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/a8f1cf951a8e8192.parquet` | 0.017 | 148 | 2025-01-07 – 2025-12-17 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/a9bea5fe3d620367.parquet` | 34.031 | 599,335 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/aa8f6ae6df3849e7.parquet` | 0.007 | 17 | 2025-11-18 – 2025-11-19 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/abcd94ea9073943d.parquet` | 0.015 | 135 | 2025-03-02 – 2025-11-18 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/b0e941d0bf226c1d.parquet` | 26.960 | 469,809 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/b1464ef0b8d8debd.parquet` | 5.855 | 103,794 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/b194f511b1e9835d.parquet` | 0.220 | 3,236 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/b218bb83b6b7095a.parquet` | 0.373 | 5,717 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/b32bcf4af40085d0.parquet` | 0.064 | 856 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/b3993353bcb07c72.parquet` | 1.538 | 25,885 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/b4c0bda6a8e39df9.parquet` | 0.558 | 9,116 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/b527a5a0d8ae72c8.parquet` | 0.271 | 4,039 | 2025-01-02 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/b5374970121d56be.parquet` | 0.090 | 1,282 | 2025-01-08 – 2025-12-10 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/ba3cd9eb36eb2ab0.parquet` | 0.623 | 9,888 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/bac66ed395351657.parquet` | 0.136 | 2,035 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/bbca93e6c56949ab.parquet` | 0.008 | 34 | 2025-07-01 – 2025-09-18 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/bc2302b661dedf12.parquet` | 0.048 | 632 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/bd2ce7486e065c8a.parquet` | 0.024 | 255 | 2025-01-04 – 2025-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/c018dfdc7e2f013e.parquet` | 16.887 | 302,675 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/c2d614efbee261fb.parquet` | 0.143 | 2,109 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/c2e5deeab7685853.parquet` | 0.300 | 4,891 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/c3523fa384e0db4d.parquet` | 0.073 | 1,009 | 2025-01-03 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/c49ce1fe6897a64f.parquet` | 0.019 | 191 | 2025-01-04 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/c57ff17615678af6.parquet` | 110.461 | 1,958,522 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/c8478be2ce58d278.parquet` | 6.123 | 109,649 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/c9afec4e28eec7d2.parquet` | 0.322 | 5,018 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/c9fe54cbcc73fd35.parquet` | 0.076 | 1,034 | 2025-01-05 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/ce7d18597d079569.parquet` | 5.645 | 96,056 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/cf5f1080741b2d9f.parquet` | 12.209 | 216,290 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/cf73db0a052b126f.parquet` | 4.723 | 83,148 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/d110f2451044395c.parquet` | 0.081 | 1,145 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/d1c0f725e7e65910.parquet` | 0.006 | 5 | 2025-10-28 – 2025-10-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/d51906c9a87191f4.parquet` | 0.582 | 9,263 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/d6d17fcc936a3278.parquet` | 15.945 | 276,921 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/d7a02f21f567063e.parquet` | 1.132 | 18,652 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/d8ad0de096daf1df.parquet` | 4.131 | 73,875 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/dc1e2e20c2177e4d.parquet` | 42.810 | 766,112 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/e1ff03b0103084f0.parquet` | 3.402 | 59,685 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/e34eead4e2eb8e2b.parquet` | 8.607 | 154,279 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/e3579c2ec2abcb35.parquet` | 0.015 | 122 | 2025-01-03 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/e43ccdd039811bdd.parquet` | 13.254 | 234,909 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/e4930ac5c72e616c.parquet` | 0.164 | 2,478 | 2025-01-01 – 2025-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/e6585a7974e36e05.parquet` | 0.004 | 1 | 2025-03-01 – 2025-03-01 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/e668629a9fdbe926.parquet` | 0.015 | 125 | 2025-01-04 – 2025-12-22 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/e757946864db0c7d.parquet` | 0.251 | 3,719 | 2025-01-02 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/e86eb05d0bf7a9f8.parquet` | 0.546 | 9,199 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/e8c6a218a1544eee.parquet` | 0.516 | 8,563 | 2025-01-08 – 2025-12-07 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/e9ca75cb36108611.parquet` | 0.048 | 630 | 2025-01-02 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/eb19074af5e0e0c3.parquet` | 0.025 | 291 | 2025-01-19 – 2025-10-23 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/ebfe468e3130a717.parquet` | 0.219 | 3,508 | 2025-01-02 – 2025-12-28 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/ec24c66885526915.parquet` | 0.242 | 3,688 | 2025-01-06 – 2025-12-14 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/edc1321295216e26.parquet` | 0.126 | 1,955 | 2025-01-04 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/f2667e352a1ba356.parquet` | 0.088 | 1,222 | 2025-01-01 – 2025-12-30 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/f4a5f87d38b1eeee.parquet` | 0.133 | 2,017 | 2025-01-05 – 2025-12-15 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/fa88895f3bb256e2.parquet` | 0.449 | 7,301 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/fb254e2b92c86283.parquet` | 0.553 | 8,959 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/fc444c3861e04520.parquet` | 1.628 | 27,639 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/fc6124132d581b97.parquet` | 0.169 | 2,457 | 2025-01-01 – 2025-12-31 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/fcfee3be19e9613e.parquet` | 0.006 | 8 | 2025-02-14 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2025/product_type=SP/product=VIIRS_SNPP_SP/feb3a275aee26f8d.parquet` | 0.259 | 3,931 | 2025-01-10 – 2025-12-29 |
| `data/processed/observations/sensor_family=VIIRS/year=2026/product_type=NRT/product=VIIRS_NOAA21_NRT/73b043f82e531ed0.parquet` | 397.755 | 7,177,402 | 2026-08-01 – 2026-11-14 |

Parquet scan count: 2,042; extant-file aggregate size: 7.04 GiB. Raw extracted files: 10,154; about 46.07 GiB.

## 2. FILE INVENTORY TABLE

Every discovered non-data source/config/doc/test file. `.env` is not inventoried or opened. Internal imports are only those expressed as local module imports. Archived backup content is included and labeled.

| Path | Lines | Purpose (one sentence) | Key exports/functions/routes/components | Depends on (internal imports) |
|---|---:|---|---|---|
| `data/raw/README.txt` | 20 | Documents expected downloaded archive and extraction folder structure. | — | — |
| `.gitignore` | 12 | Git exclusions for local/secrets/generated content. | — | — |
| `.pytest_cache/.gitignore` | 2 | Application source/configuration; purpose inferred from filename and imports (ASSUMED). | — | — |
| `.pytest_cache/README.md` | 8 | Project documentation or archived README. | — | — |
| `.ruff_cache/.gitignore` | 2 | Application source/configuration; purpose inferred from filename and imports (ASSUMED). | — | — |
| `AUDIT_REPORT.md` | 400 | Prior project audit artifact. | — | — |
| `backend/.pytest_cache/.gitignore` | 2 | Application source/configuration; purpose inferred from filename and imports (ASSUMED). | — | — |
| `backend/.pytest_cache/README.md` | 8 | Project documentation or archived README. | — | — |
| `backend/.ruff_cache/.gitignore` | 2 | Application source/configuration; purpose inferred from filename and imports (ASSUMED). | — | — |
| `backend/app/__init__.py` | 1 | Application source/configuration; purpose inferred from filename and imports (ASSUMED). | — | — |
| `backend/app/analytics_api.py` | 237 | Bounded DuckDB queries and analytics input validation. | daily_cell_paths, AnalyticsQueryError, AnalyticsTimeout, validate_bbox, parse_geojson_polygon, _validate_range, get_calendar, coverage_status, check_coverage, unavailable_analysis | app.harmonize |
| `backend/app/firms.py` | 73 | FIRMS live/archive request and response parsing. | FirmsApiError, _load, load_latest, load_archive | app.validation |
| `backend/app/harmonize.py` | 268 | Common-grid sensor comparison calculations and explicit calibration status. | HarmonizationQueryError, _as_date, _validate_bbox, _orientation, _rings_sql, query_common_grid_comparison | — |
| `backend/app/local_archive.py` | 216 | Local country archive discovery, row filters and calendar aggregation. | _year_dir, available_products, _countries_for_product, available_countries, _country_file, load_country_window, _daily_record_counts, summarize_country_month | app.firms, app.validation |
| `backend/app/main.py` | 276 | FastAPI app, middleware and HTTP route handlers. | limit_api_rate, health, firms_latest, firms_archive, ingest_firms, local_archive_countries, local_archive_catalog, local_archive_records, local_archive_calendar, _parse_bbox, local_data_quality, local_coverage, local_coverage_check, analytics_calendar, analytics_climatology, analytics_anomalies, analytics_critical_periods | app.analytics_api, app.firms, app.local_archive, app.validation |
| `backend/app/validation.py` | 100 | FIRMS CSV schema validation and record parsing. | CsvValidationError, _normalized_headers, _value, parse_firms_csv | — |
| `backend/check.ps1` | 13 | Backend check runner. | — | — |
| `backend/pyproject.toml` | 8 | Python tooling/project configuration. | — | — |
| `backend/requirements.txt` | 8 | Backend runtime dependencies. | — | — |
| `backend/scripts/__init__.py` | 1 | Application source/configuration; purpose inferred from filename and imports (ASSUMED). | — | — |
| `backend/scripts/build_processed.py` | 684 | Validates and processes source CSVs into resumable Parquet and metadata outputs. | _safe_name, discover_csv_files, coverage_table, _qident, _literal, _open_csv, _normalize_headers, _expr, _source_select, _atomic_json, _output_path, _write_parquet_atomic, process_entry, build_daily_cells, run, parser | — |
| `backend/tests/test_analytics_api.py` | 146 | Automated tests for the associated application or backend behavior. | cells_file, test_calendar_bbox_query_is_bounded_and_keeps_product_streams, test_calendar_geojson_filters_cell_centers, test_calendar_reads_product_family_year_partitioned_dataset, test_calendar_rejects_bad_polygon_and_long_window, test_api_calendar_and_insufficient_anomaly_status, test_api_returns_actionable_errors, test_coverage_check_labels_date_envelopes_and_spatial_uncertainty, test_coverage_check_suggests_alternate_processing_stream, test_coverage_endpoints_publish_file_completeness_and_validate_selection | app.analytics_api, app.main |
| `backend/tests/test_firms.py` | 58 | Automated tests for the associated application or backend behavior. | test_live_client_uses_allowlisted_source_and_keeps_provenance, test_live_client_requires_a_key_and_rejects_unsupported_legacy_feed, test_latest_route_reports_key_setup_and_rejects_retired_feed, test_archive_client_uses_date_bounded_standard_processing_feed | app.firms, app.main |
| `backend/tests/test_harmonize.py` | 63 | Automated tests for the associated application or backend behavior. | daily_cells, test_comparison_keeps_sources_separate_and_reports_cell_overlap, test_nrt_and_platform_filter_are_explicit, test_invalid_comparison_filters_are_actionable | app.harmonize |
| `backend/tests/test_processing.py` | 204 | Automated tests for the associated application or backend behavior. | test_discovers_country_and_noaa21_global_streams, test_processing_validates_normalizes_and_aggregates_exact_duplicates, test_compact_cell_shard_preserves_sensor_metrics_and_cell_presence, test_compact_mode_converts_existing_observation_parquet_without_raw_csv, test_noaa21_sp_precedes_nrt_until_the_latest_sp_date, test_run_records_corrupt_file_in_quarantine_report_and_resumes, test_coverage_table_counts_expected_processed_and_failed, test_full_run_disk_preflight_stops_without_touching_raw_files, test_catalog_records_unsupported_csv_without_processing_it | — |
| `backend/tests/test_validation.py` | 104 | Automated tests for the associated application or backend behavior. | test_parses_supported_firms_columns_and_preserves_original_metadata, test_reports_missing_columns_actionably, test_reports_invalid_coordinates_with_row_number, test_refuses_blank_sensor_and_bad_brightness, test_reports_invalid_date_format, test_date_window_filters_records_and_allows_no_matches, test_rejects_empty_rows, test_ingestion_api_returns_clear_validation_error_and_health_status, test_local_archive_reads_country_files_and_keeps_sensors_distinct, test_local_archive_catalog_exposes_sources_by_year_and_future_noaa21 | app.main, app.validation, app |
| `backups/firewatch-pre-2.0-20261114-202127/.gitignore` | 9 | Archived project snapshot; not wired into current runtime. | — | — |
| `backups/firewatch-pre-2.0-20261114-202127/backend/app/__init__.py` | 1 | Archived project snapshot; not wired into current runtime. | — | — |
| `backups/firewatch-pre-2.0-20261114-202127/backend/app/firms.py` | 73 | Archived project snapshot; not wired into current runtime. | FirmsApiError, _load, load_latest, load_archive | app.validation |
| `backups/firewatch-pre-2.0-20261114-202127/backend/app/local_archive.py` | 216 | Archived project snapshot; not wired into current runtime. | _year_dir, available_products, _countries_for_product, available_countries, _country_file, load_country_window, _daily_record_counts, summarize_country_month | app.firms, app.validation |
| `backups/firewatch-pre-2.0-20261114-202127/backend/app/main.py` | 127 | Archived project snapshot; not wired into current runtime. | health, firms_latest, firms_archive, ingest_firms, local_archive_countries, local_archive_catalog, local_archive_records, local_archive_calendar | app.validation, app.firms, app.local_archive |
| `backups/firewatch-pre-2.0-20261114-202127/backend/app/validation.py` | 100 | Archived project snapshot; not wired into current runtime. | CsvValidationError, _normalized_headers, _value, parse_firms_csv | — |
| `backups/firewatch-pre-2.0-20261114-202127/backend/tests/test_firms.py` | 58 | Automated tests for the associated application or backend behavior. | test_live_client_uses_allowlisted_source_and_keeps_provenance, test_live_client_requires_a_key_and_rejects_unsupported_legacy_feed, test_latest_route_reports_key_setup_and_rejects_retired_feed, test_archive_client_uses_date_bounded_standard_processing_feed | app.firms, app.main |
| `backups/firewatch-pre-2.0-20261114-202127/backend/tests/test_validation.py` | 96 | Automated tests for the associated application or backend behavior. | test_parses_supported_firms_columns_and_preserves_original_metadata, test_reports_missing_columns_actionably, test_reports_invalid_coordinates_with_row_number, test_refuses_blank_sensor_and_bad_brightness, test_reports_invalid_date_format, test_date_window_filters_records_and_allows_no_matches, test_rejects_empty_rows, test_ingestion_api_returns_clear_validation_error_and_health_status, test_local_archive_reads_country_files_and_keeps_sensors_distinct, test_local_archive_catalog_exposes_sources_by_year_and_future_noaa21 | app.main, app.validation, app |
| `backups/firewatch-pre-2.0-20261114-202127/data/raw/README.txt` | 17 | Archived project snapshot; not wired into current runtime. | — | — |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/index.html` | 1 | Archived project snapshot; not wired into current runtime. | — | — |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/package.json` | 9 | Archived project snapshot; not wired into current runtime. | — | — |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/src/data/demo.ts` | 11 | Archived project snapshot; not wired into current runtime. | FireRecord, demoRecords | — |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/src/lib/filters.test.ts` | 17 | Automated tests for the associated application or backend behavior. | — | ../data/demo, ./filters |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/src/lib/filters.ts` | 22 | Archived project snapshot; not wired into current runtime. | Filters, filterRecords, regionFor, csvFor | ../data/demo |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/src/main.tsx` | 6 | Archived project snapshot; not wired into current runtime. | — | ./ui/App |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/src/styles.css` | 8 | Archived project snapshot; not wired into current runtime. | — | — |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/src/testSetup.ts` | 1 | Archived project snapshot; not wired into current runtime. | — | — |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/src/ui/App.tsx` | 178 | Archived project snapshot; not wired into current runtime. | App | ../data/demo, ../lib/filters |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/src/ui/MapView.tsx` | 27 | Archived project snapshot; not wired into current runtime. | MapView | ../data/demo |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/src/ui/TimelineChart.tsx` | 7 | Archived project snapshot; not wired into current runtime. | TimelineChart | — |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/src/vite-env.d.ts` | 1 | Archived project snapshot; not wired into current runtime. | — | — |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/tsconfig.json` | 1 | Archived project snapshot; not wired into current runtime. | — | — |
| `backups/firewatch-pre-2.0-20261114-202127/frontend/vite.config.ts` | 3 | Archived project snapshot; not wired into current runtime. | default export | — |
| `backups/firewatch-pre-2.0-20261114-202127/package.json` | 12 | Archived project snapshot; not wired into current runtime. | — | — |
| `backups/firewatch-pre-2.0-20261114-202127/README.md` | 94 | Archived project snapshot; not wired into current runtime. | — | — |
| `docs/API.md` | 18 | API interface and limits documentation. | — | — |
| `docs/DATA_ENGINE.md` | 43 | Ingestion and processed storage documentation. | — | — |
| `docs/HARMONIZATION.md` | 31 | Comparison method and limits documentation. | — | — |
| `docs/LIMITATIONS.md` | 12 | Data coverage and interpretation limits documentation. | — | — |
| `eslint.config.mjs` | 18 | ESLint configuration. | default export | — |
| `frontend/index.html` | 1 | Vite HTML entry point. | — | — |
| `frontend/package.json` | 9 | Frontend dependencies and scripts. | — | — |
| `frontend/src/data/demo.ts` | 11 | Deterministic simulated fixture records and record type. | FireRecord, demoRecords | — |
| `frontend/src/lib/apiClient.test.ts` | 33 | Automated tests for the associated application or backend behavior. | — | ./apiClient |
| `frontend/src/lib/apiClient.ts` | 79 | Fetch wrapper with timeouts, retries and error mapping. | ApiErrorKind, ApiClientError, apiRequest, apiGet, apiPost, errorMessage | — |
| `frontend/src/lib/filters.test.ts` | 29 | Automated tests for the associated application or backend behavior. | — | ../data/demo, ./filters |
| `frontend/src/lib/filters.ts` | 29 | Record filtering and CSV serialization. | Filters, filterRecords, withDateBound, regionFor, csvFor | ../data/demo |
| `frontend/src/main.tsx` | 6 | React application mounting point. | — | ./ui/App |
| `frontend/src/styles.css` | 15 | Dashboard styling and responsive layout. | — | — |
| `frontend/src/testSetup.ts` | 1 | Application source/configuration; purpose inferred from filename and imports (ASSUMED). | — | — |
| `frontend/src/ui/App.test.tsx` | 31 | Automated tests for the associated application or backend behavior. | — | ./App |
| `frontend/src/ui/App.tsx` | 225 | Root dashboard state, controls, source status, map/calendar/upload and export wiring. | App | ../data/demo, ../lib/filters, ../lib/apiClient, ./ProcessedComparison, ./DataExplorer |
| `frontend/src/ui/DataExplorer.test.tsx` | 22 | Automated tests for the associated application or backend behavior. | — | ../data/demo, ./DataExplorer |
| `frontend/src/ui/DataExplorer.tsx` | 28 | Selected observation table and data exploration panel. | DataExplorer | ../data/demo, ../lib/filters |
| `frontend/src/ui/MapView.tsx` | 47 | Interactive map and area-of-interest interaction. | MapView | ../data/demo |
| `frontend/src/ui/ProcessedComparison.test.tsx` | 44 | Automated tests for the associated application or backend behavior. | — | ./ProcessedComparison |
| `frontend/src/ui/ProcessedComparison.tsx` | 108 | Processed MODIS/VIIRS comparison query, coverage and CSV export. | ProcessedComparison | ../lib/apiClient |
| `frontend/src/ui/TimelineChart.tsx` | 7 | Daily activity visualization. | TimelineChart | — |
| `frontend/src/vite-env.d.ts` | 1 | Application source/configuration; purpose inferred from filename and imports (ASSUMED). | — | — |
| `frontend/tsconfig.json` | 1 | Frontend TypeScript compiler configuration. | — | — |
| `frontend/vite.config.ts` | 3 | Vite and frontend test configuration. | default export | — |
| `package-lock.json` | 4929 | Locked npm dependency graph. | — | — |
| `package.json` | 25 | Root scripts and npm workspace configuration. | — | — |
| `process_2020_2026_compact.bat` | 19 | Runs selected-year compact Parquet processing. | — | — |
| `README.md` | 93 | Project run, provenance and data processing instructions. | — | — |
| `scripts/dev.mjs` | 75 | Starts API/Vite, checks health/ports and stops child processes. | — | — |
| `start.bat` | 26 | Windows dependency bootstrap and local app launcher. | — | — |

## 3. ENTRY POINTS AND WIRING

### Startup commands

- `npm run dev` runs `scripts/dev.mjs`: FastAPI at `127.0.0.1:8000`, waits for API health, then Vite at `127.0.0.1:5173`; port/Python overrides are below. Ctrl+C stops both.
- `start.bat` checks/install npm dependencies, creates `.venv`, installs backend requirements if needed, then invokes `npm run dev`.
- `npm run api` starts only Uvicorn (`backend/app.main:app`, default 8000). `npm run dev:frontend` starts only Vite (default 5173).
- `process_2020_2026_compact.bat` invokes `backend/scripts/build_processed.py` for 2020–2026 with compact cell and daily-cell options; it is a data-processing launcher, not an app launcher.
- FastAPI interactive docs: `/docs` on the API port.

### Backend routes

| Method | Path | Handler | File:line |
|---|---|---|---|
| GET | `/api/health` | `health` | `backend/app/main.py:59` |
| GET | `/api/firms/latest` | `firms_latest` | `backend/app/main.py:68` |
| GET | `/api/firms/archive` | `firms_archive` | `backend/app/main.py:86` |
| POST | `/api/ingest/firms` | `ingest_firms` | `backend/app/main.py:105` |
| GET | `/api/local-archive/countries` | `local_archive_countries` | `backend/app/main.py:119` |
| GET | `/api/local-archive/catalog` | `local_archive_catalog` | `backend/app/main.py:129` |
| GET | `/api/local-archive/records` | `local_archive_records` | `backend/app/main.py:139` |
| GET | `/api/local-archive/calendar` | `local_archive_calendar` | `backend/app/main.py:160` |
| GET | `/api/data-quality` | `local_data_quality` | `backend/app/main.py:191` |
| GET | `/api/coverage` | `local_coverage` | `backend/app/main.py:199` |
| GET | `/api/coverage/check` | `local_coverage_check` | `backend/app/main.py:208` |
| GET | `/api/calendar` | `analytics_calendar` | `backend/app/main.py:224` |
| GET | `/api/climatology` | `analytics_climatology` | `backend/app/main.py:243` |
| GET | `/api/anomalies` | `analytics_anomalies` | `backend/app/main.py:255` |
| GET | `/api/critical-periods` | `analytics_critical_periods` | `backend/app/main.py:267` |

### Frontend component tree

`frontend/src/main.tsx` mounts `App`. Main component relationships:

```text
App
├── DataExplorer
├── MapView (lazy + Suspense)
├── TimelineChart (lazy + Suspense)
└── ProcessedComparison
```

The above are the root dashboard’s principal components; exact placement and conditional rendering are in `frontend/src/ui/App.tsx`. `MapView` and `TimelineChart` are lazy imports.

### Frontend API calls

| File:line | URL template |
|---|---|
| `frontend/src/ui/App.tsx:63` | `${api}/api/health` |
| `frontend/src/ui/App.tsx:83` | `${api}/api/local-archive/catalog?year=${localYear}` |
| `frontend/src/ui/App.tsx:119` | `${api}/api/ingest/firms` |
| `frontend/src/ui/App.tsx:132` | `${api}/api/firms/latest?${query}` |
| `frontend/src/ui/App.tsx:146` | `${api}/api/firms/archive?${query}` |
| `frontend/src/ui/App.tsx:159` | `${api}/api/local-archive/calendar?${query}` |
| `frontend/src/ui/App.tsx:173` | `${api}/api/local-archive/records?${query}` |
| `frontend/src/ui/ProcessedComparison.tsx:42` | `${api}/api/data-quality` |
| `frontend/src/ui/ProcessedComparison.tsx:59` | `${api}/api/calendar?${params}` |

### Data flow (8 steps)

1. FIRMS ZIPs and extracted CSVs reside under `data/raw/archives/` and `data/raw/extracted/`.
2. `backend/scripts/build_processed.py` discovers source CSVs and validates required schema/values.
3. Processing emits source-aware Parquet under `data/processed/observations/` or `cell_shards/`, plus index, manifest and quality report.
4. `backend/app/analytics_api.py` and `harmonize.py` query processed Parquet using DuckDB with time/spatial constraints.
5. FastAPI routes return local archive records/calendars, coverage, quality, or comparison outputs; separate live routes use FIRMS API.
6. React `App` fetches health/catalog/archive/live/upload endpoints; `ProcessedComparison` fetches data quality and calendar endpoints.
7. Map/calendar/timeline/table use selected records; CSV exports retain source provenance and sensor identity.
8. Deterministic fixtures in `frontend/src/data/demo.ts` are explicitly labeled “Simulated demo data,” not NASA observations.

## 4. CONFIGURATION

### Environment variable names (values excluded)

| Name | Read at | Default | Purpose |
|---|---|---|---|
| `FIREWATCH_API_PORT` | `scripts/dev.mjs:9` | 8000 | Combined launcher API port. |
| `FIREWATCH_CORS_ORIGINS` | `backend/app/main.py:33` | localhost and 127.0.0.1 on port 5173 | Allowed frontend origins for API CORS. |
| `FIREWATCH_PYTHON` | `scripts/dev.mjs:11` | `.venv/Scripts/python.exe` if present; otherwise `python` | Optional Python executable override. |
| `FIREWATCH_WEB_PORT` | `scripts/dev.mjs:10` | 5173 | Combined launcher Vite port. |
| `FIRMS_MAP_KEY` | `backend/app/firms.py:29`, `backend/app/firms.py:31`, `backend/app/main.py:64`, `backend/app/main.py:81`, `backend/app/main.py:100`, `backend/tests/test_firms.py:19`, `backend/tests/test_firms.py:31`, `backend/tests/test_firms.py:33`, `backend/tests/test_firms.py:43`, `backend/tests/test_firms.py:50`, `backend/tests/test_firms.py:55`, `backups/firewatch-pre-2.0-20261114-202127/backend/app/firms.py:29`, `backups/firewatch-pre-2.0-20261114-202127/backend/app/firms.py:31`, `backups/firewatch-pre-2.0-20261114-202127/backend/app/main.py:20`, `backups/firewatch-pre-2.0-20261114-202127/backend/app/main.py:36`, `backups/firewatch-pre-2.0-20261114-202127/backend/app/main.py:55`, `backups/firewatch-pre-2.0-20261114-202127/backend/tests/test_firms.py:19`, `backups/firewatch-pre-2.0-20261114-202127/backend/tests/test_firms.py:31`, `backups/firewatch-pre-2.0-20261114-202127/backend/tests/test_firms.py:33`, `backups/firewatch-pre-2.0-20261114-202127/backend/tests/test_firms.py:43`, `backups/firewatch-pre-2.0-20261114-202127/backend/tests/test_firms.py:50`, `backups/firewatch-pre-2.0-20261114-202127/backend/tests/test_firms.py:55`, `backups/firewatch-pre-2.0-20261114-202127/frontend/src/ui/App.tsx:101`, `backups/firewatch-pre-2.0-20261114-202127/frontend/src/ui/App.tsx:116`, `backups/firewatch-pre-2.0-20261114-202127/frontend/src/ui/App.tsx:166`, `frontend/src/ui/App.tsx:211` | empty / unconfigured | Optional NASA FIRMS credential, backend only; value omitted. |
| `VITE_API_URL` | `backups/firewatch-pre-2.0-20261114-202127/frontend/src/ui/App.tsx:9`, `frontend/src/ui/App.tsx:12`, `scripts/dev.mjs:69` | `http://localhost:8000`; paired launcher supplies selected API port | Frontend API base URL. |

Root `.env` filename exists; content is **[REDACTED]** and was not inspected.

### Selected behavior constants

| File:line | Expression |
|---|---|
| `backend/app/analytics_api.py:18` | `MAX_CALENDAR_DAYS = 366` |
| `backend/app/analytics_api.py:19` | `MAX_BASELINE_DAYS = 366 * 27` |
| `backend/app/analytics_api.py:20` | `QUERY_TIMEOUT_SECONDS = 30` |
| `backend/app/local_archive.py:21` | `MAX_COUNTRY_FILE_BYTES = 150_000_000` |
| `backend/app/local_archive.py:22` | `MAX_WINDOW_DAYS = 31` |
| `backend/app/local_archive.py:24` | `MAX_YEAR = 2026` |
| `scripts/dev.mjs:9` | `const apiPort = Number(process.env.FIREWATCH_API_PORT || 8000);` |
| `scripts/dev.mjs:10` | `const webPort = Number(process.env.FIREWATCH_WEB_PORT || 5173);` |

Other observed bounds in route code/docs: FIRMS day query 1–5; CSV upload preview 10 MB; in-process API rate limit 120 requests/client/minute; processed calendar up to 366 days; local archive query window up to 31 days per README. Common-grid resolution and method details are defined in `backend/app/harmonize.py` and `docs/HARMONIZATION.md`.

## 5. HEALTH FLAGS (facts only)

### Files over 500 lines
- `backend/scripts/build_processed.py`: 684 lines.
- `package-lock.json`: 4,929 lines.

### Orphaned/duplicate candidates

- `AUDIT_REPORT.md` is a prior audit artifact with no runtime reference found; **ASSUMED orphaned**.
- `backups/firewatch-pre-2.0-20261114-202127/` contains an archived snapshot and duplicate/near-duplicate project files; current app wiring does not use it.
- `frontend/tsconfig.tsbuildinfo`, if present, is generated build metadata, not a runtime module.
- `data/processed/daily_cell.parquet` coexists with the partitioned `cell_shards/` outputs. `analytics_api.py` supports a legacy-file fallback; the files are parallel derived representations.
- No whole-program dead-code analyzer was run; any other unused status is **ASSUMED**.

### Standard files / testing

- `README.md`: present (README).
- `.gitignore`: present (Git ignore).
- `.env.example`: missing (environment template).
- `eslint.config.mjs`: present (lint configuration).
- `.github/workflows`: missing (CI configuration).
- `LICENSE`: missing (license).
- Backend tests are under `backend/tests/`; frontend tests are colocated under `frontend/src/` (`*.test.ts[x]`).
- Direct per-module tests were not found for `backend/app/main.py`, `backend/app/local_archive.py`, `frontend/src/ui/MapView.tsx`, `frontend/src/ui/TimelineChart.tsx`, `frontend/src/main.tsx`, `frontend/src/styles.css`, or `scripts/dev.mjs`; indirect coverage is possible.
- No end-to-end browser test suite was found.
- `data/raw/archives/` currently has no files; extracted sources are present.
- The processing process was active during scan; partial outputs or changing file sizes are a snapshot limitation, not a claim of completeness.
- This inventory does not validate source completeness, scientific validity, or MODIS/VIIRS calibration.
