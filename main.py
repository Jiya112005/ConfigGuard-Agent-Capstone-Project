import os
from agents.ingest_agent import IngestAgent
from agents.drift_agent import DriftAgent
from agents.audit_agent import AuditAgent
from agents.fixer_agent import FixerAgent
from agents.pr_agent import PRAgent
import yaml

def main():
    ingester = IngestAgent()
    file_path = "temp_audit.yaml"
    
    actual = ingester.fetch_remote_config()
    
    intended = ingester.load_intended_config()
    if not actual or not intended:
        print("Error!,Could not Load configurations.Exiting")
        return
    
    fixed_yaml = None
    # print(f"DEBUG - Remote Debug Value: {actual.get('security', {}).get('debug')}")
    # print(f"DEBUG - Local Debug Value:  {intended.get('security', {}).get('debug')}")
    # print("--------------------------------------------------")
    
    with open(file_path,"w") as f:
        yaml.dump(actual,f)
    print(f"Saved temporary config to {file_path}")
    
    
    if actual and intended:
        drift_agent = DriftAgent()
        drift_report = drift_agent.detect_drift(intended,actual)

        # try:
        audit_agent = AuditAgent()
        audit_report = audit_agent.run_audit(file_path)
        # except Exception as e:
        #     print(f"Audit tools skipped:{e}")
        #     audit_report = {"security_issues":[],"quality_issues":[]}
        
        # print(f"Audit Report by audit agent: {audit_report}")
        print(f"Security Issues: {audit_report['security_issues']}")
        print(f"Quality Issues: {audit_report['quality_issues']}")
        if drift_report or audit_report['security_issues']:
            print("\n Issues detected! Activating Fixer Agent...")

            for issue in drift_report:
                print(issue)
            
            fixer = FixerAgent()
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    raw_yaml = f.read()
            
                fixed_yaml = fixer.generate_fix(raw_yaml, drift_report, audit_report)
        
                if fixed_yaml:
                    print("\n PROPOSED FIX:\n")
                    print(fixed_yaml)
            
            
                    with open("fixed_config.yaml", "w") as f:
                        f.write(fixed_yaml)
                    print("\n Saved fix to 'fixed_config.yaml'")
                else:
                    print(" Could not generate fix.")
            else:
                print("Error : File not found")
        else:
            print("\n System is healthy. No actions needed.")
        if fixed_yaml:
            print("MANAGER APPROVAL ")
            choice = input("[ACTION REQUIRED] Do you authorize to open a Pull Request? (y/n):")
            if choice.lower() == 'y':
                print("\n Executing PR Workflow...")
                pr_agent = PRAgent()
                pr_url=pr_agent.create_pull_request(fixed_yaml)
                if pr_url:
                    print(f"\n MISSION ACCOMPLISHED! Fix deployed:{pr_url}")
            else:
                print("\n Action Denied. The agent will NOT modify the repository.")
                
                    
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    main()