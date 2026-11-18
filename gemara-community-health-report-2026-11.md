# Gemara Community Health Report — November 2026

**Window:** 90 days, 2026-08-19 → 2026-11-17 · **Scope:** 14 active `gemaraproj` repos · **Source:** GitHub REST + GraphQL, pulled 2026-11-17

---

## TL;DR

**Gemara is growing fast on intake and lagging on response. The bottleneck is maintainer throughput, not interest.**

| Signal | Number | Read |
|---|---|---|
| New contributors (first-ever merged PR) | **12** in 90d (7 in last 30) | 39% of all 31 all-time contributors arrived this quarter |
| Issues with no human reply | **60%** (57 of 95) | Median first response **8.3 days** |
| Review concentration | **3 people = 82%** of reviews | Bus factor of 3 |
| External spec adopters | **CloudNativePG, wasmCloud, Capsule, OpenSSF Scorecard** | Reach beyond the GRC orbit — currently unmeasured |
| On-ramp supply | **5** open `good first issue`s, **0** repos with GitHub topics | Demand exceeds supply; project is undiscoverable by topic search |

**The shape of the problem:** if you already know what to build, Gemara merges your work in ~19 hours. If you arrive with a question, you are ignored for over a week. That filters out exactly the newcomers the project wants.

**Three asks of leadership:**
1. **Maintainer capacity** — promote 5 already-active volunteer reviewers up the contributor ladder with scoped merge rights.
2. **LFX Insights coverage** — Insights tracks 1 of 14 repos, under the stale `ossf/gemara` name. Needs an LF ticket.
3. **Adoption narrative** — four CNCF/OpenSSF projects adopt the spec without the SDK. This is the strongest proof point in the report and it is neither tracked nor published.

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

**Backlog is growing** and concentrated: `gemara` (39 open PRs) and `website` (19) hold **70% of all open PRs**. `website` has more open PRs than open issues — contributions arriving faster than review.

Forks, not stars, are the activity signal: `gemara` 31, `go-gemara` 18, `gemara-mcp` 11, `website` 11.

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

## 2. New contributors — the strongest signal

| Period | New contributors |
|---|---:|
| 2025 (full year) | 12 |
| 2026 Jan–Aug 18 | 7 |
| **2026 Aug 19 – Nov 17** | **12** (7 in last 30d) |

**Several are already reviewing and triaging, not just submitting** — `nameetsinha7-hue` (7 reviews), `YAshhh29` (6 reviews), `harshsomankar123-tech` (6 issue first-responses), `imshubham22apr-gif` (3). The on-ramp is producing participants, not drive-bys.

**Retention risk:** the cohort's work is concentrated in `gemara` and `website` — the same two repos holding the 58-deep PR backlog. If it stalls there, the cohort evaporates.

<details>
<summary>90-day cohort, by first merge date</summary>

`PaarthPandey10` (09-10), `astrogilda` (09-15), `gxmiranda` (09-30), `kocaemre` (10-02), `vansh-nagar` (10-05), `jor2` (10-24), `YAshhh29` (10-25), `harshsomankar123-tech` (10-28), `nameetsinha7-hue` (10-29), `ravindra-RKB` (10-30), `yvonnedevlinrh` (11-07), `imshubham22apr-gif` (11-10)

</details>

---

## 3. Maintainer load and bus factor

**Top 3 reviewers = 82% of all human reviews:** `jpower432` (74, 50%), `jmeridth` (29, 20%), `eddie-knight` (19, 13%). Bots (`coderabbitai` 15, Copilot 3) supplement but don't substitute.

`jmeridth` authored merged PRs in **all 14 repos** — the only person with org-wide coverage, and a single point of failure for cross-repo maintenance.

Of 8 GitHub org members, **3 did not review a PR in 90 days**. 27% of merged PRs (39 of 143) had no human review — mostly bot/chore, worth confirming none were substantive.

---

## 4. Responsiveness — the weakest area

| Issues opened last 90d | Value |
|---|---|
| Opened | 95 |
| **No human response yet** | **57 (60%)** |
| Median time to first human response | **8.3 days** |

`gemara` itself is reasonable (~2 days). Everywhere else a newcomer filing an issue should expect silence: `go-gemara` **29 days**, `community` **60 days**, `grcli` 13 days, `website` 7.5 days.

**Time to merge is far better** — median **19.4h** across non-bot PRs, with most repos under 3h. The contrast is the finding: fast merges, slow answers.

---

## 5. Ease of entry

**Cheapest fixes available:**
- **Zero repos have GitHub topics.** Nothing is discoverable by searching `grc`, `compliance`, `policy-as-code`, `supply-chain`. Minutes of work.
- **Only 5 open `good first issue`s** org-wide (11 `help wanted`) — and **none in `gemara`**, the flagship with 31 forks.
- `website` — 11 forks, 19 open PRs, **no CONTRIBUTING.md and no license**. Most contributor-facing repo, least documented.
- No description on `gemara-react`, `gemara-python`, `community`. Issue templates on only 4 of 14 repos.
- Discussions enabled on `gemara-mcp` only — questions have nowhere to go but unanswered issues.
- `gemara-mcp-eval-infra` license reads `NOASSERTION` — blocks adopter legal review.

**Org-level governance is in good shape** (`CODE_OF_CONDUCT`, `GOVERNANCE`, `CHARTER`, `MAINTAINERS`, `CONTRIBUTOR_LADDER`, `SECURITY` all inherited from `.github`). The gap is per-repo.

**Dogfooding gap:** `security-insights.yml` present in **7 of 14 repos**. For a project pitching structured security metadata, 50% self-coverage is a credibility gap — and an easy `good first issue` batch.

---

## 6. Adoption — two tracks

**SDK adoption (Go dependency graph):** 25 external repos import `go-gemara`, but concentrated in the home orbit — ComplyTime, Privateer, revanite-io, OpenSSF. The genuinely independent adopters are `IBM/ai-security-baseline`, `finos/common-cloud-controls`, `cncf/contribute-site`.

**Spec adoption (`security-insights.yml`) — the bigger story:**

| Adopter | Status |
|---|---|
| cloudnative-pg | **CNCF graduated** |
| wasmCloud | **CNCF incubating** |
| projectcapsule/capsule | CNCF sandbox |
| ossf/scorecard | OpenSSF flagship |

These four use the format **without importing the Go library** — invisible to the dependency graph, and reaching outside the GRC-tooling orbit in a way SDK adoption does not. CloudNativePG's use is independently documented in [Gabriele Bartolini's comparison writeup](https://www.gabrielebartolini.it/articles/2026/05/cloudnativepg-and-crunchy-pgo-an-honest-opinionated-comparison/).

**It is currently untracked.** A scheduled code search, recorded in `gemaraproj/community`, would make it trendable.

**Direction of travel:** nearly every SDK adopter is a standards or assessment project, not an end-user application. Gemara is **codifying standards**, not chasing wide adoption. Legitimate — but it means growth tracks standards bodies converted, not downloads.

**Release gap:** `grcli`, `gemara-react`, `grc-store-clientkit`, `gemara-ai` have **never cut a release** despite active development. Users cannot pin a version.

---

## 7. Visibility — reach exists, the loop is open

2026 saw talks at **OpenSSF Community Day NA and EU**, **DevConf CZ**, and **KubeCon NA SecurityCon**, plus OpenSSF blog coverage (including [CRA due diligence](https://openssf.org/blog/2026/10/22/who-checked-it-attestations-gemara-and-cra-due-diligence/)) and third-party mentions from CUE Labs and CloudNativePG.

**Gap: none of it is linked from the repos.** No talks/media page on `website`, no README mention, not in `awesome-gemara`. A viewer who hears a talk has no path back to a first issue.

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

## 8. Initiatives

- **Security Slam 2026** — Gemara is wired in from the outside (`pvtr-security-slam-review` imports `go-gemara`; Slam repos carry Gemara `security-insights.yml`). Open question: **are Gemara's own repos entered, and would they pass?** With 7 of 14 missing `security-insights.yml` and only 2 carrying a `SECURITY.md`, entering now would score poorly. Fixing the dogfooding gap is a prerequisite.
- **Mentorship (LFX)** — the 12-person cohort suggests mentorship-style intake is already happening informally, with no tracking issue or board.
- **OpenSSF WG participation** — not measurable from repo data.

---

## 9. LFX Insights — coverage is broken

Gemara appears in Insights as **a single repo inside the OpenSSF collection, under its old path** (`ossf/gemara`). [Primary link, past 365 days](https://insights.linuxfoundation.org/project/openssf/repository/ossf_gemara?timeRange=past365days&start=2025-11-16&end=2026-11-16). There is no standalone `/project/gemara` page.

1. **Stale URL.** `ossf/gemara` redirects to `gemaraproj/gemara` — data likely still flows, but the name and link mislead anyone evaluating the project.
2. **1 of 14 repos tracked.** Every number in this report outside the flagship repo is invisible to LFX. Request the `gemaraproj` org be added to the OpenSSF collection.

**Five metrics LFX could give us that GitHub cannot — all currently uncollected:** contributor count by employer, active maintainers with merge rights, community meeting attendance, per-repo Scorecard, contributor retention.

Note: the public OpenSSF org figures (23 maintainers, 122 orgs, Scorecard 7.3) cover **all of OpenSSF**, not Gemara, and should not be quoted as ours.

---

## Recommendations

Ordered by leverage per hour.

**This week — minutes to hours each**
1. Set **GitHub topics on all 14 repos** (`grc`, `compliance`, `security`, `policy-as-code`, `supply-chain`, `openssf`).
2. Add **descriptions** to `gemara-react`, `gemara-python`, `community`.
3. **Triage the 57 unanswered issues** — a one-line ack resets the 8.3-day median. Start with `go-gemara` and `community`.
4. Fix **`gemara-mcp-eval-infra`'s license** to a recognized SPDX identifier.
5. **File the LF Insights ticket** — correct the URL, add the other 13 repos.

**This month — structural**
6. Create **15–20 `good first issue`s**, 5+ in `gemara`. Natural batch: add `security-insights.yml` to the 7 repos missing it (on-ramp work that also closes the dogfooding gap).
7. Add **CONTRIBUTING.md and a license to `website`**.
8. **Burn down the `gemara` + `website` PR backlog** (58 of 83 open PRs) — where the new cohort's work is sitting.
9. **Enable Discussions org-wide.**
10. **Add a talks/media page** to `website`, linked from the `gemara` README.

**This quarter — sustainability**
11. **Expand the reviewer pool past 3.** `nameetsinha7-hue`, `YAshhh29`, `harshsomankar123-tech`, `astrogilda`, `sonupreetam` already review voluntarily — formalize via the contributor ladder with scoped merge rights.
12. **Reduce `jmeridth`'s single-point-of-failure exposure** with per-repo CODEOWNERS.
13. **Cut first releases** for `grcli`, `gemara-react`, `grc-store-clientkit`, `gemara-ai`.
14. **Write adopter case studies** — CloudNativePG first (CNCF graduated, public writeup to cite), then wasmCloud, OpenSSF Scorecard, IBM, FINOS, Capsule.
15. **Automate spec-adoption tracking** via scheduled code search committed to `gemaraproj/community`.
16. **Record LFX metrics quarterly** so attendance and org diversity become trendable.

---

<details>
<summary>Method and caveats</summary>

- Pulled 2026-11-17 via GitHub REST + GraphQL. Window 2026-08-19 → 2026-11-17. Archived repos excluded (`gemara-staging`, `gemara-hub`, `grcli-staging`).
- "Contributor" = author of a merged PR. Commit-only and issue-only participants are not counted, so the all-time 31 undercounts participation.
- Bots (`dependabot`, `coderabbitai`, `github-actions`, `copilot-pull-request-reviewer`, `kusari-inspector`) excluded from human counts.
- Issue first-response = first non-author, non-bot comment. Sampled from 100 most recent issues per repo; coverage complete for the window.
- Review counts sample the 100 most recently updated merged PRs per repo; `gemara` and `go-gemara` may be slightly undercounted.
- Adoption measured two ways: code search for `gemaraproj/go-gemara` in `go.mod`, and for `gemara` in `security-insights.yml`. Code search indexes only public, non-forked, active repos — both are floors, not totals. Mirrors and forks discounted by hand (`codacy-open-source-projects-scans/cloudnative-pg`, `ydnmu/scorecard`).
- §7 links come from provided notes; URLs were not individually fetched to confirm they resolve.
- §8 initiative status is partly inferred, partly unmeasured.

</details>
