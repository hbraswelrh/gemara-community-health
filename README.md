# gemara-community-health

Quarterly health reports for the [Gemara](https://github.com/gemaraproj) project —
contributor intake, maintainer load, responsiveness, adoption, and visibility,
pulled from GitHub and written up for maintainers and leadership.

**Read the current report:** https://hbraswelrh.github.io/gemara-community-health/

## What's here

| File | What it is |
|---|---|
| `index.html` | November 2026 report, rendered. This is what GitHub Pages serves. |
| `gemara-community-health-report-2026-11.md` | Same report in Markdown. The source of record. |
| `data/metrics-YYYY-MM.json` | The raw numbers a report was written from. |
| `data/adopters.json` | Known spec and SDK adopters. Kept by hand. |
| `scripts/` | The collector. |

The HTML is a single self-contained file — no build step, no dependencies.
Styles and the light/dark toggle are inline. Open it locally and it works.

## How the numbers are produced

`scripts/collect.py` pulls public data for every active `gemaraproj` repo over a
rolling 90-day window and writes it to `data/metrics-YYYY-MM.json`. Archived
repos are excluded and bot accounts are kept out of the human counts.

It runs stdlib-only Python — nothing to install:

```bash
GH_TOKEN=$(gh auth token) python3 scripts/collect.py \
  --org gemaraproj --window 90 --out data/metrics-$(date -u +%Y-%m).json
```

A monthly workflow (`.github/workflows/collect-metrics.yml`) runs the same
command and opens a PR when the numbers move. It authenticates with the
workflow's built-in `GITHUB_TOKEN`; there is no PAT to provision or rotate.

The collector produces data, not prose. Someone still has to read the JSON and
decide what the movement means.

### What it deliberately leaves alone

**Anything LFX Insights already publishes.** Employer affiliation, who holds
merge rights, meeting attendance, Scorecard results, contributor retention — LFX
has access to data the GitHub API does not, so recomputing a worse version here
would only put two different numbers for the same thing in front of the same
reader. Those metrics come out under `lfx_insights.see_lfx_instead` as links into
the dashboard, with no value attached.

One caveat worth knowing: LFX tracks a single repo from this org, still filed
under the pre-rename `ossf/gemara` path. Figures there describe that repo, not
the org.

**Spec adopters.** Finding projects that use `security-insights.yml` without
importing the Go SDK needs cross-org code search, and `GITHUB_TOKEN` cannot do
that. Rather than add a PAT for it, the list lives in `data/adopters.json` and is
labelled in the output as a floor rather than a total. Edit it when you learn
about a new one.

Each report also carries its own "Method and caveats" section with the exact
window, exclusions, and known undercounts. Read that before quoting a number
anywhere that matters.

## Tests

```bash
python3 -m unittest discover -s tests -t .
```

The aggregation layer is pure and tested against fixtures; the GitHub client is
tested with an injected transport. Neither needs a network.

## Updating a report

1. Run the collector, or take the JSON from the latest automated PR.
2. Edit the Markdown report.
3. Regenerate `index.html` to match.
4. Open a PR. Merging to `main` publishes the page.

When the next quarter lands, add a dated pair of files and point `index.html`
at the newest one.

## License

[Apache 2.0](LICENSE).
