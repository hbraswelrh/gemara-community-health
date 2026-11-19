# gemara-community-health

Quarterly health reports for [Gemara](https://github.com/gemaraproj) maintainers
and project leadership. We use public GitHub data to see who is contributing,
how long people wait for a reply, and where the project is being used.

[Read the current report on GitHub Pages](https://hbraswelrh.github.io/gemara-community-health/).

## Report files

| File | What it is |
|---|---|
| `index.html` | November 2026 report, rendered. This is what GitHub Pages serves. |
| `gemara-community-health-report-2026-11.md` | Same report in Markdown. The source of record. |
| `data/metrics-YYYY-MM.json` | The raw numbers a report was written from. |
| `data/adopters.json` | Known spec and SDK adopters. Kept by hand. |
| `scripts/` | The collector. |

You can open `index.html` locally without building anything. The styles and
light/dark toggle are included in the file. The report loads Sora and Courier
Prime from `assets/fonts/`, so you can preview it without an internet connection.

## Collecting metrics

`scripts/collect.py` pulls public data for every active `gemaraproj` repo over a
rolling 90-day window and writes it to `data/metrics-YYYY-MM.json`. Archived
repos are excluded and bot accounts are kept out of the human counts.

The collector uses only the Python standard library. Run it with a token from
your authenticated `gh` session:

```bash
GH_TOKEN=$(gh auth token) python3 scripts/collect.py \
  --org gemaraproj --window 90 --out data/metrics-$(date -u +%Y-%m).json
```

A monthly workflow (`.github/workflows/collect-metrics.yml`) runs the same
command and opens a PR when the numbers move. It authenticates with the
workflow's built-in `GITHUB_TOKEN`; there is no PAT to provision or rotate.

Before updating the report, read the JSON and check what changed and why.

### LFX Insights and spec adoption

Use LFX Insights for employer affiliation, merge rights, meeting attendance,
Scorecard results, and contributor retention. LFX has data the GitHub API
does not expose, so the collector links to the dashboard under
`lfx_insights.see_lfx_instead` rather than publishing a second set of numbers.

LFX tracks one Gemara repo under its old path, `ossf/gemara`. Its figures
cover that repo alone.

Finding projects that use `security-insights.yml` without importing the Go SDK
takes cross-org code search, which `GITHUB_TOKEN` cannot do. We keep the known
adopters in `data/adopters.json` instead of adding a personal access token.
Add projects as you find them. The output labels this count as a lower bound.

Before citing a number, check the report's "Method and caveats" section for
the exact window, exclusions, and known undercounts.

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
