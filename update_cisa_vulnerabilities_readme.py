import requests
from github import Github, GithubException
import os
from datetime import datetime

# GitHub authentication using the repository secret token
token = os.getenv('CISA_10')  # Make sure you have the correct environment variable set
g = Github(token)

# CISA KEV feed URL
CISA_FEED_URL = 'https://www.cisa.gov/sites/default/files/feeds/kev.csv'

# Function to fetch CISA vulnerabilities from the KEV feed
def fetch_cisa_vulnerabilities():
    response = requests.get(CISA_FEED_URL)
    response.raise_for_status()  # Raises an HTTPError if the response was an error
    vulnerabilities = response.text.splitlines()[1:]  # Skip the header row
    return vulnerabilities

# Function to format the vulnerability data as a Markdown table
def format_vulnerabilities(vulnerabilities):
    formatted_vulns = "| CVE ID | Description | Published Date |\n"
    formatted_vulns += "|--------|-------------|----------------|\n"
    for vuln in vulnerabilities[:10]:  # Get the top 10 vulnerabilities
        cve_id, description, published_date = vuln.split(',')
        formatted_vulns += f"| {cve_id} | {description} | {published_date} |\n"
    return formatted_vulns

# Function to update or create the README file in the GitHub repository
def update_github_readme(content):
    try:
        repo = g.get_repo("ums91/CISA10")  # Replace with your actual repository name
        try:
            # Try to get the README file
            readme = repo.get_contents("README.md")
            print("README file found, attempting to update.")
            # Update the README with the new content
            repo.update_file(readme.path, "Update README with latest CISA vulnerabilities", content, readme.sha)
        except GithubException as e:
            # If the README file does not exist, create it
            print("README file not found, attempting to create it.")
            repo.create_file("README.md", "Create README with latest CISA vulnerabilities", content)
    except GithubException as e:
        print(f"Error updating or creating README file: {e}")

# Main function to run the process
def main():
    # Fetch the latest CISA vulnerabilities
    vulnerabilities = fetch_cisa_vulnerabilities()

    # Format the vulnerabilities as a Markdown table
    readme_content = f"# Latest CISA Vulnerabilities ({datetime.now().strftime('%Y-%m-%d')})\n\n"
    readme_content += "## Top 10 CISA Vulnerabilities\n\n"
    readme_content += format_vulnerabilities(vulnerabilities)

    # Update the README file on GitHub
    update_github_readme(readme_content)

# Run the script
if __name__ == "__main__":
    main()
