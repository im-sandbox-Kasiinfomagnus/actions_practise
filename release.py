import requests
 
# Set the source and destination repository URLs
src_repo_url = "https://api.github.com/repos/ORGNAME/REPO/releases"
 
# Set the authentication tokens for the repositories (if required)
src_token = "sourcetoken"
 
 
 
# Get the release information from the source repository
response = requests.get(src_repo_url, headers={"Authorization": f"Bearer {src_token}"})
src_releases = response.json()
 
 
# Filter out draft releases and extract the release tags and assets from the source repository
src_tags = []
src_assets = {}
for release in src_releases:
    if not release["draft"]:
        src_tags.append(release["tag_name"])
        src_assets[release["tag_name"]] = [asset["name"] for asset in release["assets"]]
 
 
print(release)
