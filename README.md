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

The HTML is a single self-contained file — no build step, no dependencies.
Styles and the light/dark toggle are inline. Open it locally and it works.

## How the numbers are produced

Data comes from the GitHub REST and GraphQL APIs over a rolling 90-day window,
across every active `gemaraproj` repo. Archived repos are excluded, and bot
accounts are stripped from human counts.

Each report carries its own "Method and caveats" section at the bottom with the
exact window, exclusions, and known undercounts. Read it before quoting a number
anywhere that matters.

## Updating

1. Edit the Markdown report.
2. Regenerate `index.html` to match.
3. Open a PR. Merging to `main` publishes the page.

When the next quarter lands, add a dated pair of files and point `index.html`
at the newest one.

## License

[Apache 2.0](LICENSE).
