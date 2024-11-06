import os
import requests
from datetime import datetime
from github import Github

# Set up your GitHub token and repository details
GITHUB_TOKEN = os.getenv("CISA_10")  # Will be set by GitHub Actions
REPO_NAME = 'ums91/CISA10'

# Direct JSON endpoint for CISA KEV catalog
CISA_JSON_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

# Fetch the latest vulnerabilities from CISA with error handling
def fetch_latest_vulnerabilities():
    response = requests.get(CISA_JSON_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from CISA. Status code: {response.status_code}")
    
    try:
        data = response.json()  # Parse JSON response directly
    except requests.exceptions.JSONDecodeError as e:
        raise Exception(f"JSON decode error: {e}. Response content: {response.text}")
    
    # Extract vulnerabilities and sort by date added in descending order
    vulnerabilities = data.get("vulnerabilities", [])
    vulnerabilities.sort(key=lambda x: x.get('dateAdded', ''), reverse=True)
    return vulnerabilities[:10]  # Return the latest 10 vulnerabilities

# Update README content with the latest vulnerabilities
def update_readme_content(vulnerabilities):
    readme_content = "# Known Exploited Vulnerabilities\n\n"
    readme_content += f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
    
    for vulnerability in vulnerabilities:
        readme_content += f"## {vulnerability.get('cveID', 'N/A')}\n"
        readme_content += f"**Vendor:** {vulnerability.get('vendorProject', 'N/A')}\n\n"
        readme_content += f"**Product:** {vulnerability.get('product', 'N/A')}\n\n"
        readme_content += f"**Description:** {vulnerability.get('vulnerabilityName', 'N/A')}\n\n"
        readme_content += f"**Date Added:** {vulnerability.get('dateAdded', 'N/A')}\n\n"
        readme_content += "---\n\n"
        
    return readme_content

# Push updates to README in GitHub repository
def update_github_readme(content):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    readme = repo.get_contents("README.md")
    repo.update_file(readme.path, "Update README with latest CISA vulnerabilities", content, readme.sha)

# Main function to update the README
def main():
    vulnerabilities = fetch_latest_vulnerabilities()
    readme_content = update_readme_content(vulnerabilities)
    update_github_readme(readme_content)

if __name__ == "__main__":
    main()
