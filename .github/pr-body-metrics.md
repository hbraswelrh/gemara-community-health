This refresh updates the metrics JSON. Review the changes before using the
numbers to update the report and `index.html`.

### What was collected

The workflow collected public GitHub data for `gemaraproj` over a rolling
window. It used the built-in `GITHUB_TOKEN` and did not need a personal
access token.

### Metrics maintained elsewhere

Use the links under `lfx_insights.see_lfx_instead` for employer affiliation,
merge rights, meeting attendance, Scorecard, and retention. LFX Insights has
data the collector cannot get from GitHub.

We maintain the list of known spec adopters in `data/adopters.json` because
`GITHUB_TOKEN` cannot search code across organizations. The output labels
the count as a lower bound.

### Reviewing

Check `meta.window_start` and `meta.window_end` first. If a count changed more
than you would expect in a month, check whether someone added, renamed, or
unarchived a repo before reading it as a change in community activity.

Use GitHub's totals for releases and open issues as a guide. For example,
the release count can include drafts.
