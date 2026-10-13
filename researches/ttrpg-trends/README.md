# TTRPG Trends Analysis

Objective statistics on tabletop role-playing game (TTRPG) player preferences, market indicators, and crowdfunding trends — collected from public industry reports and visualized in Jupyter.

## Data sources

All datasets live in `data/`. Per-file provenance (source URLs, notes) is documented in **[data/README.md](data/README.md)**.

## Setup (uv)

```bash
cd researches/ttrpg-trends
uv sync
uv run jupyter notebook analysis/ttrpg_trends.ipynb
```

Or execute headlessly:

```bash
uv run jupyter nbconvert --to notebook --execute analysis/ttrpg_trends.ipynb
```

## Datasets

| File | Description |
|------|-------------|
| `kickstarter_rpg_crowdfunding_yearly.csv` | All-platform RPG crowdfunding by year |
| `kickstarter_tabletop_games_2024.csv` | Kickstarter tabletop games category metrics (2024) |
| `kickstarter_success_rate_yearly.csv` | Tabletop success rate trend (2022–2024) |
| `kickstarter_top_ttrpg_2024.csv` | Top-funded TTRPG Kickstarter campaigns (2024) |
| `crowdfunding_platform_share_2025.csv` | Kickstarter vs Backerkit vs GameOnTabletop share |
| `crowdfunding_non5e_systems_2025.csv` | Most-funded non-D&D 5E systems on crowdfunding |
| `crowdfunding_november_yoy.csv` | November YoY crowdfunding comparison |
| `market_indicators.csv` | Global market and player-base indicators |
| `player_engagement_wotc_2024.csv` | Official D&D / D&D Beyond engagement stats |
| `hobby_store_rpg_rankings.csv` | ICv2 hobby-channel RPG line rank order |
