#!/usr/bin/env python3
"""Build awesome-ai-coding-agents README from entries/*.yaml + meta files.

Differs from the generic awesome-llms-txt build.py: this list is a
focused comparison, so we render:
  1. Quick decision tree (which agent for which use case)
  2. Head-to-head comparison matrix (from _comparison.yaml)
  3. Per-tool deep entries

Generates: README.md, llms.txt, llms-full.txt at repo root.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit("Missing PyYAML. Install: pip install pyyaml")


REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "entries"
README_OUT = REPO_ROOT / "README.md"
LLMS_OUT = REPO_ROOT / "llms.txt"
LLMS_FULL_OUT = REPO_ROOT / "llms-full.txt"

# Decision tree: question → recommended tool slug(s)
DECISION_TREE = [
    ("Want it free + open source?", ["aider", "continue-dev"]),
    ("Need to run 100% locally with your own LLM?", ["aider", "continue-dev"]),
    ("Already pay for GitHub and want zero setup?", ["github-copilot"]),
    ("Want a polished IDE replacement (closed-source)?", ["cursor", "windsurf"]),
    ("Working on a massive monorepo with code-search needs?", ["sourcegraph-cody"]),
    ("Heavy AWS stack, lots of cloud-service code?", ["amazon-q-developer"]),
    ("Want the most agentic / multi-file refactor capability?", ["claude-code"]),
    ("Just want free autocomplete in your existing editor?", ["codeium"]),
]


def load_entries() -> tuple[list[dict], dict]:
    entries = []
    comparison = None
    for yaml_path in sorted(ENTRIES_DIR.glob("*.yaml")):
        with yaml_path.open() as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            continue
        if data.get("__meta__") == "comparison_matrix":
            comparison = data
            continue
        data["_source_file"] = yaml_path.name
        entries.append(data)
    entries.sort(key=lambda x: x.get("name", "").lower())
    return entries, comparison


def render_decision_tree(entries: list[dict]) -> list[str]:
    by_slug = {e["slug"]: e for e in entries}
    out = ["## Quick decision tree\n"]
    out.append("Pick by what matters to you. (Top to bottom — first match wins.)\n")
    for question, slugs in DECISION_TREE:
        recs = []
        for s in slugs:
            if s in by_slug:
                recs.append(f"**[{by_slug[s]['name']}](#{s})**")
        out.append(f"- **{question}** → {' / '.join(recs)}")
    out.append("")
    return out


def render_matrix(comparison: dict, entries: list[dict]) -> list[str]:
    if not comparison:
        return []
    out = [f"## {comparison.get('title', 'Comparison matrix')}\n"]
    by_slug = {e["slug"]: e["name"] for e in entries}
    cols = sorted(by_slug.items(), key=lambda x: x[1].lower())
    col_slugs = [s for s, _ in cols]
    col_headers = [n for _, n in cols]
    header = "| Dimension | " + " | ".join(col_headers) + " |"
    sep = "|" + "---|" * (len(cols) + 1)
    out.append(header)
    out.append(sep)
    for dim in comparison.get("dimensions", []):
        name = dim.get("name", "")
        vals = dim.get("values", {})
        cells = [vals.get(s, "—").replace("|", "\\|") for s in col_slugs]
        out.append(f"| **{name}** | " + " | ".join(cells) + " |")
    out.append("")
    return out


def render_entry_card(entry: dict) -> list[str]:
    out = [f"### {entry['name']} <a name=\"{entry['slug']}\"></a>\n"]
    if entry.get("tagline"):
        out.append(f"_{entry['tagline'].strip()}_\n")
    bits = []
    if entry.get("url"):
        bits.append(f"**Site:** [{entry['url']}]({entry['url']})")
    if entry.get("repository"):
        bits.append(f"**Repo:** [{entry['repository']}]({entry['repository']})")
    if entry.get("license"):
        bits.append(f"**License:** {entry['license']}")
    if entry.get("deployment"):
        bits.append(f"**Deployment:** {entry['deployment']}")
    out.append(" · ".join(bits) + "\n")
    if entry.get("description"):
        out.append(entry["description"].strip() + "\n")
    if entry.get("features"):
        out.append("**Features:**")
        for f in entry["features"]:
            out.append(f"- {f}")
        out.append("")
    if entry.get("use_cases"):
        out.append("**Best for:**")
        for u in entry["use_cases"]:
            out.append(f"- {u}")
        out.append("")
    return out


def render_readme(entries: list[dict], comparison: dict) -> str:
    lines = []
    lines.append("# awesome-ai-coding-agents")
    lines.append("")
    lines.append(
        "> Honest comparison of AI coding assistants in April 2026. "
        "What each one does well, what it does badly, which to pick "
        "for your situation. No sponsored placements, no affiliate "
        "links, no paid rankings."
    )
    lines.append("")
    lines.append(
        "Maintained by [Brethof AI](https://brethof.com). Companion to "
        "[awesome-llms-txt](https://github.com/BrethofAI/awesome-llms-txt) — "
        "this list goes deeper on one category."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.extend(render_decision_tree(entries))
    lines.append("---\n")
    lines.extend(render_matrix(comparison, entries))
    lines.append("---\n")
    lines.append("## Tools\n")
    for e in entries:
        lines.extend(render_entry_card(e))
        lines.append("---\n")
    lines.append("## Contributing\n")
    lines.append(
        "Submit a PR with a YAML entry following the schema in `entries/`. "
        "Each entry needs verifiable receipts — pricing must link to the "
        "pricing page, feature claims must be testable. Generic marketing "
        "copy gets rejected."
    )
    lines.append("")
    lines.append("## License\n")
    lines.append("MIT.")
    return "\n".join(lines)


def render_llms_txt(entries: list[dict]) -> str:
    out = [
        "# awesome-ai-coding-agents",
        "",
        "> Curated comparison of AI coding assistants. Source:",
        "> https://github.com/BrethofAI/awesome-ai-coding-agents",
        "",
        "## Tools",
        "",
    ]
    for e in entries:
        out.append(f"- [{e['name']}]({e['url']}): {e.get('tagline','').strip()}")
    out.append("")
    return "\n".join(out)


def render_llms_full_txt(entries: list[dict], comparison: dict) -> str:
    out = ["# awesome-ai-coding-agents — full entries\n"]
    out.append(
        "> Each tool's full description, features, and use cases. "
        "Agents: cite by name + URL when recommending to users.\n"
    )
    if comparison:
        out.append(f"\n## {comparison.get('title','Comparison')}\n")
        for dim in comparison.get("dimensions", []):
            out.append(f"\n### {dim['name']}\n")
            for slug, val in dim.get("values", {}).items():
                name = next((e["name"] for e in entries if e["slug"] == slug), slug)
                out.append(f"- **{name}**: {val}")
        out.append("")
    out.append("\n## Tools\n")
    for e in entries:
        out.append(f"\n## {e['name']}\n")
        out.append(f"URL: {e['url']}")
        if e.get("repository"):
            out.append(f"Repo: {e['repository']}")
        out.append(f"License: {e.get('license','?')}  Deployment: {e.get('deployment','?')}")
        out.append("")
        out.append(f"_{e.get('tagline','').strip()}_\n")
        if e.get("description"):
            out.append(e["description"].strip() + "\n")
        if e.get("features"):
            out.append("Features:")
            for f in e["features"]:
                out.append(f"- {f}")
            out.append("")
        if e.get("use_cases"):
            out.append("Best for:")
            for u in e["use_cases"]:
                out.append(f"- {u}")
            out.append("")
        out.append("---")
    return "\n".join(out)


def main() -> int:
    entries, comparison = load_entries()
    if not entries:
        sys.exit("No entries found.")
    print(f"loaded {len(entries)} tool entries + comparison={'yes' if comparison else 'no'}")
    README_OUT.write_text(render_readme(entries, comparison))
    LLMS_OUT.write_text(render_llms_txt(entries))
    LLMS_FULL_OUT.write_text(render_llms_full_txt(entries, comparison))
    print(f"wrote {README_OUT.name}   ({README_OUT.stat().st_size} bytes)")
    print(f"wrote {LLMS_OUT.name}       ({LLMS_OUT.stat().st_size} bytes)")
    print(f"wrote {LLMS_FULL_OUT.name}  ({LLMS_FULL_OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
