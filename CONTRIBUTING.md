# Contributing

Thanks for wanting to help. This list curates AI tools for human and
agent discovery. Every well-described entry helps that mission.

## Adding an entry

1. Fork this repo.
2. Add a YAML file under `entries/` named after the tool's slug
   (e.g. `entries/my-tool.yaml`).
3. Open a pull request. CI reports what it finds, but a wrong
   `llms_txt_status` won't block the merge — see below.

## `llms_txt_status` is maintained automatically

That field is a *derived fact* about a live URL, not an editorial decision, so
a daily job (`scripts/validate.py --heal`) keeps it honest. Put your best guess
in your PR; if it's wrong, CI corrects it within a few days. Hand-editing a
status to override the checker will just be reverted — fix the URL instead.

The check sniffs the response body, not only the status code: many docs sites
answer *any* unknown path with HTTP 200 and their app shell, and a code-only
check would read that as a working `llms.txt`. Flips require a streak — 3
consecutive definitive failures to demote, 2 consecutive clean fetches to
promote — so one bad network day changes nothing. Streak counters live in
`.health.json`; don't hand-edit that either.

## Schema

See an existing entry under `entries/` as a template. Required fields:
- `name`, `slug`, `url`
- `tagline` (one sentence)
- `description` (multi-paragraph for showcase entries)
- `license` (open-source / commercial / freemium / paid / source-available)
- `deployment` (local / self-hosted / saas / library / cli)
- `added` (YYYY-MM-DD)

## What we accept

- Tools in production or active development
- Both open-source and commercial tools
- Tools with public documentation we can verify

## What we don't accept

- Dead projects (last commit > 12 months, broken site)
- Wrappers with no substance ("just a ChatGPT prompt frontend")
- Affiliate-link or referral-heavy listings
- Generic marketing copy without substance

## Receipts required

Every claim in an entry needs a verifiable source. Pricing claims must
link the pricing page. Feature claims must be testable. "Best in class"
claims need to identify the dimension you're measuring.

## License

By submitting a PR you agree that your contribution is licensed under
the same terms as the repo (MIT).
