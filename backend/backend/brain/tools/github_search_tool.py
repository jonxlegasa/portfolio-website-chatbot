import os
from typing import Dict

from dotenv import load_dotenv
from github import Auth, Github
from pydantic import Field

# load api api_key
load_dotenv()
api_key = os.getenv("GITHUB_API_KEY")
auth = Auth.Token(str(api_key))


def call_github_api() -> Dict:
    """This function makes API calls to github. This function receives a dictionary and returns a dictionary containing code repo names and descriptions"""

    github_data = {}
    # Initialize the GitHub object with authentication
    g = Github(auth=auth)
    # Dictionary to store GitHub data

    # Retrieve and store data for each repository
    for repo in g.get_user().get_repos():
        # Using the repository name as a key, and storing name and description in a sub-dictionary
        github_data[repo.name] = {
            "repo_name": repo.full_name,
            "repo_description": repo.description,
        }

    # Optional: Close the GitHub session if necessary
    g.close()

    return github_data
