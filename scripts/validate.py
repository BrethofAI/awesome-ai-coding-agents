#!/usr/bin/env python3
"""Validate each entry's llms_txt URL resolves.

Exit code 0 if all "published"-status entries serve a working llms.txt. Exit
code 1 only if a published entry returns a definitive client error (4xx, e.g.
404/410 — the file was actually removed). Transient errors (timeouts, connection
errors, 5xx, 429) are retried, and if still failing are reported as warnings
WITHOUT failing the build — a momentary upstream hiccup (e.g. a Cloudflare 520)
shouldn't red the daily re-check. Entries marked status=missing are skipped.

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


# This script prints check marks and box glyphs. On Windows the default stdout
# codec is cp1252, which raises UnicodeEncodeError on them; force UTF-8 so the
# output is identical on Linux CI and a Windows shell.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "entries"

USER_AGENT = "awesome-llms-txt-validator/1.0 (+https://github.com/brethofai/awesome-llms-txt)"
TIMEOUT = 10  # seconds
SLEEP_BETWEEN = 0.5  # be polite
RETRIES = 3          # transient errors (timeout / conn / 5xx / 429) retried this many times
RETRY_BACKOFF = 2.0  # seconds, multiplied by the attempt number


def load_entries() -> list[dict]:
    entries = []
    for p in sorted(ENTRIES_DIR.glob("*.yaml")):
        with p.open(encoding="utf-8") as f:
            d = yaml.safe_load(f) or {}
        d["_source_file"] = p.name
        entries.append(d)
    return entries


def is_transient(code: int) -> bool:
    """A momentary error worth retrying and NOT worth failing the build over:
    connection errors (-1), rate limits (429), and any 5xx (incl. Cloudflare
    520-524). A definitive 4xx like 404/410 is NOT transient — the file is gone."""
    return code == -1 or code == 429 or 500 <= code < 600


def check_url(url: str) -> tuple[int, str]:
    """GET the URL, retrying transient errors up to RETRIES times. Returns the
    final (status_code, reason); -1 on connection error. Returns as soon as a
    definitive result is seen (2xx/3xx, or a non-429 4xx)."""
    code, reason = -1, "no attempt"
    for attempt in range(1, RETRIES + 1):
        try:
            r = requests.get(url, timeout=TIMEOUT, allow_redirects=True,
                             headers={"User-Agent": USER_AGENT})
            code, reason = r.status_code, (r.reason or "")
        except requests.exceptions.Timeout:
            code, reason = -1, "timeout"
        except requests.exceptions.ConnectionError as e:
            code, reason = -1, f"conn-err: {type(e).__name__}"
        except Exception as e:
            code, reason = -1, f"err: {type(e).__name__}"
        if not is_transient(code):
            return code, reason            # definitive — no point retrying
        if attempt < RETRIES:
            time.sleep(RETRY_BACKOFF * attempt)
    return code, reason                    # retries exhausted, still transient


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

    failures: list[tuple[dict, int, str]] = []   # hard: definitive 4xx / no URL
    flaky: list[tuple[dict, int, str]] = []       # soft: transient (5xx/429/conn)
    unexpected_found: list[tuple[dict, int]] = []

    for e in claimed_published:
        url = e.get("llms_txt", "")
        if not url:
            failures.append((e, 0, "no llms_txt URL in entry"))
            continue
        code, reason = check_url(url)
        ok = 200 <= code < 300
        mark = "✓" if ok else ("~" if is_transient(code) else "✗")
        print(f"  {mark} [{code:>4}] {e.get('name','?'):<30} {url}")
        if not ok:
            (flaky if is_transient(code) else failures).append((e, code, reason))
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
    if flaky:
        print(f"⚠ {len(flaky)} published entries had TRANSIENT errors after "
              f"{RETRIES} retries — NOT failing the build (re-checked daily):")
        for e, code, reason in flaky:
            print(f"  ::warning file=entries/{e['_source_file']}::{e.get('name','?')}: "
                  f"HTTP {code} ({reason}) — transient, will re-check tomorrow")
        print()
    if failures:
        print(f"FAIL — {len(failures)} published entries have broken (4xx) llms.txt URLs:")
        for e, code, reason in failures:
            print(f"  - {e['_source_file']}: {e.get('name','?')}: "
                  f"HTTP {code} ({reason})")
        return 1
    else:
        print(f"OK — all published entries serve a working llms.txt"
              f"{f' ({len(flaky)} transient warning(s) ignored)' if flaky else ''}.")
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
