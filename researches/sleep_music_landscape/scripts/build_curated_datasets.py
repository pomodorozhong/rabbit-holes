#!/usr/bin/env python3
"""Build curated datasets from published sources (with citations).

These tables encode figures that are not available via free public APIs
(e.g. annual revenue, MAU, Sensor Tower weekly snapshots). Every row includes
`source_name` and `source_url` so the notebook can cite them.

Re-run after updating figures; the notebook reads the CSVs directly.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {path} ({len(rows)} rows)")


def calm_headspace_timeseries() -> None:
    # Business of Apps Calm / Headspace statistics pages (2026 editions).
    calm_rev = [
        {"year": y, "metric": "revenue_usd_mm", "value": v, "app": "Calm",
         "source_name": "Business of Apps — Calm Revenue and Usage Statistics (2026)",
         "source_url": "https://www.businessofapps.com/data/calm-statistics/"}
        for y, v in [
            (2015, 2), (2016, 7), (2017, 37), (2018, 80), (2019, 150),
            (2020, 200), (2021, 330), (2022, 355), (2023, 300), (2024, 277),
            (2025, 210),
        ]
    ]
    calm_dl = [
        {"year": y, "metric": "downloads_mm", "value": v, "app": "Calm",
         "source_name": "Business of Apps — Calm Revenue and Usage Statistics (2026)",
         "source_url": "https://www.businessofapps.com/data/calm-statistics/"}
        for y, v in [
            (2016, 2.3), (2017, 8.9), (2018, 19.3), (2019, 24.5), (2020, 32.3),
            (2021, 20.6), (2022, 13.7), (2023, 9.5), (2024, 7.9), (2025, 7.3),
        ]
    ]
    calm_subs = [
        {"year": y, "metric": "paid_subscribers_mm", "value": v, "app": "Calm",
         "source_name": "Business of Apps — Calm Revenue and Usage Statistics (2026)",
         "source_url": "https://www.businessofapps.com/data/calm-statistics/"}
        for y, v in [
            (2017, 0.75), (2018, 1), (2019, 2), (2020, 4), (2021, 4.8),
            (2022, 5), (2023, 4.5), (2024, 4), (2025, 3.5),
        ]
    ]
    hs_rev = [
        {"year": y, "metric": "revenue_usd_mm", "value": v, "app": "Headspace",
         "source_name": "Business of Apps — Headspace Revenue and Usage Statistics (2026)",
         "source_url": "https://www.businessofapps.com/data/headspace-statistics/"}
        for y, v in [
            (2016, 30), (2017, 40), (2018, 60), (2019, 100), (2020, 150),
            (2021, 220), (2022, 235), (2023, 195), (2024, 175), (2025, 140),
        ]
    ]
    hs_dl = [
        {"year": y, "metric": "downloads_mm", "value": v, "app": "Headspace",
         "source_name": "Business of Apps — Headspace Revenue and Usage Statistics (2026)",
         "source_url": "https://www.businessofapps.com/data/headspace-statistics/"}
        for y, v in [
            (2016, 5), (2017, 9.9), (2018, 16.1), (2019, 15.3), (2020, 12.1),
            (2021, 9.9), (2022, 5.7), (2023, 5.1), (2024, 4), (2025, 3),
        ]
    ]
    hs_subs = [
        {"year": y, "metric": "paid_subscribers_mm", "value": v, "app": "Headspace",
         "source_name": "Business of Apps — Headspace Revenue and Usage Statistics (2026)",
         "source_url": "https://www.businessofapps.com/data/headspace-statistics/"}
        for y, v in [
            (2017, 0.4), (2018, 1), (2019, 1.3), (2020, 2), (2021, 3.5),
            (2022, 3.3), (2023, 2.8), (2024, 2.3), (2025, 2),
        ]
    ]
    rows = calm_rev + calm_dl + calm_subs + hs_rev + hs_dl + hs_subs
    write_csv(
        PROC / "app_calm_headspace_timeseries.csv",
        rows,
        ["app", "year", "metric", "value", "source_name", "source_url"],
    )


def sleep_cycle_kpis() -> None:
    # Sleep Cycle AB annual / year-end report 2025 (public company filings).
    # SEK figures; USD approx uses 10.5 SEK/USD illustrative mid-2025 rate noted in notes.
    sek_per_usd = 10.5
    rows = [
        {
            "metric": "net_sales_tsek",
            "year": 2025,
            "value": 247879,
            "unit": "tSEK",
            "notes": "Group net sales FY2025; -5.2% YoY",
            "source_name": "Sleep Cycle Year-end Report 2025",
            "source_url": "https://storage.mfn.se/79dd61f8-4ccc-4bc2-b095-feedaf3fced8/sleep-cycle-year-end-report-2025.pdf",
        },
        {
            "metric": "net_sales_tsek",
            "year": 2024,
            "value": 261529,
            "unit": "tSEK",
            "notes": "Prior-year comparison figure from YE 2025 report",
            "source_name": "Sleep Cycle Year-end Report 2025",
            "source_url": "https://storage.mfn.se/79dd61f8-4ccc-4bc2-b095-feedaf3fced8/sleep-cycle-year-end-report-2025.pdf",
        },
        {
            "metric": "paying_users",
            "year": 2025,
            "value": 768000,
            "unit": "users",
            "notes": "Paying users end-2025 (was 918k prior year)",
            "source_name": "Sleep Cycle Year-end Report 2025",
            "source_url": "https://storage.mfn.se/79dd61f8-4ccc-4bc2-b095-feedaf3fced8/sleep-cycle-year-end-report-2025.pdf",
        },
        {
            "metric": "paying_users",
            "year": 2024,
            "value": 918000,
            "unit": "users",
            "notes": "Prior-year paying users",
            "source_name": "Sleep Cycle Year-end Report 2025",
            "source_url": "https://storage.mfn.se/79dd61f8-4ccc-4bc2-b095-feedaf3fced8/sleep-cycle-year-end-report-2025.pdf",
        },
        {
            "metric": "arpu_sek",
            "year": 2025,
            "value": 277,
            "unit": "SEK",
            "notes": "Average revenue per user; currency-adjusted ARPU SEK 282",
            "source_name": "Sleep Cycle Year-end Report 2025",
            "source_url": "https://storage.mfn.se/79dd61f8-4ccc-4bc2-b095-feedaf3fced8/sleep-cycle-year-end-report-2025.pdf",
        },
        {
            "metric": "renewal_rate_pct",
            "year": 2025,
            "value": 45,
            "unit": "percent",
            "notes": "Subscription renewal rate stable at 45%",
            "source_name": "Sleep Cycle Year-end Report 2025",
            "source_url": "https://storage.mfn.se/79dd61f8-4ccc-4bc2-b095-feedaf3fced8/sleep-cycle-year-end-report-2025.pdf",
        },
        {
            "metric": "net_sales_usd_mm_approx",
            "year": 2025,
            "value": round(247879 / sek_per_usd / 1000, 2),
            "unit": "USD_mm",
            "notes": f"tSEK/1000/{sek_per_usd} SEK per USD illustrative conversion",
            "source_name": "Sleep Cycle Year-end Report 2025 (converted)",
            "source_url": "https://storage.mfn.se/79dd61f8-4ccc-4bc2-b095-feedaf3fced8/sleep-cycle-year-end-report-2025.pdf",
        },
        {
            "metric": "sleep_tech_market_sek_bn",
            "year": 2025,
            "value": 17,
            "unit": "SEK_bn",
            "notes": "Sleep tech market size cited in annual report narrative",
            "source_name": "Sleep Cycle Annual and Sustainability Report 2025",
            "source_url": "https://storage.mfn.se/d5bebf48-cfa5-4ce7-bb55-f23b91e4ea38/sleep-cycle-annual-and-sustainability-report-2025.pdf",
        },
    ]
    write_csv(
        PROC / "app_sleep_cycle_kpis.csv",
        rows,
        ["metric", "year", "value", "unit", "notes", "source_name", "source_url"],
    )


def sensor_tower_wellness_q2_2024() -> None:
    """Approximate mid-quarter / end-quarter weekly US unified figures from Sensor Tower blogs.

    Sensor Tower publishes weekly series narratively; we encode the start/end
    (or peak) points explicitly cited in the Q2 2024 wellness posts.
    """
    src = "Sensor Tower — Q2 2024 Top 5 Wellness Apps (US, unified iOS+Android)"
    url = "https://sensortower.com/blog/2024-q2-unified-top-5-wellness%20apps-revenue-us-63e274e1e1714cfff10eaa2f"
    rows = [
        # Headspace
        {"app": "Headspace", "week_label": "Q2_start", "metric": "weekly_revenue_usd", "value": 434000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "Headspace", "week_label": "Q2_end", "metric": "weekly_revenue_usd", "value": 428000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "Headspace", "week_label": "Q2_high", "metric": "weekly_downloads", "value": 35000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "Headspace", "week_label": "Q2_end", "metric": "weekly_downloads", "value": 29000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "Headspace", "week_label": "Q2_start", "metric": "weekly_active_users", "value": 550000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "Headspace", "week_label": "Q2_end", "metric": "weekly_active_users", "value": 504000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        # ShutEye
        {"app": "ShutEye", "week_label": "Q2_start", "metric": "weekly_revenue_usd", "value": 377000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "ShutEye", "week_label": "Q2_end", "metric": "weekly_revenue_usd", "value": 186000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "ShutEye", "week_label": "Q2_start", "metric": "weekly_downloads", "value": 183000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "ShutEye", "week_label": "Q2_end", "metric": "weekly_downloads", "value": 70000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "ShutEye", "week_label": "Q2_start", "metric": "weekly_active_users", "value": 382000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "ShutEye", "week_label": "Q2_end", "metric": "weekly_active_users", "value": 232000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        # Hatch Sleep
        {"app": "Hatch Sleep", "week_label": "Q2_start", "metric": "weekly_revenue_usd", "value": 239000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "Hatch Sleep", "week_label": "Q2_end", "metric": "weekly_revenue_usd", "value": 258000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "Hatch Sleep", "week_label": "Q2_start", "metric": "weekly_downloads", "value": 22000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "Hatch Sleep", "week_label": "Q2_end", "metric": "weekly_downloads", "value": 22000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "Hatch Sleep", "week_label": "Q2_start", "metric": "weekly_active_users", "value": 948000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "Hatch Sleep", "week_label": "Q2_end", "metric": "weekly_active_users", "value": 963000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        # BetterSleep
        {"app": "BetterSleep", "week_label": "Q2_start", "metric": "weekly_revenue_usd", "value": 291000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "BetterSleep", "week_label": "Q2_end", "metric": "weekly_revenue_usd", "value": 166000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "BetterSleep", "week_label": "Q2_mid_june_spike", "metric": "weekly_downloads", "value": 207000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "BetterSleep", "week_label": "Q2_start", "metric": "weekly_active_users", "value": 711000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
        {"app": "BetterSleep", "week_label": "Q2_mid_june_peak", "metric": "weekly_active_users", "value": 917000, "geo": "US", "platform": "unified", "source_name": src, "source_url": url},
    ]
    write_csv(
        PROC / "app_sensor_tower_wellness_q2_2024.csv",
        rows,
        ["app", "week_label", "metric", "value", "geo", "platform", "source_name", "source_url"],
    )


def app_landscape_estimates() -> None:
    """Point estimates / published KPIs for sleep-field apps + category comps."""
    rows = [
        {
            "app": "Calm",
            "segment": "meditation_sleep_platform",
            "year": 2025,
            "downloads": 7_300_000,
            "downloads_note": "annual downloads 2025",
            "cumulative_downloads": 140_000_000,
            "mau_or_active": None,
            "active_note": "paid subscribers used as engagement proxy (not MAU)",
            "paid_subscribers": 3_500_000,
            "revenue_usd": 210_000_000,
            "revenue_note": "estimated annual revenue",
            "source_name": "Business of Apps — Calm (2026)",
            "source_url": "https://www.businessofapps.com/data/calm-statistics/",
        },
        {
            "app": "Headspace",
            "segment": "meditation_sleep_platform",
            "year": 2025,
            "downloads": 3_000_000,
            "downloads_note": "annual downloads 2025 (BoA series)",
            "cumulative_downloads": 85_000_000,
            "mau_or_active": None,
            "active_note": "paid subscribers used as engagement proxy (not MAU)",
            "paid_subscribers": 2_000_000,
            "revenue_usd": 140_000_000,
            "revenue_note": "estimated annual revenue",
            "source_name": "Business of Apps — Headspace (2026)",
            "source_url": "https://www.businessofapps.com/data/headspace-statistics/",
        },
        {
            "app": "Sleep Cycle",
            "segment": "sleep_tracker",
            "year": 2025,
            "downloads": None,
            "downloads_note": "company reports downloads declined in Q4 but no absolute figure",
            "cumulative_downloads": None,
            "mau_or_active": 768_000,
            "active_note": "paying users (not free MAU)",
            "paid_subscribers": 768_000,
            "revenue_usd": 23_607_524,  # 247879 tSEK / 10.5
            "revenue_note": "FY2025 net sales converted at 10.5 SEK/USD",
            "source_name": "Sleep Cycle Year-end Report 2025",
            "source_url": "https://storage.mfn.se/79dd61f8-4ccc-4bc2-b095-feedaf3fced8/sleep-cycle-year-end-report-2025.pdf",
        },
        {
            "app": "BetterSleep",
            "segment": "sleep_sounds",
            "year": 2024,
            "downloads": None,
            "downloads_note": "US weekly downloads spiked to 207k mid-June 2024 (Sensor Tower)",
            "cumulative_downloads": None,
            "mau_or_active": 917_000,
            "active_note": "US weekly active users peak mid-June 2024 (not global MAU)",
            "paid_subscribers": None,
            "revenue_usd": None,
            "revenue_note": "US weekly revenue $166k–$291k in Q2 2024 => rough annualized US ~$9–15M if sustained (illustrative)",
            "source_name": "Sensor Tower Q2 2024 Wellness (US unified)",
            "source_url": "https://sensortower.com/blog/2024-q2-unified-top-5-wellness%20apps-revenue-us-63e274e1e1714cfff10eaa2f",
        },
        {
            "app": "ShutEye",
            "segment": "sleep_sounds_tracker",
            "year": 2024,
            "downloads": None,
            "downloads_note": "US weekly downloads 70k–183k in Q2 2024",
            "cumulative_downloads": None,
            "mau_or_active": 382_000,
            "active_note": "US WAU Q2 start 2024; AppGoblin cites ~1.3M MAU estimate later",
            "paid_subscribers": None,
            "revenue_usd": None,
            "revenue_note": "US weekly revenue $186k–$377k Q2 2024; AppGoblin ~$10k+/mo estimate is storefront-modelled and far lower — treat as uncertain",
            "source_name": "Sensor Tower Q2 2024 + AppGoblin",
            "source_url": "https://sensortower.com/blog/2024-q2-unified-top-5-wellness%20apps-revenue-us-63e274e1e1714cfff10eaa2f",
        },
        {
            "app": "Hatch Sleep",
            "segment": "sleep_hardware_app",
            "year": 2024,
            "downloads": None,
            "downloads_note": "US weekly downloads ~22k stable Q2 2024",
            "cumulative_downloads": None,
            "mau_or_active": 963_000,
            "active_note": "US WAU Q2 end 2024",
            "paid_subscribers": None,
            "revenue_usd": None,
            "revenue_note": "US weekly revenue ~$239k–$258k Q2 2024",
            "source_name": "Sensor Tower Q2 2024 Wellness (US unified)",
            "source_url": "https://sensortower.com/blog/2024-q2-unified-top-5-wellness%20apps-revenue-us-63e274e1e1714cfff10eaa2f",
        },
        {
            "app": "White Noise Deep Sleep Sounds",
            "segment": "white_noise",
            "year": 2026,
            "downloads": None,
            "downloads_note": "not disclosed; iOS ratings ~202k used as engagement proxy in scrapers",
            "cumulative_downloads": None,
            "mau_or_active": None,
            "active_note": "unavailable",
            "paid_subscribers": None,
            "revenue_usd": 36_000,  # ~$3k/mo * 12 from bumetric iOS estimate
            "revenue_note": "bumetric ML estimate ~$3k/mo iOS (~$36k/yr); Android separate ~$855/mo",
            "source_name": "bumetric — White Noise Deep Sleep Sounds / Slumber Studios",
            "source_url": "https://bumetric.com/revenue/white-noise-deep-sleep-sounds",
        },
    ]
    write_csv(
        PROC / "app_landscape_point_estimates.csv",
        rows,
        [
            "app", "segment", "year", "downloads", "downloads_note",
            "cumulative_downloads", "mau_or_active", "active_note",
            "paid_subscribers", "revenue_usd", "revenue_note",
            "source_name", "source_url",
        ],
    )


def market_size_tables() -> None:
    rows = [
        {
            "market": "Spiritual wellness apps (global)",
            "year": 2024,
            "value_usd_bn": 2.16,
            "notes": "Grand View Research market size",
            "source_name": "Grand View Research — Spiritual Wellness Apps Market",
            "source_url": "https://www.grandviewresearch.com/industry-analysis/spiritual-wellness-apps-market-report",
        },
        {
            "market": "Spiritual wellness apps (global)",
            "year": 2025,
            "value_usd_bn": 2.45,
            "notes": "projected",
            "source_name": "Grand View Research — Spiritual Wellness Apps Market",
            "source_url": "https://www.grandviewresearch.com/industry-analysis/spiritual-wellness-apps-market-report",
        },
        {
            "market": "Spiritual wellness apps (global)",
            "year": 2033,
            "value_usd_bn": 7.31,
            "notes": "projected; CAGR 14.63% 2025–2033",
            "source_name": "Grand View Research — Spiritual Wellness Apps Market",
            "source_url": "https://www.grandviewresearch.com/industry-analysis/spiritual-wellness-apps-market-report",
        },
        {
            "market": "Meditation & mindfulness apps share of spiritual wellness",
            "year": 2024,
            "value_usd_bn": round(2.16 * 0.4214, 3),
            "notes": "42.14% revenue share of spiritual wellness apps",
            "source_name": "Grand View Research — Spiritual Wellness Apps Market",
            "source_url": "https://www.grandviewresearch.com/industry-analysis/spiritual-wellness-apps-market-report",
        },
        {
            "market": "Health & Fitness apps global IAP revenue",
            "year": 2025,
            "value_usd_bn": 4.0,
            "notes": "Sensor Tower outlook: H&F to fly past $4B global IAP in 2025",
            "source_name": "Sensor Tower — State of Mobile Health & Fitness Apps 2025",
            "source_url": "https://sensortower.com/blog/state-of-mobile-health-and-fitness-in-2025",
        },
        {
            "market": "Health & Fitness apps global downloads",
            "year": 2024,
            "value_usd_bn": 3.6,  # stored as billions of downloads in value field with note
            "notes": "3.6 billion downloads (value_usd_bn column reused as billions of units)",
            "source_name": "Sensor Tower — State of Mobile Health & Fitness Apps 2025",
            "source_url": "https://sensortower.com/blog/state-of-mobile-health-and-fitness-in-2025",
        },
    ]
    write_csv(
        PROC / "market_size.csv",
        rows,
        ["market", "year", "value_usd_bn", "notes", "source_name", "source_url"],
    )


def youtube_cpm_by_niche() -> None:
    # LensPOV 2026 CPM audit (n=142 disclosures, 30 niches). Ambient sleep is
    # separately sourced from NicheTracker ($2–$6, avg $3).
    lens = "LensPOV Research — YouTube CPM by Niche 2026"
    lens_url = "https://lenspov.com/research/youtube-cpm-by-niche-2026/"
    rows = [
        {"niche": "Insurance", "cpm_low": 20, "cpm_median": 31, "cpm_high": 55, "rpm_equiv": 17.05, "n": 3, "source_name": lens, "source_url": lens_url},
        {"niche": "Personal Finance", "cpm_low": 18, "cpm_median": 29.3, "cpm_high": 50, "rpm_equiv": 16.12, "n": 7, "source_name": lens, "source_url": lens_url},
        {"niche": "Education / Tutorials", "cpm_low": 5, "cpm_median": 8.5, "cpm_high": 14, "rpm_equiv": 4.68, "n": 5, "source_name": lens, "source_url": lens_url},
        {"niche": "Fitness", "cpm_low": 3, "cpm_median": 5.5, "cpm_high": 10, "rpm_equiv": 3.03, "n": 5, "source_name": lens, "source_url": lens_url},
        {"niche": "Gaming", "cpm_low": 1.8, "cpm_median": 3.4, "cpm_high": 6.5, "rpm_equiv": 1.87, "n": 8, "source_name": lens, "source_url": lens_url},
        {"niche": "Music", "cpm_low": 1.2, "cpm_median": 2.4, "cpm_high": 4.5, "rpm_equiv": 1.32, "n": 5, "source_name": lens, "source_url": lens_url},
        {"niche": "ASMR", "cpm_low": 1.0, "cpm_median": 2.0, "cpm_high": 4.0, "rpm_equiv": 1.10, "n": 3, "source_name": lens, "source_url": lens_url},
        {"niche": "Kids Content (post-COPPA)", "cpm_low": 0.4, "cpm_median": 0.7, "cpm_high": 1.2, "rpm_equiv": 0.39, "n": 6, "source_name": lens, "source_url": lens_url},
        {
            "niche": "Ambient & Sleep Soundscapes",
            "cpm_low": 2.0,
            "cpm_median": 3.0,
            "cpm_high": 6.0,
            "rpm_equiv": 1.65,  # 3.0 * 0.55
            "n": None,
            "source_name": "NicheTracker — Ambient & Sleep Soundscapes (June 2026 review; CPM est. from vidIQ/Miraflow)",
            "source_url": "https://nichetracker.live/niche/ambient-sleep-sounds",
        },
        {
            "niche": "Sleep / ASMR (creator RPM guide)",
            "cpm_low": None,
            "cpm_median": None,
            "cpm_high": None,
            "rpm_equiv": 2.75,  # midpoint of $1.50–$4 RPM
            "n": None,
            "source_name": "Leaxor — How Sleep Restore Channels Make Videos & Earn (2026)",
            "source_url": "https://leaxor.com/creators/sleep-restore",
        },
    ]
    # Store RPM range notes for sleep guide separately via median field already.
    write_csv(
        PROC / "youtube_cpm_by_niche.csv",
        rows,
        ["niche", "cpm_low", "cpm_median", "cpm_high", "rpm_equiv", "n", "source_name", "source_url"],
    )


def youtube_channel_seed_stats() -> None:
    """Seed / fallback channel stats captured during research (July 2026).

    Primary live scrape overwrites via fetch_youtube_channels.py; this file
    preserves cited third-party snapshots used in narrative comparisons.
    """
    rows = [
        {
            "name": "Soothing Relaxation",
            "handle": "soothingrelaxation",
            "subscribers": 12_000_000,
            "total_views": 5_010_000_000,
            "monthly_views": 24_580_000,
            "est_monthly_earnings_usd": 27300,
            "est_per_video_usd": 9100,
            "country": "Norway",
            "source_name": "vidIQ public channel stats",
            "source_url": "https://vidiq.com/youtube-stats/channel/@soothingrelaxation/",
            "retrieved": "2026-07-26",
        },
        {
            "name": "Yellow Brick Cinema - Relaxing Music",
            "handle": "yellowbrickcinema",
            "subscribers": 6_460_000,
            "total_views": 2_660_000_000,
            "monthly_views": 4_710_000,
            "est_monthly_earnings_usd": 19300,
            "est_per_video_usd": 1380,
            "country": "United States",
            "source_name": "vidIQ public channel stats",
            "source_url": "https://vidiq.com/youtube-stats/channel/@yellowbrickcinema/",
            "retrieved": "2026-07-26",
        },
        {
            "name": "Meditative Mind",
            "handle": "meditativemind",
            "subscribers": 6_460_000,
            "total_views": 1_770_000_000,
            "monthly_views": 12_350_000,
            "est_monthly_earnings_usd": 4170,
            "est_per_video_usd": 521,
            "country": "Australia",
            "source_name": "vidIQ public channel stats",
            "source_url": "https://vidiq.com/youtube-stats/channel/@meditativemind/",
            "retrieved": "2026-07-26",
        },
        {
            "name": "Relaxing White Noise",
            "handle": "relaxingwhitenoise",
            "subscribers": 4_480_000,
            "total_views": 2_720_000_000,
            "monthly_views": 30_300_000,
            "est_monthly_earnings_usd": 103150,
            "est_per_video_usd": 6070,
            "country": "United States",
            "source_name": "vidIQ public channel stats",
            "source_url": "https://vidiq.com/youtube-stats/channel/@relaxingwhitenoise/",
            "retrieved": "2026-07-26",
        },
        {
            "name": "Relaxing White Noise (SpeakRJ snapshot)",
            "handle": "relaxingwhitenoise",
            "subscribers": 4_480_000,
            "total_views": 2_716_455_160,
            "monthly_views": None,
            "est_monthly_earnings_usd": None,
            "est_per_video_usd": None,
            "country": "US",
            "source_name": "SPEAKRJ Stats — Relaxing White Noise",
            "source_url": "https://www.speakrj.com/audit/report/UCbunYN0o9Yaid7zHaor_UHA/youtube",
            "retrieved": "2026-07-21",
        },
    ]
    write_csv(
        PROC / "youtube_channel_seed_stats.csv",
        rows,
        [
            "name", "handle", "subscribers", "total_views", "monthly_views",
            "est_monthly_earnings_usd", "est_per_video_usd", "country",
            "source_name", "source_url", "retrieved",
        ],
    )


def category_comparison_apps() -> None:
    """Published revenue anchors for non-sleep categories (comparison)."""
    rows = [
        {
            "app": "Calm",
            "category": "sleep_meditation",
            "year": 2025,
            "revenue_usd_mm": 210,
            "source_name": "Business of Apps — Calm (2026)",
            "source_url": "https://www.businessofapps.com/data/calm-statistics/",
        },
        {
            "app": "Headspace",
            "category": "sleep_meditation",
            "year": 2025,
            "revenue_usd_mm": 140,
            "source_name": "Business of Apps — Headspace (2026)",
            "source_url": "https://www.businessofapps.com/data/headspace-statistics/",
        },
        {
            "app": "Sleep Cycle",
            "category": "sleep_tracker",
            "year": 2025,
            "revenue_usd_mm": 23.61,
            "source_name": "Sleep Cycle YE 2025 (SEK→USD @10.5)",
            "source_url": "https://storage.mfn.se/79dd61f8-4ccc-4bc2-b095-feedaf3fced8/sleep-cycle-year-end-report-2025.pdf",
        },
        {
            "app": "Health & Fitness category IAP (global)",
            "category": "health_fitness_category",
            "year": 2025,
            "revenue_usd_mm": 4000,
            "source_name": "Sensor Tower — State of Mobile H&F 2025",
            "source_url": "https://sensortower.com/blog/state-of-mobile-health-and-fitness-in-2025",
        },
        {
            "app": "Spiritual wellness apps market",
            "category": "spiritual_wellness_market",
            "year": 2025,
            "revenue_usd_mm": 2450,
            "source_name": "Grand View Research",
            "source_url": "https://www.grandviewresearch.com/industry-analysis/spiritual-wellness-apps-market-report",
        },
    ]
    write_csv(
        PROC / "app_category_revenue_comparison.csv",
        rows,
        ["app", "category", "year", "revenue_usd_mm", "source_name", "source_url"],
    )


def main() -> None:
    calm_headspace_timeseries()
    sleep_cycle_kpis()
    sensor_tower_wellness_q2_2024()
    app_landscape_estimates()
    market_size_tables()
    youtube_cpm_by_niche()
    youtube_channel_seed_stats()
    category_comparison_apps()


if __name__ == "__main__":
    main()
