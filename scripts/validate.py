#!/usr/bin/env python3
"""Validate each entry's llms_txt URL resolves.

Exit code 0 if all "published"-status entries return 200. Exit code 1 if any
entry claims llms_txt_status=published but the URL is unreachable or 404.
Entries marked status=missing are skipped (expected to be broken).

Run from scripts/ or repo root:
    python3 scripts/validate.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

try:
    import yaml
    import requests
except ImportError:
    sys.exit("Missing deps. Install them: pip install pyyaml requests")


REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "entries"

USER_AGENT = "awesome-llms-txt-validator/1.0 (+https://github.com/brethofai/awesome-llms-txt)"
TIMEOUT = 10  # seconds
SLEEP_BETWEEN = 0.5  # be polite


def load_entries() -> list[dict]:
    entries = []
    for p in sorted(ENTRIES_DIR.glob("*.yaml")):
        with p.open() as f:
            d = yaml.safe_load(f) or {}
        d["_source_file"] = p.name
        entries.append(d)
    return entries


def check_url(url: str) -> tuple[int, str]:
    """Return (http_status_code, reason). -1 on connection error."""
    try:
        r = requests.get(url, timeout=TIMEOUT, allow_redirects=True,
                         headers={"User-Agent": USER_AGENT})
        return r.status_code, r.reason or ""
    except requests.exceptions.Timeout:
        return -1, "timeout"
    except requests.exceptions.ConnectionError as e:
        return -1, f"conn-err: {type(e).__name__}"
    except Exception as e:
        return -1, f"err: {type(e).__name__}"


def main() -> int:
    entries = load_entries()
    print(f"validating {len(entries)} entries")
    print()

    claimed_published = [e for e in entries if e.get("llms_txt_status") == "published"]
    claimed_missing = [e for e in entries if e.get("llms_txt_status") == "missing"]
    stubs = [e for e in entries if e.get("status") == "stub"]

    print(f"  claimed published: {len(claimed_published)}")
    print(f"  claimed missing:   {len(claimed_missing)}")
    print(f"  stubs:             {len(stubs)}")
    print()

    failures: list[tuple[dict, int, str]] = []
    unexpected_found: list[tuple[dict, int]] = []

    for e in claimed_published:
        url = e.get("llms_txt", "")
        if not url:
            failures.append((e, 0, "no llms_txt URL in entry"))
            continue
        code, reason = check_url(url)
        mark = "✓" if 200 <= code < 300 else "✗"
        print(f"  {mark} [{code:>4}] {e.get('name','?'):<30} {url}")
        if not (200 <= code < 300):
            failures.append((e, code, reason))
        time.sleep(SLEEP_BETWEEN)

    # Optional sanity: pick up to 10 claimed-missing and check if they
    # unexpectedly exist now. Good for the maintainer but not a hard fail.
    print()
    print("spot-checking 'missing' entries (free upgrade if any are now live)...")
    for e in claimed_missing[:10]:
        url = e.get("llms_txt", "")
        if not url:
            continue
        code, reason = check_url(url)
        mark = "!" if 200 <= code < 300 else "·"
        print(f"  {mark} [{code:>4}] {e.get('name','?'):<30} {url}")
        if 200 <= code < 300:
            unexpected_found.append((e, code))
        time.sleep(SLEEP_BETWEEN)

    print()
    print("=" * 60)
    if failures:
        print(f"FAIL — {len(failures)} published entries have broken llms.txt URLs:")
        for e, code, reason in failures:
            print(f"  - {e['_source_file']}: {e.get('name','?')}: "
                  f"HTTP {code} ({reason})")
        return 1
    else:
        print("OK — all published entries serve a working llms.txt.")
    if unexpected_found:
        print()
        print(f"FYI — {len(unexpected_found)} entries marked 'missing' but "
              f"actually serving llms.txt now:")
        for e, code in unexpected_found:
            print(f"  - {e['_source_file']}: {e.get('name','?')}")
        print("Consider a PR to flip their status to 'published'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
