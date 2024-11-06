import os
import requests
from datetime import datetime, timezone
from github import Github

GITHUB_TOKEN = os.getenv("CISA_10")  # GitHub Actions token
REPO_NAME = 'ums91/CISA10'
CISA_JSON_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

def fetch_latest_vulnerabilities():
    response = requests.get(CISA_JSON_URL)
    response.raise_for_status()
    data = response.json()
    vulnerabilities = data.get("vulnerabilities", [])
    vulnerabilities.sort(key=lambda x: x.get('dateAdded', ''), reverse=True)
    return vulnerabilities[:10]

def update_readme_content(vulnerabilities):
    readme_content = "# Known Exploited Vulnerabilities\n\n"
    readme_content += f"Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
    
    for vulnerability in vulnerabilities:
        readme_content += f"## {vulnerability.get('cveID', 'N/A')}\n"
        readme_content += f"**Vendor:** {vulnerability.get('vendorProject', 'N/A')}\n\n"
        readme_content += f"**Product:** {vulnerability.get('product', 'N/A')}\n\n"
        readme_content += f"**Description:** {vulnerability.get('vulnerabilityName', 'N/A')}\n\n"
        readme_content += f"**Date Added:** {vulnerability.get('dateAdded', 'N/A')}\n\n"
        readme_content += "---\n\n"
        
    return readme_content

def update_github_readme(content):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Debug: List all files in the repository to confirm correct path
    try:
        contents = repo.get_contents("")
        print("Repository contents:")
        for content_file in contents:
            print(content_file.path)  # Print paths of all files in the root directory

        # Try accessing the README file directly
        try:
            readme = repo.get_contents("README.md")
            repo.update_file(readme.path, "Update README with latest CISA vulnerabilities", content, readme.sha)
            print("README file updated successfully.")
        except Exception as e:
            print("README not found, attempting to create it.")
            repo.create_file("README.md", "Create README with latest CISA vulnerabilities", content)
            print("README file created successfully.")
    except Exception as e:
        print(f"Error listing repository contents: {e}")
        raise e

def main():
    vulnerabilities = fetch_latest_vulnerabilities()
    readme_content = update_readme_content(vulnerabilities)
    update_github_readme(readme_content)

if __name__ == "__main__":
    main()
