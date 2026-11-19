"""GraphQL documents. No logic lives here.

Split deliberately: the all-time pull-request query stays light because it
only exists to find each contributor's first merge, while reviews are fetched
only for the window. Asking for reviews across all of history multiplies the
node count for data no section uses.
"""

REPO_OVERVIEW = """
query($owner:String!, $name:String!) {
  repository(owner:$owner, name:$name) {
    name
    description
    isArchived
    forkCount
    hasDiscussionsEnabled
    licenseInfo { spdxId }
    repositoryTopics(first: 20) { nodes { topic { name } } }
    openIssues: issues(states: OPEN) { totalCount }
    openPRs: pullRequests(states: OPEN) { totalCount }
    releases { totalCount }
    goodFirstIssues: issues(states: OPEN, labels: ["good first issue"]) { totalCount }
    helpWanted: issues(states: OPEN, labels: ["help wanted"]) { totalCount }
    contributing: object(expression: "HEAD:CONTRIBUTING.md") { __typename }
    contributingDotGithub: object(expression: "HEAD:.github/CONTRIBUTING.md") { __typename }
    issueTemplates: object(expression: "HEAD:.github/ISSUE_TEMPLATE") { __typename }
    securityInsights: object(expression: "HEAD:security-insights.yml") { __typename }
    securityInsightsDotGithub: object(expression: "HEAD:.github/security-insights.yml") { __typename }
  }
}
"""

MERGED_PRS_ALL_TIME = """
query($owner:String!, $name:String!, $pageSize:Int!, $cursor:String) {
  repository(owner:$owner, name:$name) {
    items: pullRequests(states: MERGED, first: $pageSize, after: $cursor,
                        orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        number
        createdAt
        mergedAt
        author { login __typename }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""

MERGED_PRS_WITH_REVIEWS = """
query($owner:String!, $name:String!, $pageSize:Int!, $cursor:String) {
  repository(owner:$owner, name:$name) {
    items: pullRequests(states: MERGED, first: $pageSize, after: $cursor,
                        orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        number
        createdAt
        mergedAt
        author { login __typename }
        reviews(first: 50) {
          nodes { submittedAt author { login __typename } }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""

ISSUES = """
query($owner:String!, $name:String!, $pageSize:Int!, $cursor:String) {
  repository(owner:$owner, name:$name) {
    items: issues(first: $pageSize, after: $cursor,
                  orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        number
        createdAt
        author { login __typename }
        comments(first: 20) {
          nodes { createdAt author { login __typename } }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""
