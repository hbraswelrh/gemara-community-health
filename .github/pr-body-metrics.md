Automated refresh of the numbers behind the community health report.

**This changes data, not prose.** Someone still has to read the JSON, decide
what the movement means, and update the report and `index.html`.

### What was collected

Public GitHub data for the `gemaraproj` org over a rolling window, using the
workflow's built-in `GITHUB_TOKEN`. No personal access token involved.

### What was deliberately not collected

- **Anything LFX Insights publishes** — employer affiliation, merge rights,
  meeting attendance, Scorecard, retention. These appear in the JSON under
  `lfx_insights.see_lfx_instead` as links into the dashboard, with no value
  attached. Publishing a second, worse number for a metric LFX already owns
  would just give two answers to the same question.
- **Spec adopters** — finding these needs cross-org code search, which
  `GITHUB_TOKEN` cannot do. The list is curated by hand in
  `data/adopters.json` and labelled in the output as a floor, not a total.

### Reviewing

Check `meta.window_start` and `meta.window_end` first, then skim the diff for
counts that moved further than a month of activity would explain. A sharp jump
usually means a repo was added, renamed, or un-archived rather than a real
change in the community.

Counts drawn from GitHub's own totals (releases, open issues) include things a
human reading the repo would not count — draft releases, for one. Treat them as
directional.
