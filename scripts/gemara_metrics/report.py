"""Assembles the metrics JSON the workflow commits.

This is the contract between the collector and whoever writes the prose.
Nothing here decides what a number means — it decides what gets measured,
what gets linked out to LFX Insights, and what is kept by hand.
"""

from . import aggregate


def _in_window(prs, start, end):
    return [pr for pr in prs if pr.get("merged_at") and start <= pr["merged_at"][:10] <= end]


def build(org, window, generated_at, repos, prs_all_time, issues_window, reviews_window, adopters):
    start, end = window
    merged_in_window = _in_window(prs_all_time, start, end)
    cohort = aggregate.new_contributors(prs_all_time, start, end)

    human_authors = sorted({
        pr["author"] for pr in merged_in_window if not pr.get("author_is_bot")
    })
    all_time_humans = sorted({
        pr["author"] for pr in prs_all_time
        if pr.get("merged_at") and not pr.get("author_is_bot")
    })

    return {
        "meta": {
            "org": org,
            "window_start": start,
            "window_end": end,
            "generated_at": generated_at,
            "repos_in_scope": len(repos),
            "collector": "scripts/collect.py",
            "auth": "workflow GITHUB_TOKEN, public data only",
        },
        "scale": {
            "merged_in_window": aggregate.merge_velocity(merged_in_window),
            "human_pr_authors_in_window": len(human_authors),
            "human_contributors_all_time": len(all_time_humans),
            "open_issues": sum(r.get("open_issues", 0) for r in repos),
            "open_prs": sum(r.get("open_prs", 0) for r in repos),
            "forks": sum(r.get("forks", 0) for r in repos),
            "releases_all_time": sum(r.get("releases", 0) for r in repos),
            "per_repo": [
                {
                    "name": r["name"],
                    "forks": r.get("forks", 0),
                    "open_issues": r.get("open_issues", 0),
                    "open_prs": r.get("open_prs", 0),
                    "releases": r.get("releases", 0),
                    "merged_in_window": len([p for p in merged_in_window if p["repo"] == r["name"]]),
                }
                for r in repos
            ],
        },
        "new_contributors": {
            "count": len(cohort),
            "cohort": cohort,
        },
        "responsiveness": aggregate.responsiveness(issues_window),
        "reviews": aggregate.review_concentration(reviews_window),
        "ease_of_entry": aggregate.ease_of_entry(repos),
        "adoption": {
            "source": adopters.get("source"),
            "method": (
                "Curated by hand in data/adopters.json. Automating this needs "
                "cross-org code search, which the workflow's GITHUB_TOKEN cannot do; "
                "adding a PAT was judged not worth the secret. Treat the list as a "
                "floor, not a total."
            ),
            "spec": adopters.get("spec", []),
            "sdk": adopters.get("sdk", []),
        },
        "lfx_insights": aggregate.lfx_insights(),
    }
