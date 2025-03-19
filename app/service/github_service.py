import os
import shutil
import time
from fastapi import FastAPI
from github import Github
import git

from core.config import settings

print(settings.GITHUB_ACCESS_TOKEN)
g = Github(settings.GITHUB_ACCESS_TOKEN)


class GithubManager:
    @staticmethod
    def fork_repo(repo_link: str):
       
        try:
            repo = g.get_repo(repo_link)
            forked_repo = repo.create_fork()
            print(f" Forked repo: {forked_repo.full_name}")
            return forked_repo.full_name
        except Exception as e:
            print(f" Error while forking repo: {e}")
            return None

    @staticmethod
    async def clone_repo(username: str, repo_name: str):
        """Clone a public forked GitHub repository (No authentication required)."""
        try:
            repo_url = f"https://github.com/{username}/{repo_name}.git"
            local_path = os.path.join(os.getcwd(), repo_name)

            if os.path.exists(local_path):
                shutil.rmtree(local_path)

            git.Repo.clone_from(repo_url, local_path)
            print(f"Cloned repo to {local_path}")
            return local_path
        except Exception as e:
            print(f" Error while cloning repo: {e}")
            return None

    @staticmethod
    async def push_repo(local_path: str):
        try:
            repo = git.Repo(local_path)
            repo.git.add(A=True)
            repo.index.commit("Automated update via FastAPI")
            origin = repo.remote(name="origin")
            origin.push()

            repo_name = repo.remotes.origin.url.split("/")[-1].replace(".git", "")
            print(f"✅ Changes pushed to {repo_name}")
            return repo_name
        except Exception as e:
            print(f" Error while pushing repo: {e}")
            return None

    @staticmethod
    async def create_pull_request(token: str, username: str, repo_owner: str, repo_name: str):
        g = Github(token)
        try:
            original_repo = g.get_repo(f"{repo_owner}/{repo_name}")
            forked_repo = g.get_repo(f"{username}/{repo_name}")

            pr = original_repo.create_pull(
                title="Automated PR - Internationalization Update",
                body="This PR contains automated updates for i18n.",
                head=f"{username}:main",
                base="main",
            )

            print("sucees")
            return pr.html_url
        except Exception as e:
            print(f" Error while creating pull request: {e}")
            return None

