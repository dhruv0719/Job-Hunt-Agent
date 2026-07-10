# app/ingestion/loader/github_info.py

from github import Github, GithubException, Auth

# Using an access token
auth = Auth.Token("access_token")

print(auth)
