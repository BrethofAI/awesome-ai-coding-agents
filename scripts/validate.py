#!/usr/bin/env python3
"""Reconcile every entry's ``llms_txt_status`` with what the web actually serves.

``llms_txt_status`` is not an opinion — it is a *derived fact* about a live URL.
Maintaining it by hand means link rot is only ever found by a human reading a
red build, which is exactly the failure this script exists to remove.

Two modes:

    python3 scripts/validate.py            # report drift, change nothing
    python3 scripts/validate.py --heal     # write the corrected statuses back

``--heal`` is what CI runs daily. It rewrites ``llms_txt_status`` in the entry
YAML, updates ``.health.json``, and leaves the working tree ready to commit.
Link rot is therefore *repaired*, not merely *reported*.

WHY A STATUS CODE IS NOT ENOUGH
-------------------------------
Many docs sites are SPAs that answer any unknown path with HTTP 200 and their
app shell. A status-code-only check certifies those as a working ``llms.txt``.
Measured against this corpus on 2026-07-30, six of forty-nine claimed-published
entries were HTML pages, and two entries marked ``missing`` had quietly started
serving a real file. So the body is sniffed, not just the code.

An entry counts as published when the response is 2xx and the body is *not* an
HTML document. Note that spec conformance (llmstxt.org wants a leading ``# ``
H1) is deliberately NOT required: a few sites serve a large plain-text docs
bundle at ``/llms.txt`` instead. That is still a machine-readable file at the
advertised URL, so it stays published; the non-conforming shape is reported for
information only.

HYSTERESIS
----------
A single bad day must not rewrite the list. ``.health.json`` tracks consecutive
outcomes per entry; a status only flips after DEMOTE_AFTER consecutive
definitive failures or PROMOTE_AFTER consecutive clean fetches. Transient
errors (timeout, connection reset, 5xx, 429) never move either streak — they
are noise, not evidence.

Streak counters are capped at their thresholds so that a steady-state day
produces a byte-identical ``.health.json`` and therefore no commit. The file
carries no timestamps for the same reason: it should only change when reality
changes.

Exit codes: 0 = healthy or healed. 1 = the script itself could not run.
Link rot never fails the build; it gets fixed.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
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
HEALTH_PATH = REPO_ROOT / ".health.json"

USER_AGENT = ("awesome-llms-txt-validator/2.0 "
              "(+https://github.com/brethofai/awesome-llms-txt)")
TIMEOUT = 20
RETRIES = 3            # transient outcomes only
RETRY_BACKOFF = 2.0    # seconds, multiplied by attempt number
WORKERS = 8            # entries are spread over ~100 distinct hosts

DEMOTE_AFTER = 3       # consecutive definitive failures before published -> missing
PROMOTE_AFTER = 2      # consecutive clean fetches before missing -> published

# Outcome states.
OK = "ok"                  # 2xx and the body is a real file      -> published
GONE = "gone"              # definitive 4xx                       -> missing
NOT_A_FILE = "not_a_file"  # 2xx but the body is an HTML document -> missing
TRANSIENT = "transient"    # timeout / conn / 5xx / 429           -> no change

DEFINITIVE_BAD = (GONE, NOT_A_FILE)

# ``[ \t\r]*`` not ``[ \t]*``: entry files may be checked out with CRLF on
# Windows, and a bare ``$`` in MULTILINE matches before the \n, leaving the \r
# unconsumed. Without the \r the pattern silently fails to match and heal
# becomes a no-op on exactly one platform.
_STATUS_RE = re.compile(r"^(llms_txt_status:[ \t]*)(\S+)[ \t\r]*$", re.MULTILINE)
_LLMS_TXT_RE = re.compile(r"^llms_txt:[ \t]*\S[^\r\n]*", re.MULTILINE)


# ── probing ───────────────────────────────────────────────────────────────

def looks_like_html(body: str) -> bool:
    """True when the payload is a web page rather than an llms.txt file.

    Sniffs the body rather than trusting Content-Type: a handful of sites serve
    a perfectly good llms.txt with a wrong header, and punishing those would be
    a false negative. The body is authoritative; the header only corroborates.
    """
    head = body.lstrip()[:600].lower()
    if head.startswith(("<!doctype html", "<html")):
        return True
    # Fragment-style shells that skip the doctype.
    return "<head" in head and "<script" in head


def classify(resp: requests.Response) -> tuple[str, str]:
    """Map a response to (state, shape). ``shape`` is human-facing detail."""
    code = resp.status_code
    if code == 429 or 500 <= code < 600:
        return TRANSIENT, f"HTTP {code}"
    if 400 <= code < 500:
        return GONE, f"HTTP {code}"
    if not (200 <= code < 300):
        return TRANSIENT, f"HTTP {code}"

    body = resp.text or ""
    ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
    if not body.strip():
        return NOT_A_FILE, "empty body"
    if looks_like_html(body):
        return NOT_A_FILE, f"HTML page ({ctype or 'no content-type'}, {len(body)}B)"

    first = next((ln for ln in body.splitlines() if ln.strip()), "")
    if first.startswith("# "):
        return OK, f"llms.txt ({len(body)}B)"
    # Real text, but not the spec's H1 form. Still a machine-readable file at
    # the advertised URL, so it counts — flagged so the shape is visible.
    return OK, f"non-conforming text, no H1 ({ctype or '?'}, {len(body)}B)"


def probe(url: str) -> tuple[str, int, str]:
    """GET with retries on transient outcomes. Returns (state, code, shape)."""
    state, code, shape = TRANSIENT, -1, "no attempt"
    for attempt in range(1, RETRIES + 1):
        try:
            r = requests.get(url, timeout=TIMEOUT, allow_redirects=True,
                             headers={"User-Agent": USER_AGENT})
            state, shape = classify(r)
            code = r.status_code
        except requests.exceptions.Timeout:
            state, code, shape = TRANSIENT, -1, "timeout"
        except requests.exceptions.ConnectionError as e:
            state, code, shape = TRANSIENT, -1, f"conn-err: {type(e).__name__}"
        except Exception as e:                       # noqa: BLE001 - report, don't crash
            state, code, shape = TRANSIENT, -1, f"err: {type(e).__name__}"
        if state != TRANSIENT:
            return state, code, shape                # definitive, stop retrying
        if attempt < RETRIES:
            time.sleep(RETRY_BACKOFF * attempt)
    return state, code, shape


# ── entries and health state ──────────────────────────────────────────────

def load_entries() -> list[dict]:
    entries = []
    for p in sorted(ENTRIES_DIR.glob("*.yaml")):
        with p.open(encoding="utf-8") as f:
            d = yaml.safe_load(f) or {}
        d["_path"] = p
        d["_source_file"] = p.name
        d["_key"] = d.get("slug") or p.stem
        entries.append(d)
    return entries


def load_health() -> dict:
    if not HEALTH_PATH.is_file():
        return {}
    try:
        data = json.loads(HEALTH_PATH.read_text(encoding="utf-8"))
    except Exception as e:                           # noqa: BLE001
        # Corrupt state must be loud: silently restarting the streaks would let
        # a demotion fire days early, or never.
        sys.exit(f"FATAL: {HEALTH_PATH.name} is unreadable ({e}). "
                 f"Fix or delete it deliberately, then re-run.")
    return data.get("entries", {}) if isinstance(data, dict) else {}


def save_health(health: dict) -> None:
    payload = {
        "schema": 1,
        "_comment": ("Machine state for scripts/validate.py. Consecutive-outcome "
                     "streaks per entry, capped at their thresholds and carrying "
                     "no timestamps, so this file only changes when a URL's real "
                     "state changes. Do not hand-edit."),
        "entries": {k: health[k] for k in sorted(health)},
    }
    tmp = HEALTH_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, HEALTH_PATH)


def set_status(path: Path, new_status: str) -> bool:
    """Rewrite llms_txt_status in place, preserving all other formatting.

    Line-surgical on purpose: a yaml.safe_load/safe_dump round trip would strip
    every comment and reflow the whole file, burying the real change in noise.

    Read and write with newline="" so the file's existing line endings survive
    untouched — otherwise a one-word edit rewrites every line of a CRLF file.
    """
    with path.open(encoding="utf-8", newline="") as f:
        text = f.read()
    if _STATUS_RE.search(text):
        new_text = _STATUS_RE.sub(
            lambda m: f"{m.group(1)}{new_status}", text, count=1)
    else:
        m = _LLMS_TXT_RE.search(text)
        if not m:
            return False
        eol = "\r\n" if "\r\n" in text else "\n"
        new_text = (text[:m.end()] + f"{eol}llms_txt_status: {new_status}"
                    + text[m.end():])
    if new_text == text:
        return False
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    return True


# ── reconcile ─────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--heal", action="store_true",
                    help="write corrected statuses back to the entry YAML")
    ap.add_argument("--force", action="store_true",
                    help="apply the current evidence immediately, ignoring the "
                         "consecutive-run streaks. For seeding .health.json the "
                         "first time, or after verifying a URL by hand. CI must "
                         "NOT use this — the streaks are what stop one bad day "
                         "from rewriting the list.")
    ap.add_argument("--json", action="store_true", help="emit a JSON report")
    args = ap.parse_args()

    entries = load_entries()
    checkable = [e for e in entries if e.get("llms_txt")]
    health = load_health()

    print(f"{len(entries)} entries, {len(checkable)} with an llms_txt URL "
          f"({'HEAL' if args.heal else 'report-only'})")
    print()

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        probes = list(ex.map(lambda e: probe(e["llms_txt"]), checkable))

    promoted: list[tuple[dict, str]] = []
    demoted: list[tuple[dict, str]] = []
    pending: list[tuple[dict, str, str]] = []   # drift seen, streak not yet met
    transient: list[tuple[dict, str]] = []
    nonconforming: list[tuple[dict, str]] = []
    failed_write: list[dict] = []

    for e, (state, code, shape) in sorted(
            zip(checkable, probes), key=lambda z: z[0].get("name", "").lower()):
        claimed = e.get("llms_txt_status", "")
        rec = health.get(e["_key"], {"ok_streak": 0, "fail_streak": 0})

        if state == OK:
            rec["ok_streak"] = min(rec.get("ok_streak", 0) + 1, PROMOTE_AFTER)
            rec["fail_streak"] = 0
            if "no H1" in shape:
                nonconforming.append((e, shape))
        elif state in DEFINITIVE_BAD:
            rec["fail_streak"] = min(rec.get("fail_streak", 0) + 1, DEMOTE_AFTER)
            rec["ok_streak"] = 0
        else:
            transient.append((e, shape))
        # Deliberately NOT storing ``shape`` here: it embeds the response size,
        # and docs sites change size constantly. Persisting it would make this
        # file churn every day and produce a commit even when nothing about the
        # entry's real state changed. State and code only.
        rec["last"] = {"state": state, "code": code}
        health[e["_key"]] = rec

        # What the evidence says the status should be.
        promote_at = 1 if args.force else PROMOTE_AFTER
        demote_at = 1 if args.force else DEMOTE_AFTER
        want = claimed
        if state == OK and rec["ok_streak"] >= promote_at:
            want = "published"
        elif state in DEFINITIVE_BAD and rec["fail_streak"] >= demote_at:
            want = "missing"

        mark = {OK: "✓", GONE: "✗", NOT_A_FILE: "✗", TRANSIENT: "~"}[state]
        note = ""
        if want != claimed:
            note = f"   →  {claimed or '(unset)'} → {want}"
        elif state in DEFINITIVE_BAD and claimed == "published":
            note = (f"   (failing {rec['fail_streak']}/{DEMOTE_AFTER} — "
                    f"demotes after {DEMOTE_AFTER})")
            pending.append((e, shape, "demote"))
        elif state == OK and claimed == "missing":
            note = (f"   (live {rec['ok_streak']}/{PROMOTE_AFTER} — "
                    f"promotes after {PROMOTE_AFTER})")
            pending.append((e, shape, "promote"))
        print(f"  {mark} [{code:>4}] {e.get('name','?'):<28} {shape}{note}")

        if want == claimed:
            continue
        (promoted if want == "published" else demoted).append((e, shape))
        if args.heal and not set_status(e["_path"], want):
            failed_write.append(e)

    print()
    print("=" * 68)

    def section(title: str, rows, fmt) -> None:
        if not rows:
            return
        print(f"\n{title}")
        for row in rows:
            print(fmt(row))

    section(f"PROMOTED to published ({len(promoted)}) — "
            f"{PROMOTE_AFTER} consecutive clean fetches:", promoted,
            lambda r: f"  + {r[0]['_source_file']}: {r[0].get('name','?')} — {r[1]}")
    section(f"DEMOTED to missing ({len(demoted)}) — "
            f"{DEMOTE_AFTER} consecutive definitive failures:", demoted,
            lambda r: f"  - {r[0]['_source_file']}: {r[0].get('name','?')} — {r[1]}")
    section(f"drift seen, streak not yet met ({len(pending)}):", pending,
            lambda r: f"  · {r[0].get('name','?')}: {r[2]} pending — {r[1]}")
    section(f"transient, ignored ({len(transient)}):", transient,
            lambda r: f"  ~ {r[0].get('name','?')}: {r[1]}")
    section(f"served, but not spec-conforming ({len(nonconforming)}) — "
            f"informational, still counted as published:", nonconforming,
            lambda r: f"  ? {r[0].get('name','?')}: {r[1]}")

    if failed_write:
        print(f"\nFATAL: could not rewrite {len(failed_write)} entr"
              f"{'y' if len(failed_write) == 1 else 'ies'}:")
        for e in failed_write:
            print(f"  {e['_source_file']}")
        return 1

    if args.heal:
        save_health(health)
        changed = len(promoted) + len(demoted)
        print(f"\nhealed {changed} status change(s); "
              f"{HEALTH_PATH.name} updated.")
        if changed:
            print("Run scripts/build.py to regenerate README/llms.txt.")
    else:
        drift = len(promoted) + len(demoted)
        if drift:
            print(f"\n{drift} status change(s) ready to apply. "
                  f"Re-run with --heal.")
        elif pending:
            print(f"\nNo status change applied: {len(pending)} entr"
                  f"{'y' if len(pending) == 1 else 'ies'} drifted but have not "
                  f"yet met the streak threshold. Statuses flip once they do.")
        else:
            print("\nAll statuses match what the web serves.")

    if args.json:
        print(json.dumps({
            "promoted": [e["_key"] for e, _ in promoted],
            "demoted": [e["_key"] for e, _ in demoted],
            "transient": [e["_key"] for e, _ in transient],
            "nonconforming": [e["_key"] for e, _ in nonconforming],
        }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
