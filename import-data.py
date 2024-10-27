import requests

# Set your GitHub token and headers
GITHUB_TOKEN = "Inventory_secrets"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Helper function to send requests and return JSON response
def github_api_request(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# Get CODEOWNERS per repo
def get_codeowners(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/CODEOWNERS"
    try:
        codeowners = github_api_request(url)
        return codeowners['download_url']
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return "CODEOWNERS file not found."
        else:
            raise

# Get Actions workflows per repo
def get_workflows(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows"
    workflows = github_api_request(url)
    return [workflow['name'] for workflow in workflows.get('workflows', [])]

# Get LFS usage per repo
def get_lfs_usage(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/lfs"
    try:
        lfs_info = github_api_request(url)
        return "Yes" if lfs_info else "No"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return "No"
        else:
            raise

# Get releases and release attachments
def get_releases(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    releases = github_api_request(url)
    release_data = []
    for release in releases:
        release_info = {
            "tag_name": release["tag_name"],
            "release_name": release["name"],
            "published_at": release["published_at"],
            "draft": release["draft"],
            "prerelease": release["prerelease"],
            "asset_count": len(release["assets"]),
            "html_url": release["html_url"],
            "size": sum(asset["size"] for asset in release["assets"])
        }
        release_data.append(release_info)
    return release_data

# Get rulesets per organization
def get_org_rulesets(org):
    url = f"https://api.github.com/orgs/{org}/rulesets"
    try:
        rulesets = github_api_request(url)
        return [{"name": ruleset["name"], "json": ruleset} for ruleset in rulesets]
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return "No rulesets found for this org."
        else:
            raise

# Get rulesets per repo
def get_repo_rulesets(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/rulesets"
    try:
        rulesets = github_api_request(url)
        return [{"name": ruleset["name"], "json": ruleset} for ruleset in rulesets]
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return "No rulesets found for this repo."
        else:
            raise

# Example usage
owner = "kasiinfomagnus"
repo = "actions_practise"
org = "im-sandbox-Kasiinfomagnus"

# Collecting the data in the required format
data = {}

# Repository, CODEOWNERS path, Pattern, Owners
codeowners_path = get_codeowners(owner, repo)
data['Repository'] = repo
data['CODEOWNERS Path'] = codeowners_path

# Repository, workflow filename
workflows = get_workflows(owner, repo)
data['Workflows'] = workflows

# Repository, LFS Y/N
lfs_usage = get_lfs_usage(owner, repo)
data['LFS Usage'] = lfs_usage

# Repository, tag_name, release_name, published_at, draft, prerelease, asset_count, html_url, size
releases = get_releases(owner, repo)
data['Releases'] = releases

# Org Rulesets: Ruleset name, ruleset JSON
org_rulesets = get_org_rulesets(org)
data['Org Rulesets'] = org_rulesets

# Repo Rulesets: Ruleset name, ruleset JSON
repo_rulesets = get_repo_rulesets(owner, repo)
data['Repo Rulesets'] = repo_rulesets

# Output the collected data
print(f"Data for repository: {repo}")
print(data)
