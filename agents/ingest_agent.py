import os
import yaml
from github import Github
from dotenv import load_dotenv

class IngestAgent:
    def __init__(self):
        load_dotenv()
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("TARGET_REPO")
        self.client = Github(self.github_token)
    
    def fetch_remote_config(self,file_path="k8s-specifications/vote-deployment.yaml"):
        """ 
        Connects to Github and retrieves the "Actual" state of the config.
        """
        print(f"Connecting to Github Repo:{self.repo_name}...")
        try:
            repo = self.client.get_repo(self.repo_name)
            file_content = repo.get_contents(file_path)
            
            yaml_content = file_content.decoded_content.decode("utf-8")
            
            config_dict = yaml.safe_load(yaml_content)
            
            print(f"Successfully fetched {file_path}")
            return config_dict
        except Exception as e:
            print(f"Error fetching the file:{e}")
            return None
    
    def load_intended_config(self,local_path="config/intended_state.yaml"):
        """Loads the 'Golden State' (desired state) from the local directory. """
        try:
            with open(local_path,"r") as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading local config: {e}")
            return None