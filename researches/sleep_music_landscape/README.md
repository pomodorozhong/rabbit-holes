# Sleep Music & White Noise — Marketing Landscape

Jupyter report on the YouTube + mobile-app marketing landscape for sleep music, white noise, nature soundscapes, and adjacent meditation/sleep products.

## Quick start

```bash
cd researches/sleep_music_landscape
uv sync

# Refresh curated tables + live scrapes (network required)
uv run python scripts/build_curated_datasets.py
uv run python scripts/fetch_youtube_channels.py
uv run python scripts/fetch_app_store_signals.py

# Open / execute the report
uv run jupyter notebook sleep_music_landscape.ipynb
# or headless:
uv run jupyter nbconvert --to notebook --execute sleep_music_landscape.ipynb --inplace
```

## What’s inside

| Path | Purpose |
|------|---------|
| `sleep_music_landscape.ipynb` | Full report with plots + citations |
| `scripts/fetch_youtube_channels.py` | Scrape YouTube `/about` + vidIQ + NicheTracker |
| `scripts/fetch_app_store_signals.py` | iTunes Lookup API + Google Play HTML signals |
| `scripts/build_curated_datasets.py` | Published stats → CSVs with `source_url` per row |
| `data/raw/` | Raw JSON scrape payloads |
| `data/processed/` | Analysis-ready CSVs |
| `figures/` | Plots written when the notebook runs |

## Coverage

- **YouTube:** subscribers, total/monthly views, estimated ad revenue per channel and per video, CPM/RPM vs finance / education / gaming / music / ASMR
- **Apps:** Calm / Headspace time series, Sleep Cycle filings, Sensor Tower US wellness weekly snapshots, storefront rating/install proxies, category revenue comparison
- **Citations:** every plotted series carries `source_name` / `source_url`; master index in the notebook §5

## Important caveats

- vidIQ earnings are **models**, not AdSense dashboards.
- Many specialist-app MAU/revenue figures are **US-only weekly** Sensor Tower points or third-party ML estimates.
- Google Play install figures are **public bands** (e.g. `10M+`), not exact downloads.
