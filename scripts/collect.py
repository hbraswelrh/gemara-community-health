#!/usr/bin/env python3
"""Collect Gemara community health metrics into a JSON file.

Runs on the workflow's built-in GITHUB_TOKEN. Everything it reads is public
data on a public org, so there is no secret to provision or rotate.

    python3 scripts/collect.py --org gemaraproj --window 90 --out data/2026-11.json

Locally, export a token first: GH_TOKEN=$(gh auth token).

What this does not do, on purpose:

  * It does not recompute anything LFX Insights publishes. Employer
    affiliation, merge rights, meeting attendance, Scorecard and retention
    come out as links into the LFX dashboard, not as numbers. Two different
    figures for the same metric in front of the same reader is worse than
    one figure and a link.
  * It does not crawl for spec adopters. That needs cross-org code search,
    which GITHUB_TOKEN cannot do. The list is curated in data/adopters.json
    and passed straight through, labelled as a floor.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemara_metrics import aggregate, github, normalise, queries, report

DEFAULT_ADOPTERS = {"source": "data/adopters.json", "spec": [], "sdk": []}


def load_adopters(path):
    if not path or not os.path.exists(path):
        return dict(DEFAULT_ADOPTERS)
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    data.setdefault("source", path)
    return data


def active_repos(client, org):
    """Repository names in the org, archived ones dropped.

    Archived repos keep their history and would quietly pad every count.
    """
    names = []
    page_number = 1
    while True:
        batch = client.rest(
            "/orgs/{}/repos".format(org),
            {"per_page": 100, "page": page_number, "type": "public"},
        )
        if not batch:
            return names
        names.extend(repo["name"] for repo in batch if not repo.get("archived"))
        if len(batch) < 100:
            return names
        page_number += 1


def collect_repo(client, org, name, window_start, window_end, log):
    log("  {}".format(name))
    overview_node = client.graphql(
        queries.REPO_OVERVIEW, {"owner": org, "name": name}
    ).get("repository")
    if not overview_node:
        log("    skipped (not readable)")
        return None

    too_old = lambda node: (node.get("createdAt") or "")[:10] < window_start

    all_time_prs = client.paginate(
        queries.MERGED_PRS_ALL_TIME, {"owner": org, "name": name}, ["repository", "items"]
    )
    window_pr_nodes = client.paginate(
        queries.MERGED_PRS_WITH_REVIEWS, {"owner": org, "name": name},
        ["repository", "items"], page_size=50, stop_when=too_old,
    )
    issue_nodes = client.paginate(
        queries.ISSUES, {"owner": org, "name": name},
        ["repository", "items"], page_size=50, stop_when=too_old,
    )

    issues_in_window = [
        normalise.issue(node, name)
        for node in issue_nodes
        if window_start <= (node.get("createdAt") or "")[:10] <= window_end
    ]

    return {
        "overview": normalise.repo_overview(overview_node),
        "prs_all_time": [normalise.pull_request(node, name) for node in all_time_prs],
        "issues_window": issues_in_window,
        "reviews_window": normalise.reviews_in_window(
            window_pr_nodes, window_start, window_end, name
        ),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--org", default="gemaraproj")
    parser.add_argument("--window", type=int, default=90, help="window length in days")
    parser.add_argument("--end", default=None, help="last day of the window (default: today, UTC)")
    parser.add_argument("--out", required=True, help="where to write the metrics JSON")
    parser.add_argument("--adopters", default="data/adopters.json")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    log = (lambda *_: None) if args.quiet else (lambda message: print(message, file=sys.stderr))

    now = datetime.now(timezone.utc)
    end_day = args.end or now.strftime("%Y-%m-%d")
    window_start, window_end = aggregate.window_bounds(end_day, args.window)

    client = github.Client(token=os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", ""))

    log("window {} to {}".format(window_start, window_end))
    names = active_repos(client, args.org)
    log("{} active repos in {}".format(len(names), args.org))

    repos, prs_all_time, issues_window, reviews_window = [], [], [], []
    for name in names:
        collected = collect_repo(client, args.org, name, window_start, window_end, log)
        if collected is None:
            continue
        repos.append(collected["overview"])
        prs_all_time.extend(collected["prs_all_time"])
        issues_window.extend(collected["issues_window"])
        reviews_window.extend(collected["reviews_window"])

    payload = report.build(
        org=args.org,
        window=(window_start, window_end),
        generated_at=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        repos=repos,
        prs_all_time=prs_all_time,
        issues_window=issues_window,
        reviews_window=reviews_window,
        adopters=load_adopters(args.adopters),
    )

    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")

    log("wrote {}".format(args.out))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except github.GitHubError as error:
        print("collection failed: {}".format(error), file=sys.stderr)
        sys.exit(1)
