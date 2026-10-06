"""Persist scanned jobs to data/jobs.json (the dashboard reads this).

The daily GitHub Action calls merge_and_save() and commits the file back to the
repo. Jobs are keyed by URL, refreshed each run, and pruned after KEEP_DAYS so
the dashboard shows a rolling window of recent openings (not just today's).
"""
from __future__ import annotations

import datetime as dt
import json
import os

from .sources import Job

KEEP_DAYS = int(os.environ.get("JOBS_KEEP_DAYS", "30"))


def _today() -> str:
    return dt.date.today().isoformat()


def load_jobs(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}
    return {j["url"]: j for j in data.get("jobs", []) if j.get("url")}


def job_to_dict(j: Job) -> dict:
    return {
        "url": j.url, "title": j.title, "company": j.company,
        "location": j.location, "source": j.source, "posted": j.posted,
        "score": j.score, "experience_req": j.experience_req,
        "exp_years": j.exp_years, "tier": j.tier,
        "target_priority": j.target_priority,
        "resume": j.resume, "resume_path": j.resume_path,
        "matched": list(j.matched or [])[:8],
    }


def merge_and_save(path: str, jobs: list[Job]) -> int:
    """Merge today's jobs into the rolling store and write it. Returns count."""
    existing = load_jobs(path)
    today = _today()
    for j in jobs:
        d = job_to_dict(j)
        if j.url in existing:
            existing[j.url].update(d)          # refresh, keep first_seen + emailed
        else:
            d["first_seen"] = today
            existing[j.url] = d

    cutoff = (dt.date.today() - dt.timedelta(days=KEEP_DAYS)).isoformat()
    kept = {u: e for u, e in existing.items()
            if e.get("first_seen", today) >= cutoff}

    out = {
        "updated": dt.datetime.now().isoformat(timespec="seconds"),
        "jobs": sorted(kept.values(), key=lambda e: -e.get("score", 0)),
    }
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    return len(kept)


def mark_emailed(path: str, urls: list[str]) -> None:
    """Flag these URLs as already emailed, so a later run never resends them.

    Called only after a successful send (see main.py) — if the send fails,
    these stay unmarked and get retried on the next run instead of silently
    being dropped from the email.
    """
    if not urls:
        return
    existing = load_jobs(path)
    for u in urls:
        if u in existing:
            existing[u]["emailed"] = True
    out = {
        "updated": dt.datetime.now().isoformat(timespec="seconds"),
        "jobs": sorted(existing.values(), key=lambda e: -e.get("score", 0)),
    }
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
