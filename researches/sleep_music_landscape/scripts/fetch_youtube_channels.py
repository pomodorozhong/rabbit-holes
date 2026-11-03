#!/usr/bin/env python3
"""Fetch public YouTube + third-party stats for sleep/white-noise channels.

Reproducible collectors (no YouTube Data API key required):
  1. YouTube channel /about HTML  -> subscribers, views, video count, country
  2. vidIQ public channel pages   -> monthly views / earnings estimates
  3. NicheTracker ambient page    -> niche CPM / competition snapshot

Outputs (under data/raw/ and data/processed/):
  - youtube_channels_raw.json
  - youtube_channels.csv
  - youtube_videos_sample.csv   (top videos when available from vidIQ)
  - niche_ambient_snapshot.json
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

# Channel universe for the sleep / white-noise / ambient music niche.
# channel_id sourced from public YouTube URLs / SpeakRJ / channel pages.
CHANNELS: list[dict[str, str]] = [
    {
        "name": "Soothing Relaxation",
        "handle": "soothingrelaxation",
        "channel_id": "",
        "category": "sleep_music",
    },
    {
        "name": "Yellow Brick Cinema - Relaxing Music",
        "handle": "yellowbrickcinema",
        "channel_id": "UCwobzUc3z-0PrFpoRxNszXQ",
        "category": "sleep_music",
    },
    {
        "name": "Meditative Mind",
        "handle": "meditativemind",
        "channel_id": "",
        "category": "meditation_sleep",
    },
    {
        "name": "Relaxing White Noise",
        "handle": "relaxingwhitenoise",
        "channel_id": "UCbunYN0o9Yaid7zHaor_UHA",
        "category": "white_noise",
    },
    {
        "name": "Jason Stephenson - Guided Sleep Meditation",
        "handle": "jasonstephensonmeditation",
        "channel_id": "",
        "category": "sleep_meditation",
    },
    {
        "name": "The Honest Guys",
        "handle": "thehonestguys",
        "channel_id": "UCTDiRJp9MeAgZbmwmq4w4GA",
        "category": "guided_meditation",
    },
    {
        "name": "Michael Sealey",
        "handle": "michaelsealey",
        "channel_id": "",
        "category": "sleep_hypnosis",
    },
    {
        "name": "Nu Meditation Music",
        "handle": "numeditationmusic",
        "channel_id": "",
        "category": "meditation_music",
    },
    {
        "name": "MeditationRelaxClub",
        "handle": "meditationrelaxclub",
        "channel_id": "",
        "category": "sleep_music",
    },
    {
        "name": "Stardust Vibes - Relaxing Sounds",
        "handle": "stardustvibes",
        "channel_id": "",
        "category": "ambient_sounds",
    },
    {
        "name": "Greenred Productions - Relaxing Music",
        "handle": "greenredproductions",
        "channel_id": "",
        "category": "sleep_music",
    },
    {
        "name": "Calm",
        "handle": "calm",
        "channel_id": "",
        "category": "brand_sleep",
    },
    {
        "name": "Headspace",
        "handle": "headspace",
        "channel_id": "",
        "category": "brand_meditation",
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


def parse_count(text: str | None) -> int | None:
    """Parse strings like '6.46M subscribers', '2,656,109,637 views', '24.58M'."""
    if not text:
        return None
    s = text.strip().lower().replace(",", "")
    s = re.sub(r"(subscribers|views|videos|subscriber|view|video)", "", s).strip()
    m = re.search(r"([\d.]+)\s*([kmb])?", s)
    if not m:
        digits = re.sub(r"[^\d]", "", text)
        return int(digits) if digits else None
    value = float(m.group(1))
    suffix = (m.group(2) or "").lower()
    mult = {"": 1, "k": 1_000, "m": 1_000_000, "b": 1_000_000_000}[suffix]
    return int(value * mult)


def money_to_float(text: str | None) -> float | None:
    """Parse '$19.3K', '$103K', '$27K' style strings."""
    if not text:
        return None
    s = text.strip().upper().replace(",", "").replace("$", "")
    m = re.search(r"([\d.]+)\s*([KMB])?", s)
    if not m:
        return None
    value = float(m.group(1))
    suffix = m.group(2) or ""
    mult = {"": 1, "K": 1_000, "M": 1_000_000, "B": 1_000_000_000}[suffix]
    return value * mult


def resolve_handle(handle: str) -> dict[str, Any]:
    """Resolve @handle -> channel_id and basic about-page stats."""
    handle = handle.lstrip("@")
    url = f"https://www.youtube.com/@{handle}/about"
    r = SESSION.get(url, timeout=45)
    r.raise_for_status()
    html = r.text

    channel_id = None
    m = re.search(r'"channelId":"(UC[\w-]{22})"', html)
    if m:
        channel_id = m.group(1)
    else:
        m = re.search(r'"browseId":"(UC[\w-]{22})"', html)
        if m:
            channel_id = m.group(1)

    subs_text = None
    m = re.search(r'"subscriberCountText":"([^"]+)"', html)
    if m:
        subs_text = m.group(1)
    else:
        m = re.search(r'"content":"([\d.,]+[KkMmBb]?\s*subscribers)"', html)
        if m:
            subs_text = m.group(1)

    views_text = None
    m = re.search(r'"viewCountText":"([^"]+)"', html)
    if m:
        views_text = m.group(1)

    videos_text = None
    m = re.search(r'"content":"([\d.,]+[KkMm]?\s*videos)"', html)
    if m:
        videos_text = m.group(1)

    country = None
    m = re.search(r'"country":"([^"]+)"', html)
    if m:
        country = m.group(1)

    title = None
    m = re.search(r'"channelMetadataRenderer":\{"title":"([^"]+)"', html)
    if m:
        title = m.group(1)

    return {
        "source": "youtube_about_html",
        "source_url": url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "handle": handle,
        "channel_id": channel_id,
        "title": title,
        "subscribers_text": subs_text,
        "subscribers": parse_count(subs_text),
        "views_text": views_text,
        "total_views": parse_count(views_text),
        "videos_text": videos_text,
        "video_count": parse_count(videos_text),
        "country": country,
        "http_status": r.status_code,
    }


def fetch_vidiq(handle: str) -> dict[str, Any]:
    """Scrape public vidIQ channel stats page for monthly views / earnings."""
    handle = handle.lstrip("@")
    url = f"https://vidiq.com/youtube-stats/channel/@{handle}/"
    r = SESSION.get(url, timeout=45)
    out: dict[str, Any] = {
        "source": "vidiq_public",
        "source_url": url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "handle": handle,
        "http_status": r.status_code,
    }
    if r.status_code != 200:
        out["error"] = f"HTTP {r.status_code}"
        return out

    text = r.text

    # Subscribers / total views often appear near FAQ / hero.
    m = re.search(
        r"Subscribers</[^>]*>\s*<[^>]*>\s*([\d.]+[KkMmBb]?)",
        text,
        re.I | re.S,
    )
    # Fallback: FAQ style "got X views in the last month"
    month_views = None
    m = re.search(
        r"got\s+([\d.,]+\s*[KkMmBb]?)\s+views in the last (?:30 days|month)",
        text,
        re.I,
    )
    if m:
        month_views = parse_count(m.group(1))
        out["monthly_views_text"] = m.group(1)
        out["monthly_views"] = month_views

    m = re.search(
        r"estimated at\s*\$?\s*([\d.,]+\s*[KkMmBb]?)\s*monthly",
        text,
        re.I,
    )
    if m:
        out["est_monthly_earnings_text"] = m.group(1)
        out["est_monthly_earnings_usd"] = money_to_float(m.group(1))

    m = re.search(
        r"makes an estimated\s*\$?\s*([\d.,]+\s*[KkMmBb]?)\s*per video",
        text,
        re.I,
    )
    if m:
        out["est_per_video_earnings_text"] = m.group(1)
        out["est_per_video_earnings_usd"] = money_to_float(m.group(1))

    m = re.search(
        r"gained\s+([\d.,]+\s*[KkMmBb]?)\s+subscribers in the last (?:30 days|month)",
        text,
        re.I,
    )
    if not m:
        m = re.search(
            r"lost\s+([\d.,]+\s*[KkMmBb]?)\s+subscribers in the last (?:30 days|month)",
            text,
            re.I,
        )
        if m:
            out["monthly_sub_change"] = -1 * (parse_count(m.group(1)) or 0)
            out["monthly_sub_change_text"] = "-" + m.group(1)
    else:
        out["monthly_sub_change"] = parse_count(m.group(1))
        out["monthly_sub_change_text"] = m.group(1)

    m = re.search(r"Est\.\s*Monthly Earnings</[^>]*>\s*<[^>]*>\s*\$?([\d.]+[KkMmBb]?)", text, re.I | re.S)
    if m and "est_monthly_earnings_usd" not in out:
        out["est_monthly_earnings_text"] = m.group(1)
        out["est_monthly_earnings_usd"] = money_to_float(m.group(1))

    # Capture a few top video rows if present: title + view count in table.
    videos = []
    for vm in re.finditer(
        r'href="https://www\.youtube\.com/watch\?v=([\w-]{11})"[^>]*>\s*([^<]{5,180})</a>'
        r".{0,400}?([\d.,]+\s*[KkMmBb]?)",
        text,
        re.I | re.S,
    ):
        videos.append(
            {
                "video_id": vm.group(1),
                "title": re.sub(r"\s+", " ", vm.group(2)).strip(),
                "views": parse_count(vm.group(3)),
                "views_text": vm.group(3).strip(),
            }
        )
        if len(videos) >= 8:
            break
    out["top_videos"] = videos
    return out


def fetch_nichetracker_ambient() -> dict[str, Any]:
    url = "https://nichetracker.live/niche/ambient-sleep-sounds"
    r = SESSION.get(url, timeout=45)
    text = r.text
    out: dict[str, Any] = {
        "source": "nichetracker",
        "source_url": url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "http_status": r.status_code,
        "niche": "Ambient & Sleep Soundscapes",
    }
    def _first_float(pattern: str) -> float | None:
        m = re.search(pattern, text, re.I | re.S)
        if not m:
            return None
        return float(m.group(1).rstrip("."))

    out["avg_cpm_usd"] = _first_float(r"Average CPM.*?\$([\d.]+)")
    m = re.search(r"\$([\d.]+)\s*-\s*\$([\d.]+)", text)
    if m:
        out["cpm_low_usd"] = float(m.group(1).rstrip("."))
        out["cpm_high_usd"] = float(m.group(2).rstrip("."))
    out["competition_score"] = _first_float(r"([\d.]+)\s*/100")
    m = re.search(r"([\d,]+)\s*channels in niche", text, re.I)
    if m:
        out["active_channels"] = int(m.group(1).replace(",", ""))
    out["growth_pct"] = _first_float(r"\+([\d.]+)%")
    m = re.search(r"Search Volume.*?([\d.]+[KkMm]?)", text, re.I | re.S)
    if m:
        out["search_volume_text"] = m.group(1)
        out["search_volume"] = parse_count(m.group(1))
    return out


def estimate_revenue(
    monthly_views: int | None,
    rpm_low: float = 1.5,
    rpm_high: float = 4.0,
    rpm_mid: float = 3.0,
) -> dict[str, float | None]:
    """Creator take-home RPM (revenue per 1,000 views) estimate for sleep niche.

    Sleep/ambient RPM commonly cited ~$1.50–$4 (Leaxor, Fluxnote, NicheTracker
    ambient CPM $2–$6 with ~55% creator share => ~$1.1–$3.3 RPM).
    """
    if not monthly_views:
        return {
            "est_revenue_low_usd": None,
            "est_revenue_mid_usd": None,
            "est_revenue_high_usd": None,
            "rpm_low": rpm_low,
            "rpm_mid": rpm_mid,
            "rpm_high": rpm_high,
        }
    return {
        "est_revenue_low_usd": round(monthly_views / 1000 * rpm_low, 2),
        "est_revenue_mid_usd": round(monthly_views / 1000 * rpm_mid, 2),
        "est_revenue_high_usd": round(monthly_views / 1000 * rpm_high, 2),
        "rpm_low": rpm_low,
        "rpm_mid": rpm_mid,
        "rpm_high": rpm_high,
    }


def main() -> None:
    results: list[dict[str, Any]] = []
    video_rows: list[dict[str, Any]] = []

    for meta in CHANNELS:
        handle = meta["handle"]
        print(f"[youtube] @{handle} ...")
        try:
            yt = resolve_handle(handle)
        except Exception as exc:  # noqa: BLE001
            yt = {"handle": handle, "error": str(exc), "source": "youtube_about_html"}
        time.sleep(0.8)
        print(f"[vidiq]   @{handle} ...")
        try:
            vq = fetch_vidiq(handle)
        except Exception as exc:  # noqa: BLE001
            vq = {"handle": handle, "error": str(exc), "source": "vidiq_public"}
        time.sleep(0.8)

        monthly_views = vq.get("monthly_views")
        rev = estimate_revenue(monthly_views)

        row = {
            **meta,
            **{f"yt_{k}": v for k, v in yt.items() if k != "handle"},
            **{f"vidiq_{k}": v for k, v in vq.items() if k not in {"handle", "top_videos"}},
            **rev,
            # Prefer third-party monthly earnings if present, else RPM model.
            "est_monthly_ad_revenue_usd": vq.get("est_monthly_earnings_usd")
            or rev.get("est_revenue_mid_usd"),
        }
        results.append(row)

        for vid in vq.get("top_videos") or []:
            video_rows.append(
                {
                    "channel_handle": handle,
                    "channel_name": meta["name"],
                    "category": meta["category"],
                    **vid,
                    "source": "vidiq_public",
                    "source_url": vq.get("source_url"),
                }
            )

    niche = fetch_nichetracker_ambient()

    raw_payload = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "channels": results,
        "niche_snapshot": niche,
    }
    raw_path = RAW / "youtube_channels_raw.json"
    raw_path.write_text(json.dumps(raw_payload, indent=2), encoding="utf-8")
    print(f"Wrote {raw_path}")

    (RAW / "niche_ambient_snapshot.json").write_text(
        json.dumps(niche, indent=2), encoding="utf-8"
    )

    # Flatten CSV for analysis
    fieldnames = [
        "name",
        "handle",
        "category",
        "yt_channel_id",
        "yt_title",
        "yt_subscribers",
        "yt_total_views",
        "yt_video_count",
        "yt_country",
        "yt_source_url",
        "vidiq_monthly_views",
        "vidiq_est_monthly_earnings_usd",
        "vidiq_est_per_video_earnings_usd",
        "vidiq_monthly_sub_change",
        "vidiq_source_url",
        "est_revenue_low_usd",
        "est_revenue_mid_usd",
        "est_revenue_high_usd",
        "est_monthly_ad_revenue_usd",
        "rpm_low",
        "rpm_mid",
        "rpm_high",
    ]
    csv_path = PROC / "youtube_channels.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"Wrote {csv_path}")

    vpath = PROC / "youtube_videos_sample.csv"
    with vpath.open("w", newline="", encoding="utf-8") as f:
        fields = [
            "channel_handle",
            "channel_name",
            "category",
            "video_id",
            "title",
            "views",
            "views_text",
            "source",
            "source_url",
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(video_rows)
    print(f"Wrote {vpath} ({len(video_rows)} rows)")


if __name__ == "__main__":
    main()
