import requests
import github
from github import Github
import os
from datetime import datetime
import base64
import json

# GitHub repository settings
REPO_NAME = "CISA10"
OWNER_NAME = "ums91"
GITHUB_TOKEN = os.getenv("CISA_10")  # GitHub token stored in your environment variables

# URL for the CISA KEV JSON feed
CISA_VULNERABILITIES_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

# Fetch CISA vulnerabilities from the JSON feed
def fetch_cisa_vulnerabilities():
    try:
        response = requests.get(CISA_VULNERABILITIES_URL)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        vulnerabilities = response.json()  # Parse the JSON response
        return vulnerabilities
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CISA vulnerabilities: {e}")
        raise

# Update the README with the latest vulnerabilities
def update_github_readme(content):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")
        
        # Check if README exists
        try:
            readme = repo.get_contents("README.md")
            print("README file found, attempting to update.")
            repo.update_file(readme.path, "Update README with latest CISA vulnerabilities", content, readme.sha)
        except github.GithubException.UnknownObjectException:
            print("README file not found, attempting to create it.")
            repo.create_file("README.md", "Create README with latest CISA vulnerabilities", content)
    except Exception as e:
        print(f"Error updating or creating README file: {e}")
        raise

# Format the vulnerabilities for the README
def format_vulnerabilities_for_readme(vulnerabilities):
    today = datetime.today().strftime("%Y-%m-%d")
    readme_content = f"# CISA Vulnerabilities - {today}\n\n"
    readme_content += "## Latest CISA Known Exploited Vulnerabilities\n\n"
    
    # Get the first 10 vulnerabilities
    for vuln in vulnerabilities[:10]:
        id = vuln.get("cisaID", "N/A")
        title = vuln.get("title", "No Title")
        description = vuln.get("description", "No Description")
        date_added = vuln.get("dateAdded", "N/A")
        
        readme_content += f"### {id} - {title}\n"
        readme_content += f"**Description:** {description}\n"
        readme_content += f"**Date Added:** {date_added}\n\n"
    
    return readme_content

# Main function
def main():
    # Fetch the latest vulnerabilities
    vulnerabilities = fetch_cisa_vulnerabilities()
    
    # Format the content for the README
    readme_content = format_vulnerabilities_for_readme(vulnerabilities)
    
    # Update the README with the new content
    update_github_readme(readme_content)

# Run the script
if __name__ == "__main__":
    main()
