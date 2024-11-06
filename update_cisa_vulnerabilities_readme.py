import requests
from datetime import datetime
from github import Github

# Set up your GitHub token and repository details
GITHUB_TOKEN = 'your_github_token'
REPO_NAME = 'your_username/your_repository'  # e.g., 'ums91/Wolfpack'

# API endpoint for CISA KEV catalog
CISA_API_URL = "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"

# Fetch the latest vulnerabilities from CISA
def fetch_latest_vulnerabilities():
    response = requests.get(CISA_API_URL)
    response.raise_for_status()
    vulnerabilities = response.json()  # Assumes JSON response format
    vulnerabilities.sort(key=lambda x: x['dateAdded'], reverse=True)
    return vulnerabilities[:10]

# Update README content with the latest vulnerabilities
def update_readme_content(vulnerabilities):
    readme_content = "# Known Exploited Vulnerabilities\n\n"
    readme_content += f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
    
    for vulnerability in vulnerabilities:
        readme_content += f"## {vulnerability['cveID']}\n"
        readme_content += f"**Vendor:** {vulnerability['vendorProject']}\n\n"
        readme_content += f"**Product:** {vulnerability['product']}\n\n"
        readme_content += f"**Description:** {vulnerability['vulnerabilityName']}\n\n"
        readme_content += f"**Date Added:** {vulnerability['dateAdded']}\n\n"
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
