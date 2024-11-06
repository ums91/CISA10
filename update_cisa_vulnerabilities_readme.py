import requests
import json
from datetime import datetime
import os
from github import Github

# CISA vulnerabilities JSON URL
CISA_VULNERABILITIES_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
DATE_THRESHOLD = datetime(2024, 11, 1)  # The date from which to fetch vulnerabilities

# Fetch the GitHub token from GitHub Secrets
GITHUB_TOKEN = os.getenv("CISA_10")
REPO_NAME = "ums91/CISA10"  # Make sure this is correct: username/repository_name

def fetch_cisa_vulnerabilities():
    try:
        response = requests.get(CISA_VULNERABILITIES_URL)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        vulnerabilities_data = response.json()  # Parse the JSON response

        # Debugging: print the structure of the vulnerabilities object
        print(json.dumps(vulnerabilities_data, indent=2))  # Pretty print the JSON response for inspection
        
        # Access the 'vulnerabilities' key to get the list of vulnerabilities
        vulnerabilities = vulnerabilities_data.get("vulnerabilities", [])
        
        # Debugging: check the number of vulnerabilities fetched
        print(f"Total vulnerabilities fetched: {len(vulnerabilities)}")

        # Filter vulnerabilities based on published date (only include those from 1-Nov-2024 onwards)
        filtered_vulnerabilities = [
            vuln for vuln in vulnerabilities
            if datetime.strptime(vuln.get('dateAdded', ''), '%Y-%m-%d') > DATE_THRESHOLD
        ]

        print(f"Filtered vulnerabilities: {len(filtered_vulnerabilities)}")  # Debug the count of filtered vulnerabilities
        return filtered_vulnerabilities

    except requests.exceptions.RequestException as e:
        print(f"Error fetching CISA vulnerabilities: {e}")
        raise

def format_vulnerabilities_for_readme(vulnerabilities):
    readme_content = "# Latest CISA Vulnerabilities\n\n"

    # Format the latest vulnerabilities (first 10 from the filtered list)
    for vuln in vulnerabilities[:10]:
        cve_id = vuln.get('cveID', 'N/A')
        description = vuln.get('shortDescription', 'No description available')
        published_date = vuln.get('dateAdded', 'Unknown')
        
        # Debug: Print formatted content for each vulnerability
        print(f"Formatting CVE: {cve_id}, Description: {description}, Date: {published_date}")
        
        readme_content += f"### {cve_id}\n"
        readme_content += f"**Description**: {description}\n"
        readme_content += f"**Published Date**: {published_date}\n\n"

    return readme_content

def update_github_readme(content):
    try:
        print("Initializing GitHub client...")
        # Initialize the GitHub API client
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        print(f"Connected to repository: {repo.name}")

        try:
            print("Attempting to fetch README.md from the repo...")
            readme = repo.get_contents("README.md")
            print(f"README.md found with sha: {readme.sha}")
            
            # Attempt to update the README file
            repo.update_file(readme.path, "Update README with latest CISA vulnerabilities", content, readme.sha)
            print("README updated successfully.")
        except Exception as e:
            print(f"Error fetching README.md: {e}")
            print("README.md not found, creating a new one...")
            # If README doesn't exist, create it
            repo.create_file("README.md", "Create README with latest CISA vulnerabilities", content)
            print("README created successfully.")

    except Exception as e:
        print(f"Error updating or creating README file: {e}")
        raise

def main():
    vulnerabilities = fetch_cisa_vulnerabilities()
    if vulnerabilities:
        readme_content = format_vulnerabilities_for_readme(vulnerabilities)
        print(f"Generated README content:\n{readme_content}")  # Debug the generated content
        update_github_readme(readme_content)
    else:
        print("No vulnerabilities found after the date threshold.")

if __name__ == "__main__":
    main()
