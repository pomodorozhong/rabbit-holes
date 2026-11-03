#!/usr/bin/env python3
"""Fetch public app-store signals for sleep / white-noise apps.

Collectors:
  1. iTunes Lookup API (official, free) -> ratings, price, genre, current version
  2. Google Play store HTML scrape     -> rating count / approximate install band
  3. Writes curated + live signals into data/raw and data/processed

Note: Exact download counts / MAU / revenue are not public for most apps.
Those come from curated published sources (Business of Apps, Sensor Tower blogs,
Sleep Cycle annual report) via build_curated_datasets.py. This script gathers
what is reproducibly scrapable from public storefronts.
"""

from __future__ import annotations

import csv
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROC.mkdir(parents=True, exist_ok=True)

# App universe — package IDs / Apple IDs verified against public storefronts.
APPS: list[dict[str, Any]] = [
    {
        "name": "Calm",
        "segment": "meditation_sleep_platform",
        "ios_id": 571800810,
        "android_package": "com.calm.android",
        "publisher": "Calm.com, Inc.",
    },
    {
        "name": "Headspace",
        "segment": "meditation_sleep_platform",
        "ios_id": 493145008,
        "android_package": "com.getsomeheadspace.android",
        "publisher": "Headspace Inc.",
    },
    {
        "name": "BetterSleep",
        "segment": "sleep_sounds",
        "ios_id": 314498713,
        "android_package": "com.bettersleep.app",
        "publisher": "Ipnos Software Inc.",
    },
    {
        "name": "Sleep Cycle",
        "segment": "sleep_tracker",
        "ios_id": 320606217,
        "android_package": "com.northcube.sleepcycle",
        "publisher": "Sleep Cycle AB",
    },
    {
        "name": "ShutEye",
        "segment": "sleep_sounds_tracker",
        "ios_id": 1490078804,
        "android_package": "com.sleepmonitor.aio",
        "publisher": "Enerjoy Pte. Ltd.",
    },
    {
        "name": "White Noise Deep Sleep Sounds",
        "segment": "white_noise",
        "ios_id": 1083248251,
        "android_package": "com.kitefaster.MagicBabySleeperFree",
        "publisher": "Slumber Studios, LLC",
    },
    {
        "name": "Insight Timer",
        "segment": "meditation",
        "ios_id": 337472899,
        "android_package": "com.spotlightsix.zentimerlite2",
        "publisher": "Insight Network Inc.",
    },
    {
        "name": "myNoise",
        "segment": "noise_generator",
        "ios_id": 1523675125,
        "android_package": "net.mynoise.player",
        "publisher": "myNoise BVBA",
    },
    {
        "name": "Noisli",
        "segment": "noise_generator",
        "ios_id": 862773459,
        "android_package": "com.noisli.noisli",
        "publisher": "Noisli Labs UG",
    },
    {
        "name": "Endel",
        "segment": "adaptive_soundscapes",
        "ios_id": 1346247457,
        "android_package": "com.endel.endel",
        "publisher": "Endel",
    },
    {
        "name": "White Noise Lite (TMSOFT)",
        "segment": "white_noise",
        "ios_id": 292987597,
        "android_package": "com.tmsoft.whitenoise.lite",
        "publisher": "TMSOFT",
    },
]

# Category comparison apps (fitness / entertainment) for relative context.
COMPARISON_APPS: list[dict[str, Any]] = [
    {
        "name": "Strava",
        "segment": "fitness_tracking",
        "ios_id": 426826309,
        "android_package": "com.strava",
        "publisher": "Strava Inc.",
        "comparison_category": "fitness",
    },
    {
        "name": "MyFitnessPal",
        "segment": "nutrition",
        "ios_id": 341232718,
        "android_package": "com.myfitnesspal.android",
        "publisher": "MyFitnessPal, Inc.",
        "comparison_category": "fitness",
    },
    {
        "name": "Spotify",
        "segment": "music_streaming",
        "ios_id": 324684580,
        "android_package": "com.spotify.music",
        "publisher": "Spotify AB",
        "comparison_category": "entertainment",
    },
    {
        "name": "Duolingo",
        "segment": "education",
        "ios_id": 570060128,
        "android_package": "com.duolingo",
        "publisher": "Duolingo",
        "comparison_category": "education",
    },
]

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
)


def itunes_lookup(app_id: int) -> dict[str, Any]:
    url = f"https://itunes.apple.com/lookup?id={app_id}&country=us"
    r = SESSION.get(url, timeout=30)
    r.raise_for_status()
    payload = r.json()
    results = payload.get("results") or []
    if not results:
        return {"source": "itunes_lookup", "source_url": url, "error": "empty"}
    item = results[0]
    return {
        "source": "itunes_lookup",
        "source_url": url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "track_name": item.get("trackName"),
        "bundle_id": item.get("bundleId"),
        "artist_name": item.get("artistName"),
        "average_user_rating": item.get("averageUserRating"),
        "user_rating_count": item.get("userRatingCount"),
        "price": item.get("price"),
        "formatted_price": item.get("formattedPrice"),
        "primary_genre": item.get("primaryGenreName"),
        "genres": item.get("genres"),
        "version": item.get("version"),
        "release_date": item.get("releaseDate"),
        "current_version_release_date": item.get("currentVersionReleaseDate"),
        "minimum_os_version": item.get("minimumOsVersion"),
        "content_advisory_rating": item.get("contentAdvisoryRating"),
        "track_view_url": item.get("trackViewUrl"),
        "description_excerpt": (item.get("description") or "")[:280],
    }


def play_store_signals(package: str) -> dict[str, Any]:
    url = f"https://play.google.com/store/apps/details?id={package}&hl=en_US&gl=US"
    out: dict[str, Any] = {
        "source": "google_play_html",
        "source_url": url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "package": package,
    }
    try:
        r = SESSION.get(url, timeout=45)
        out["http_status"] = r.status_code
        if r.status_code != 200:
            out["error"] = f"HTTP {r.status_code}"
            return out
        html = r.text
    except Exception as exc:  # noqa: BLE001
        out["error"] = str(exc)
        return out

    # Install band e.g. "10M+", "5M+", "100,000+"
    m = re.search(r'">([\d,]+[+]?(?:\s*[KkMmBb]\+?)?)</div><div[^>]*>Downloads</div>', html)
    if not m:
        m = re.search(r'([\d,]+(?:\+|M\+|K\+|B\+)?)</span>\s*<span[^>]*>Downloads', html, re.I)
    if not m:
        m = re.search(r'"([\d,]+(?:\+|M\+|K\+|B\+)?)\s*downloads"', html, re.I)
    if not m:
        # Newer Play markup often embeds install ranges near "downloads"
        m = re.search(
            r'([0-9][0-9,]*(?:\+|M\+|K\+|B\+)?|[0-9]+[KkMmBb]\+)\s*(?=downloads|Downloads)',
            html,
        )
    if m:
        out["downloads_text"] = m.group(1).strip()

    m = re.search(r'"ratingValue"\s*:\s*"?([\d.]+)"?', html)
    if m:
        out["rating"] = float(m.group(1))
    m = re.search(r'"ratingCount"\s*:\s*"?([\d,]+)"?', html)
    if m:
        out["rating_count"] = int(m.group(1).replace(",", ""))

    # Another common pattern: aria/content snippets
    m = re.search(r'aria-label="([\d.]+) stars? out of five stars?"', html, re.I)
    if m and "rating" not in out:
        out["rating"] = float(m.group(1))
    m = re.search(r'aria-label="([\d,]+) ratings?"', html, re.I)
    if m and "rating_count" not in out:
        out["rating_count"] = int(m.group(1).replace(",", ""))

    # Install band alternative from AF_initDataCallback blobs
    if "downloads_text" not in out:
        m = re.search(r'\["(10M\+|5M\+|1M\+|500K\+|100K\+|50K\+|10K\+|5K\+|1K\+|100\+)"\]', html)
        if m:
            out["downloads_text"] = m.group(1)

    return out


def main() -> None:
    rows: list[dict[str, Any]] = []
    universe = APPS + COMPARISON_APPS

    for app in universe:
        print(f"[itunes] {app['name']} ({app['ios_id']})")
        try:
            ios = itunes_lookup(int(app["ios_id"]))
        except Exception as exc:  # noqa: BLE001
            ios = {"error": str(exc), "source": "itunes_lookup"}
        time.sleep(0.4)

        pkg = app.get("android_package")
        print(f"[play]   {app['name']} ({pkg})")
        try:
            play = play_store_signals(pkg) if pkg else {"error": "no package"}
        except Exception as exc:  # noqa: BLE001
            play = {"error": str(exc), "source": "google_play_html"}
        time.sleep(0.6)

        rows.append(
            {
                **app,
                **{f"ios_{k}": v for k, v in ios.items()},
                **{f"play_{k}": v for k, v in play.items()},
            }
        )

    raw_path = RAW / "app_store_signals_raw.json"
    raw_path.write_text(
        json.dumps(
            {"scraped_at": datetime.now(timezone.utc).isoformat(), "apps": rows},
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {raw_path}")

    fields = [
        "name",
        "segment",
        "publisher",
        "comparison_category",
        "ios_id",
        "android_package",
        "ios_track_name",
        "ios_average_user_rating",
        "ios_user_rating_count",
        "ios_price",
        "ios_primary_genre",
        "ios_track_view_url",
        "play_downloads_text",
        "play_rating",
        "play_rating_count",
        "play_source_url",
        "ios_source_url",
    ]
    csv_path = PROC / "app_store_signals.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()
