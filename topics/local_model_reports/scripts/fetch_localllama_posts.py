#!/usr/bin/env python3
"""Fetch r/LocalLLaMA posts via the Arctic Shift archive API.

Reddit.com often blocks direct scrapes / unauthenticated JSON. This script
pages through https://arctic-shift.photon-reddit.com for a date window and
prints (or writes) New Model / high-engagement threads.

Example (the window used for the May–Jul 2026 summary):

    python3 fetch_localllama_posts.py \\
        --after 2026-05-16 --before 2026-07-17 \\
        --new-model-only --min-score 100 \\
        --out posts.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Iterable

API_BASE = "https://arctic-shift.photon-reddit.com/api/posts"
DEFAULT_UA = "localllama-research/1.0 (+https://github.com/pomodorozhong/rabbit-holes)"


def parse_date(value: str) -> int:
    """Parse YYYY-MM-DD (UTC midnight) or a unix epoch int into epoch seconds."""
    value = value.strip()
    if value.isdigit():
        return int(value)
    dt = datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def api_get(path: str, params: dict[str, Any], timeout: float = 90.0) -> Any:
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = f"{API_BASE}{path}?{query}"
    req = urllib.request.Request(url, headers={"User-Agent": DEFAULT_UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode())
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    return data


def fetch_posts_page(
    *,
    subreddit: str,
    after: int,
    before: int,
    limit: int = 100,
) -> list[dict[str, Any]]:
    result = api_get(
        "/search",
        {
            "subreddit": subreddit,
            "after": after,
            "before": before,
            "limit": limit,
            "sort": "desc",
        },
    )
    if not isinstance(result, list):
        return []
    return result


def fetch_post_by_id(post_id: str) -> dict[str, Any] | None:
    result = api_get("/ids", {"ids": post_id})
    if isinstance(result, list) and result:
        return result[0]
    return None


def iter_posts(
    *,
    subreddit: str,
    after: int,
    before: int,
    page_limit: int = 100,
    max_pages: int = 40,
    sleep_s: float = 0.2,
) -> Iterable[dict[str, Any]]:
    """Page backwards through [after, before) by moving the `before` cursor."""
    cursor_before = before
    seen: set[str] = set()

    for page in range(max_pages):
        try:
            posts = fetch_posts_page(
                subreddit=subreddit,
                after=after,
                before=cursor_before,
                limit=page_limit,
            )
        except urllib.error.HTTPError as exc:
            print(f"HTTP {exc.code} on page {page}: {exc.reason}", file=sys.stderr)
            break
        except urllib.error.URLError as exc:
            print(f"Network error on page {page}: {exc.reason}", file=sys.stderr)
            break

        if not posts:
            print(f"page {page}: empty — done", file=sys.stderr)
            break

        oldest = min(p.get("created_utc") or 0 for p in posts)
        newest = max(p.get("created_utc") or 0 for p in posts)
        print(
            f"page {page}: {len(posts)} posts "
            f"{datetime.fromtimestamp(oldest, tz=timezone.utc).date()} "
            f".. {datetime.fromtimestamp(newest, tz=timezone.utc).date()}",
            file=sys.stderr,
        )

        new_on_page = 0
        for post in posts:
            pid = post.get("id")
            if not pid or pid in seen:
                continue
            seen.add(pid)
            new_on_page += 1
            yield post

        if oldest >= cursor_before or oldest <= after:
            print("page cursor stuck — stopping", file=sys.stderr)
            break
        if new_on_page == 0:
            print("no new posts on page — stopping", file=sys.stderr)
            break

        cursor_before = oldest
        if sleep_s:
            time.sleep(sleep_s)


def format_row(post: dict[str, Any]) -> str:
    created = post.get("created_utc") or 0
    dt = datetime.fromtimestamp(created, tz=timezone.utc).strftime("%Y-%m-%d")
    flair = post.get("link_flair_text") or "-"
    score = post.get("score") or 0
    comments = post.get("num_comments") or 0
    title = (post.get("title") or "").replace("\n", " ")
    permalink = post.get("permalink") or ""
    return f"[{score}] {dt} | {comments}c | [{flair}] {title}\n  https://reddit.com{permalink}"


def matches_filters(
    post: dict[str, Any],
    *,
    new_model_only: bool,
    min_score: int,
    keywords: list[str],
) -> bool:
    if new_model_only and (post.get("link_flair_text") or "") != "New Model":
        return False
    if (post.get("score") or 0) < min_score:
        return False
    if keywords:
        hay = f"{post.get('title') or ''}\n{post.get('selftext') or ''}".lower()
        if not any(k.lower() in hay for k in keywords):
            return False
    return True


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--subreddit", default="LocalLLaMA")
    p.add_argument("--after", required=True, help="Start date YYYY-MM-DD (UTC) or epoch")
    p.add_argument("--before", required=True, help="End date YYYY-MM-DD (UTC, exclusive-ish) or epoch")
    p.add_argument("--max-pages", type=int, default=40)
    p.add_argument("--page-limit", type=int, default=100, help="API page size (max typically 100)")
    p.add_argument("--sleep", type=float, default=0.2, help="Seconds between pages")
    p.add_argument("--new-model-only", action="store_true", help="Keep link_flair_text == 'New Model'")
    p.add_argument("--min-score", type=int, default=0)
    p.add_argument(
        "--keyword",
        action="append",
        default=[],
        help="Case-insensitive title/selftext filter; repeatable (OR)",
    )
    p.add_argument("--ids", nargs="+", help="Fetch specific Reddit post IDs instead of paging")
    p.add_argument("--out", help="Write matching posts as JSONL (full API payloads)")
    p.add_argument("--top", type=int, default=50, help="How many top matches to print (0 = all)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    after = parse_date(args.after)
    before = parse_date(args.before)

    if args.ids:
        posts = []
        for pid in args.ids:
            post = fetch_post_by_id(pid.removeprefix("t3_"))
            if post:
                posts.append(post)
            else:
                print(f"missing id: {pid}", file=sys.stderr)
    else:
        posts = list(
            iter_posts(
                subreddit=args.subreddit,
                after=after,
                before=before,
                page_limit=args.page_limit,
                max_pages=args.max_pages,
                sleep_s=args.sleep,
            )
        )

    matched = [
        post
        for post in posts
        if matches_filters(
            post,
            new_model_only=args.new_model_only,
            min_score=args.min_score,
            keywords=args.keyword,
        )
    ]
    matched.sort(key=lambda p: p.get("score") or 0, reverse=True)

    print(
        f"collected={len(posts)} matched={len(matched)} "
        f"window={args.after}..{args.before} subreddit={args.subreddit}",
        file=sys.stderr,
    )

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            for post in matched:
                fh.write(json.dumps(post, ensure_ascii=False) + "\n")
        print(f"wrote {len(matched)} posts -> {args.out}", file=sys.stderr)

    to_print = matched if args.top <= 0 else matched[: args.top]
    for post in to_print:
        print(format_row(post))
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
