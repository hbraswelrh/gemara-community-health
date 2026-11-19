# Gemara Community Health Report: November 2026

This report covers 14 active `gemaraproj` repositories from August 19 to November 17, 2026. The data was pulled from GitHub on November 17.

---

## In brief

Gemara welcomed as many new contributors in these 90 days as it did in all of 2025. The median time to merge a pull request was about 19 hours, but most new issues went unanswered during the reporting period.

At the Fall 2026 [Security Slam](https://securityslam.com/), participants used Gemara threat catalogs as evidence for the Inspector badge.

| Metric | Count | Context |
|---|---|---|
| New contributors (first merged PR) | 12 in 90 days (7 in the last 30) | 39% of the 31 contributors to date |
| Issues with no human reply | 60% (57 of 95) | Median first reply among issues that got one: 8.3 days |
| External spec adopters | CloudNativePG and OpenSSF Scorecard | Both use the format without importing the Go SDK |

Two things would give us a clearer picture: ask the Linux Foundation to add the other 13 repos to LFX Insights, and document how projects use the spec even when they don’t import the SDK.

---

## 1. Scale and activity

| Metric (90d) | Value |
|---|---|
| PRs merged | 267 (161 human / 106 Dependabot) |
| Unique human PR authors | 19 |
| **New contributors** | **12** |
| Issues opened / closed | 95 / 62 (**net −33**) |
| Open backlog | 91 issues, 83 PRs |
| All-time human contributors | 31 |
| Releases, all time | 62 across 5 repos |

More issues were opened than closed during the period. Two repos account for 70% of the open PRs: `gemara` has 39 and `website` has 19.

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
| 2026 Jan–Aug 18 | 7 |
| **2026 Aug 19 – Nov 17** | **12** (7 in last 30d) |

Several new contributors are helping with review and triage. `nameetsinha7-hue` submitted seven reviews and `YAshhh29` submitted six. `harshsomankar123-tech` posted the first reply on six issues, and `imshubham22apr-gif` did so on three.

Most of the new contributors’ work is in `gemara` and `website`. Those two repos are a good place to start reviewing the backlog.

<details>
<summary>90-day cohort, by first merge date</summary>

`PaarthPandey10` (09-10), `astrogilda` (09-15), `gxmiranda` (09-30), `kocaemre` (10-02), `vansh-nagar` (10-05), `jor2` (10-24), `YAshhh29` (10-25), `harshsomankar123-tech` (10-28), `nameetsinha7-hue` (10-29), `ravindra-RKB` (10-30), `yvonnedevlinrh` (11-07), `imshubham22apr-gif` (11-10)

</details>

---

## 3. Issue replies and PR merges

| Issues opened last 90d | Value |
|---|---|
| Opened | 95 |
| **No human response yet** | **57 (60%)** |
| Median time to first human response | **8.3 days** |

Among issues that got a human reply, the median wait was about 2 days in `gemara`, 7.5 in `website`, 13 in `grcli`, 29 in `go-gemara`, and 60 in `community`.

The median time to merge a non-bot PR was 19.4 hours across the organization. Most repos had a median below three hours.

---

## 4. SDK and spec adoption

The Go dependency graph shows 25 external repos importing `go-gemara`. Most are in ComplyTime, Privateer, revanite-io, or OpenSSF. Other examples include `IBM/ai-security-baseline`, `finos/common-cloud-controls`, and `cncf/contribute-site`.

### Spec adoption

| Adopter | Status |
|---|---|
| cloudnative-pg | **CNCF graduated** |
| ossf/scorecard | OpenSSF flagship |

Neither project imports the Go library, so downloads and dependency counts miss this use. [Gabriele Bartolini’s comparison of CloudNativePG and Crunchy PGO](https://www.gabrielebartolini.it/articles/2026/05/cloudnativepg-and-crunchy-pgo-an-honest-opinionated-comparison/) documents the CloudNativePG example.

We don’t track spec adoption over time yet. A scheduled code search, with results saved in `gemaraproj/community`, would give us a starting point.

Seven of Gemara’s 14 repos have a `security-insights.yml` file.

Most SDK adopters work on standards or assessments. Tracking what those projects build with Gemara would tell us more than download counts alone.

`grcli`, `gemara-react`, `grc-store-clientkit`, and `gemara-ai` are under active development but haven’t published a first release.

---

## 5. Talks and project coverage

Gemara talks in 2026 included OpenSSF Community Day in North America and Europe, DevConf CZ, and KubeCon NA SecurityCon. OpenSSF covered [CRA due diligence](https://openssf.org/blog/2026/10/22/who-checked-it-attestations-gemara-and-cra-due-diligence/), and CUE Labs and CloudNativePG also wrote about the project.

The talks and articles aren’t linked from `website`, the `gemara` README, or `awesome-gemara`. A talks page would give people one place to find the recordings and articles.

<details>
<summary>Full talk, blog, and post list</summary>

**Talks (2026)**

| Event | Talk | Recording |
|---|---|---|
| OpenSSF Community Day NA — Minneapolis | [Gemara: The GRC Architecture You Didn't Know You Built](https://openssfcdna2026.sched.com/event/2I458/gemara-the-grc-architecture-you-didnt-know-you-built-hannah-braswell-jennifer-power-red-hat) — Hannah Braswell, Jennifer Power (Red Hat) | [YouTube](https://youtu.be/eGWm29YtEJw?si=LMZ2h9NCVxYsKGqH) |
| OpenSSF Community Day EU — Prague | [From First PR to Hardening Guide](https://openssfcdeu2026.sched.com/event/2RA3q/from-first-pr-to-hardening-guide-structured-security-with-gemara-hannah-braswell-red-hat) — Hannah Braswell (Red Hat) | [YouTube](https://www.youtube.com/watch?v=5jcwp5It8gU&list=PLDEhySvXRac0&index=14) |
| DevConf CZ 2026 | [Hardening the Source: Gemara, ComplyTime and Ampel](https://pretalx.devconf.info/devconf-cz-2026/schedule/) | [YouTube](https://youtu.be/lJR-59r2MB4?si=DX4zPWMIrHG2_zCP) |
| KubeCon NA — OpenSource SecurityCon | "The Golden Path Doesn't Exist Yet" lightning round | [LinkedIn](https://www.linkedin.com/posts/openssf_securitycon-kubecon-cloudnativecon-activity-7525707447039131648-W3B1) |

**Blogs:** [Who Checked It? Attestations, Gemara, and CRA Due Diligence](https://openssf.org/blog/2026/10/22/who-checked-it-attestations-gemara-and-cra-due-diligence/) (Eddie Knight, OpenSSF) · [Introducing the Gemara Model](https://openssf.org/blog/2026/03/09/introducing-the-gemara-model/) (OpenSSF) · [Make Configuration User Friendly](https://cue.dev/blog/make-configuration-user-friendly/) (CUE Labs) · [CloudNativePG vs Crunchy PGO](https://www.gabrielebartolini.it/articles/2026/05/cloudnativepg-and-crunchy-pgo-an-honest-opinionated-comparison/) (Gabriele Bartolini — independent adopter)

**LinkedIn:** [Eddie Knight on Gemara / OSPS Baseline / Privateer / GRC Store](https://www.linkedin.com/feed/update/urn:li:activity:7524469471328120832/)

</details>

---

## 6. Initiatives

Gemara was part of the [Fall 2026 Security Slam](https://securityslam.com/) through the Inspector badge. To apply for the badge, teams documented project-specific threats in a Gemara threat catalog and pointed reviewers to their self-assessment evidence through `assessments.self.evidence` in `security-insights.yml`. The [Privateer review plugin](https://github.com/eddie-knight/pvtr-security-slam-review#what-each-badge-checks) checks that the evidence is reachable and the catalog contains threats and matches the Gemara schema. People make the final decision. [CloudNativePG’s participation tracker](https://github.com/cloudnative-pg/cloudnative-pg/issues/11763) records that it earned the badge.

The repository data doesn’t show whether contributors took part in LFX Mentorship or OpenSSF working groups.

---

## 7. LFX Insights coverage

LFX Insights lists [one Gemara repo in the OpenSSF collection](https://insights.linuxfoundation.org/project/openssf/repository/ossf_gemara?timeRange=past365days&start=2025-11-16&end=2026-11-16) under its old path, `ossf/gemara`. GitHub redirects that path to `gemaraproj/gemara`. There is no standalone Gemara page in Insights, and the other 13 repos aren’t listed there.

With broader coverage, Insights could help us track contributor counts by employer, meeting attendance, per-repo Scorecard results, and contributor retention. This report doesn’t include those measures.

The public figures of 23 maintainers, 122 organizations, and a 7.3 Scorecard score are for all of OpenSSF, not Gemara.

---

## Recommendations

### This week

1. Reply to unanswered issues, starting with `go-gemara` and `community`. A short acknowledgment helps even when the answer will take longer.
2. Ask the Linux Foundation to update the Insights listing and add the other 13 repos.

### This month

3. Add `security-insights.yml` to the seven repos missing it.
4. Review the 58 open PRs in `gemara` and `website`, where most of the new contributors’ work is.
5. Add a talks page to `website` and link to it from the `gemara` README.

### This quarter

6. Publish first releases for `grcli`, `gemara-react`, `grc-store-clientkit`, and `gemara-ai`.
7. Write up how adopters use Gemara, starting with CloudNativePG, then OpenSSF Scorecard, IBM, and FINOS.
8. Schedule a code search for spec adopters and save the results in `gemaraproj/community`.
9. Record LFX metrics quarterly to see how attendance and contributor representation change over time.

---

<details>
<summary>Method and caveats</summary>

- Pulled 2026-11-17 via GitHub REST + GraphQL. Window 2026-08-19 → 2026-11-17. Archived repos excluded (`gemara-staging`, `gemara-hub`, `grcli-staging`).
- "Contributor" = author of a merged PR. Commit-only and issue-only participants are not counted, so the all-time 31 undercounts participation.
- Bots (`dependabot`, `coderabbitai`, `github-actions`, `copilot-pull-request-reviewer`, `kusari-inspector`) excluded from human counts.
- Issue first-response = first non-author, non-bot comment. Sampled from 100 most recent issues per repo; coverage complete for the window.
- Review counts sample the 100 most recently updated merged PRs per repo; `gemara` and `go-gemara` may be slightly undercounted.
- Adoption measured two ways: code search for `gemaraproj/go-gemara` in `go.mod`, and for `gemara` in `security-insights.yml`. Code search indexes only public, non-forked, active repos — both are floors, not totals. Mirrors and forks discounted by hand (`codacy-open-source-projects-scans/cloudnative-pg`, `ydnmu/scorecard`).
- The talks and media links in section 5 were not all checked individually.

</details>
