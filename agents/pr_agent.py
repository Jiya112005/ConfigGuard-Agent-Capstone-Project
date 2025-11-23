import os
import time
from github import Github
from dotenv import load_dotenv

class PRAgent: #Pull request agent
    def __init__(self):
        load_dotenv()
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("TARGET_REPO")
        self.client=Github(self.github_token)
    def create_pull_request(self,fixed_yaml_content,file_path="app_config.yaml"):
        """ Creates a new branch, commits the fix , and opens a PULL REQUEST (PR)"""
        print(f"PR AGENT: Preparing to push fixes ")
        try:
            repo=self.client.get_repo(self.repo_name)
            source_branch = repo.get_branch("main")
            
            branch_name = f"fix/drift-{int(time.time())}"
            print(f" -> Creating branch: {branch_name}")
            repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=source_branch.commit.sha
            )
            print(f"-> Committing changes to {file_path}...")
            contents = repo.get_contents(file_path,ref="main")
            
            repo.update_file(
                path=contents.path,
                message = "AI-Agent: Remediation of configuration drift",
                content = fixed_yaml_content,
                sha=contents.sha,
                branch=branch_name
            )
            
            print("-> Opening Pull Request....")
            pr_title = "Security Fix: Configuration Drift Detected"
            pr_body = (
                "### Automated Fix Report\n"
                "My audit detected configuration drift in `app_config.yaml`.\n\n"
                "**Changes Applied:**\n"
                "- Reverted drifted values to the Intended State.\n"
                "- Enforced security compliance (e.g.,`debug:false`).\n\n"
                "Please review and merge."
            )
            pr = repo.create_pull(
                title = pr_title,
                body=pr_body,
                head=branch_name,
                base="main"
            )
            
            print(f"PR Created Successfully! URL:{pr.html_url}")
            return pr.html_url
            
        except Exception as e:
            print(f"PR Agent failed: {e}")
            return None