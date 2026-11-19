# Gemara Community Health Report: November 2026

This report covers 14 active `gemaraproj` repos over the 90 days from 2026-08-19 to 2026-11-17. The data comes from GitHub REST and GraphQL, pulled on 2026-11-17.

---

## TL;DR

Gemara welcomed as many new contributors in 90 days as it did in all of 2025.

| Metric | Count | Context |
|---|---|---|
| New contributors (first merged PR) | 12 in 90 days (7 in the last 30) | 39% of the 31 contributors to date |
| Issues with no human reply | 60% (57 of 95) | Median first reply among issues that got one: 8.3 days |
| Review concentration | 3 people handled 82% of human reviews | |
| External spec adopters | CloudNativePG, wasmCloud, Capsule, OpenSSF Scorecard | These projects use the spec without the Go SDK |
| Getting started | 5 open issues labeled `good first issue`; 0 repos with GitHub topics | No issues with that label in `gemara` |

The median time to merge a non-bot PR was about 19 hours. If you are new and need an answer before you can open a PR, the wait for an issue reply can make it harder to get started.

### Leadership requests

1. Move five active volunteer reviewers up the contributor ladder and give them merge rights for the repos they review.
2. File a Linux Foundation ticket to update the `ossf/gemara` listing in LFX Insights and add the other 13 repos.
3. Document how the four adopters in this report use the spec and keep a public record as we find more.

---

## 1. Scale and activity

| Metric (90d) | Value |
|---|---|
| PRs merged | 267 (161 human / 106 Dependabot) |
| Unique human PR authors | 19 |
| New contributors | 12 |
| Issues opened / closed | 95 / 62 (net −33) |
| Open backlog | 91 issues, 83 PRs |
| All-time human contributors | 31 |
| Releases, all time | 62 across 5 repos |

The issue backlog grew during the window. Two repos hold 70% of all open PRs: `gemara` has 39 and `website` has 19. On `website`, more PRs are open than issues.

The most-forked repos were `gemara` (31), `go-gemara` (18), `gemara-mcp` (11), and `website` (11).

<details>
<summary>Per-repository detail</summary>

| Repo | Forks | PRs merged 90d (human) | Human authors | Open issues | Open PRs | Releases |
|---|---:|---:|---:|---:|---:|---:|
| gemara | 31 | 67 (51) | 11 | 34 | 39 | 30 |
| website | 11 | 26 (25) | 7 | 8 | 19 | 0 |
| go-gemara | 18 | 28 (14) | 7 | 15 | 6 | 19 |
| gemara-react | 2 | 29 (13) | 2 | 0 | 6 | 0 |
| gemara-mcp | 11 | 32 (10) | 3 | 3 | 5 | 7 |
| grcli | 2 | 9 (9) | 3 | 3 | 0 | 0 |
| gemara-publish-action | 4 | 25 (6) | 2 | 4 | 1 | 5 |
| .github | 2 | 8 (8) | 3 | 1 | 0 | — |
| community | 1 | 7 (7) | 2 | 11 | 1 | — |
| gemara-ai | 6 | 6 (6) | 2 | 6 | 3 | 0 |
| gemara-python | 4 | 22 (4) | 2 | 1 | 2 | 1 |
| grc-store-clientkit | 0 | 3 (3) | 2 | 5 | 0 | 0 |
| awesome-gemara | 3 | 3 (3) | 2 | 0 | 0 | — |
| gemara-mcp-eval-infra | 3 | 2 (2) | 1 | 0 | 1 | — |

</details>

---

## 2. New contributors

| Period | New contributors |
|---|---:|
| 2025 (full year) | 12 |
| 2026 Jan to Aug 18 | 7 |
| 2026 Aug 19 to Nov 17 | 12 (7 in the last 30 days) |

Several new contributors are already helping with review and triage. `nameetsinha7-hue` submitted 7 reviews and `YAshhh29` submitted 6. `harshsomankar123-tech` posted the first reply on 6 issues, and `imshubham22apr-gif` did so on 3.

Most of the new contributors' work is in `gemara` and `website`. I would start backlog review there so people who have already contributed have a reason to come back.

<details>
<summary>90-day cohort, by first merge date</summary>

`PaarthPandey10` (09-10), `astrogilda` (09-15), `gxmiranda` (09-30), `kocaemre` (10-02), `vansh-nagar` (10-05), `jor2` (10-24), `YAshhh29` (10-25), `harshsomankar123-tech` (10-28), `nameetsinha7-hue` (10-29), `ravindra-RKB` (10-30), `yvonnedevlinrh` (11-07), `imshubham22apr-gif` (11-10)

</details>

---

## 3. Maintainer workload

Three people handled 82% of human reviews: `jpower432` (74, 50%), `jmeridth` (29, 20%), and `eddie-knight` (19, 13%). Separately, `coderabbitai` did 15 reviews and Copilot did 3.

`jmeridth` was the only person with merged PRs in all 14 repos. If someone else needs to pick up maintenance across repos, we should make it clear who can help with each one.

Three of the eight GitHub org members did not review a PR in the 90-day window. In the review sample, 39 of 143 merged PRs (27%) had no human review. Most were bot or maintenance PRs; check whether the rest included changes that needed review.

---

## 4. Issue replies and PR merges

| Issues opened last 90d | Value |
|---|---|
| Opened | 95 |
| No human response yet | 57 (60%) |
| Median time to first human response | 8.3 days |

The median first reply took about 2 days in `gemara`, 7.5 in `website`, 13 in `grcli`, 29 in `go-gemara`, and 60 in `community`.

The median time to merge a non-bot PR was 19.4 hours across the org. Most repos had a median below 3 hours.

---

## 5. Getting started

What would you find if you came to GitHub looking for a place to start? None of the repos have topics, so a topic search for `grc`, `compliance`, `policy-as-code`, or `supply-chain` will miss them. Of the 5 open issues labeled `good first issue`, none are in `gemara`, even though it has 31 forks. Another label to look for is `help wanted`, which appears on 11 open issues across the org.

`website` has 11 forks and 19 open PRs but no `CONTRIBUTING.md` or license. `gemara-react`, `gemara-python`, and `community` lack repo descriptions. Four of the 14 repos have issue templates, and only `gemara-mcp` has Discussions enabled. GitHub lists the `gemara-mcp-eval-infra` license as `NOASSERTION`, which leaves prospective adopters without a clear license to review.

The repos inherit `CODE_OF_CONDUCT`, `GOVERNANCE`, `CHARTER`, `MAINTAINERS`, `CONTRIBUTOR_LADDER`, and `SECURITY` from `.github`, so there is no need to recreate those files to improve the repo-level guidance.

Seven of the 14 repos have a `security-insights.yml`. Adding it to the other seven would give new contributors a concrete first issue and let people see how we use the format in our own repos.

---

## 6. SDK and spec adoption

The Go dependency graph shows 25 external repos importing `go-gemara`. Most are in ComplyTime, Privateer, revanite-io, or OpenSSF. Independent adopters include `IBM/ai-security-baseline`, `finos/common-cloud-controls`, and `cncf/contribute-site`.

### Spec adoption (`security-insights.yml`)

| Adopter | Status |
|---|---|
| cloudnative-pg | CNCF graduated |
| wasmCloud | CNCF incubating |
| projectcapsule/capsule | CNCF sandbox |
| ossf/scorecard | OpenSSF flagship |

These four projects use the format without importing the Go library, so they do not show up in the dependency graph. [Gabriele Bartolini's comparison of CloudNativePG and Crunchy PGO](https://www.gabrielebartolini.it/articles/2026/05/cloudnativepg-and-crunchy-pgo-an-honest-opinionated-comparison/) documents one example. A scheduled code search with results saved in `gemaraproj/community` would let us see how spec adoption changes over time.

Nearly every SDK adopter works on standards or assessments. I would track which standards and assessment projects take up Gemara rather than use download counts as the main measure of adoption.

`grcli`, `gemara-react`, `grc-store-clientkit`, and `gemara-ai` are under active development but have no release versions for users to pin.

---

## 7. Talks and project coverage

Gemara talks in 2026 included OpenSSF Community Day NA and EU, DevConf CZ, and KubeCon NA SecurityCon. OpenSSF covered [CRA due diligence](https://openssf.org/blog/2026/10/22/who-checked-it-attestations-gemara-and-cra-due-diligence/), and CUE Labs and CloudNativePG also wrote about the project.

The talks and articles are not linked from `website`, the README, or `awesome-gemara`. A talks page would give someone who heard about Gemara at an event a place to find the recording and see how to contribute.

<details>
<summary>Full talk, blog, and post list</summary>

**Talks (2026)**

| Event | Talk | Recording |
|---|---|---|
| OpenSSF Community Day NA (Minneapolis) | [Gemara: The GRC Architecture You Didn't Know You Built](https://openssfcdna2026.sched.com/event/2I458/gemara-the-grc-architecture-you-didnt-know-you-built-hannah-braswell-jennifer-power-red-hat), by Hannah Braswell and Jennifer Power (Red Hat) | [YouTube](https://youtu.be/eGWm29YtEJw?si=LMZ2h9NCVxYsKGqH) |
| OpenSSF Community Day EU (Prague) | [From First PR to Hardening Guide](https://openssfcdeu2026.sched.com/event/2RA3q/from-first-pr-to-hardening-guide-structured-security-with-gemara-hannah-braswell-red-hat), by Hannah Braswell (Red Hat) | [YouTube](https://www.youtube.com/watch?v=5jcwp5It8gU&list=PLDEhySvXRac0&index=14) |
| DevConf CZ 2026 | [Hardening the Source: Gemara, ComplyTime and Ampel](https://pretalx.devconf.info/devconf-cz-2026/schedule/) | [YouTube](https://youtu.be/lJR-59r2MB4?si=DX4zPWMIrHG2_zCP) |
| KubeCon NA (OpenSource SecurityCon) | "The Golden Path Doesn't Exist Yet" lightning round | [LinkedIn](https://www.linkedin.com/posts/openssf_securitycon-kubecon-cloudnativecon-activity-7525707447039131648-W3B1) |

Blogs: [Who Checked It? Attestations, Gemara, and CRA Due Diligence](https://openssf.org/blog/2026/10/22/who-checked-it-attestations-gemara-and-cra-due-diligence/) (Eddie Knight, OpenSSF) · [Introducing the Gemara Model](https://openssf.org/blog/2026/03/09/introducing-the-gemara-model/) (OpenSSF) · [Make Configuration User Friendly](https://cue.dev/blog/make-configuration-user-friendly/) (CUE Labs) · [CloudNativePG vs Crunchy PGO](https://www.gabrielebartolini.it/articles/2026/05/cloudnativepg-and-crunchy-pgo-an-honest-opinionated-comparison/) (Gabriele Bartolini, independent adopter)

LinkedIn: [Eddie Knight on Gemara / OSPS Baseline / Privateer / GRC Store](https://www.linkedin.com/feed/update/urn:li:activity:7524469471328120832/)

</details>

---

## 8. Initiatives

Security Slam 2026 already uses Gemara: `pvtr-security-slam-review` imports `go-gemara`, and Slam repos carry `security-insights.yml`. Are we entering Gemara's own repos? Seven are missing `security-insights.yml` and only two carry their own `SECURITY.md`. I would close those gaps before entering.

The 12 new contributors suggest some informal mentoring may already be happening. I found no tracking issue or board for LFX mentorship. Repository activity does not tell us who participates in OpenSSF working groups.

---

## 9. LFX Insights coverage

LFX Insights lists [one Gemara repo in the OpenSSF collection](https://insights.linuxfoundation.org/project/openssf/repository/ossf_gemara?timeRange=past365days&start=2025-11-16&end=2026-11-16), under `ossf/gemara`. There is no standalone `/project/gemara` page.

GitHub redirects `ossf/gemara` to `gemaraproj/gemara`, so data may still be flowing. Ask the Linux Foundation to update the listing and add the `gemaraproj` org so we can see the other 13 repos.

LFX could give us contributor counts by employer, active maintainers with merge rights, community meeting attendance, per-repo Scorecard results, and contributor retention. This report does not include those measurements.

The public figures of 23 maintainers, 122 organizations, and a 7.3 Scorecard score cover all of OpenSSF. Use Gemara-specific figures when citing project metrics.

---

## Recommendations

### This week

1. Set GitHub topics on all 14 repos: `grc`, `compliance`, `security`, `policy-as-code`, `supply-chain`, and `openssf`.
2. Add descriptions to `gemara-react`, `gemara-python`, and `community`.
3. Triage the 57 unanswered issues, starting with `go-gemara` and `community`. If you cannot resolve an issue yet, a short reply still tells the author someone has seen it.
4. Clarify the `gemara-mcp-eval-infra` license using a recognized SPDX identifier.
5. File the LFX Insights ticket to update the listing and add the other 13 repos.

### This month

6. Create 15 to 20 issues labeled `good first issue`, including at least 5 in `gemara`. Start with the 7 repos missing `security-insights.yml`.
7. Add `CONTRIBUTING.md` and a license to `website`.
8. Review the 58 open PRs in `gemara` and `website`, where most of the new contributors' work is.
9. Enable Discussions across the org.
10. Add a talks page to `website` and link it from the `gemara` README.

### This quarter

11. Use the contributor ladder to give scoped merge rights to people who already review: `nameetsinha7-hue`, `YAshhh29`, `harshsomankar123-tech`, `astrogilda`, and `sonupreetam`.
12. Add per-repo `CODEOWNERS` so `jmeridth` is not the only point of contact for work that spans multiple repos.
13. Publish first releases for `grcli`, `gemara-react`, `grc-store-clientkit`, and `gemara-ai`.
14. Write up how adopters use Gemara. Start with CloudNativePG, a graduated CNCF project with a public writeup to cite, then cover wasmCloud, OpenSSF Scorecard, IBM, FINOS, and Capsule.
15. Schedule a code search for spec adopters and commit the results to `gemaraproj/community`.
16. Record LFX metrics quarterly to see how meeting attendance and organizational diversity change over time.

---

<details>
<summary>Method and caveats</summary>

- Pulled 2026-11-17 via GitHub REST + GraphQL. Window 2026-08-19 → 2026-11-17. Archived repos excluded (`gemara-staging`, `gemara-hub`, `grcli-staging`).
- "Contributor" = author of a merged PR. Commit-only and issue-only participants are not counted, so the all-time 31 undercounts participation.
- Bots (`dependabot`, `coderabbitai`, `github-actions`, `copilot-pull-request-reviewer`, `kusari-inspector`) excluded from human counts.
- Issue first-response = first non-author, non-bot comment. Sampled from 100 most recent issues per repo; coverage complete for the window.
- Review counts sample the 100 most recently updated merged PRs per repo; `gemara` and `go-gemara` may be slightly undercounted.
- Adoption measured by searching for `gemaraproj/go-gemara` in `go.mod` and `gemara` in `security-insights.yml`. Both counts are lower bounds because code search only indexes public, active repos that are not forks. Mirrors and forks were also excluded by hand (`codacy-open-source-projects-scans/cloudnative-pg`, `ydnmu/scorecard`).
- §7 links come from provided notes; URLs were not individually fetched to confirm they resolve.
- §8 initiative status is partly inferred, partly unmeasured.

</details>
