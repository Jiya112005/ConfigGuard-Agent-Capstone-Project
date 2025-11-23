import subprocess 
import json 
import os 

class AuditAgent:
    def __init__(self):
        pass
    def run_audit(self,file_path):
        """ Runs the Third party tools against the file. """
        print(f"Audit Agent: Scanning {file_path} for security & quality_issues...")
        security_issues = self._run_checkov(file_path) or []
        quality_issues = self._run_yamllint(file_path) or []
        report = {
            "security_issues":security_issues,
            "quality_issues":quality_issues
        }
        self._print_summary(report)
        return report 
    
    
    def _run_checkov(self,file_path):
        """ Runs Checkov to find security vulnerabilities.
        """
        try:
            cmd=["checkov","-f",file_path,"-o","json","--quiet"]
            result = subprocess.run(cmd,shell=True,capture_output=True,text=True)
            
            if not result.stdout.strip():
                return []
            
            output = json.loads(result.stdout)
            
            if isinstance(output,list):
                output = output[0]
                
            failed_checks = output.get("results",{}).get("failed_checks",[])
            issues=[]
            
            for check in failed_checks:
                issues.append({
                    "id":check['check_id'],
                    "desc":check['check_name'],
                    "severity":"HIGH"
                })
            return issues
        except Exception as e:
            print(f"Checkov failed to run:{e}")
            return []
        
        
    def _run_yamllint(self,file_path):
        """ 
            Runs Yamllint to find syntax and Quality errors
        """
        try:
            cmd = ["yamllint","-f","parsable",file_path]
            result = subprocess.run(cmd,shell=True,capture_output=True,text=True)
            issues = []
            for line in result.stdout.splitlines():
                parts = line.split(":",4)
                if len(parts)>=5:
                    issues.append({
                        "line":parts[1],
                        "type":parts[3].strip("[]").title(),
                        "desc":parts[4].strip()
                    })
            return issues 
        except Exception as e:
            print(f"Yamllint failed to run:{e}")
            return []
    def _print_summary(self,report):
        total_security = len(report['security_issues'])
        total_quality = len(report['quality_issues'])
        
        if total_security > 0:
            print(f"Found {total_security} SECURITY vulnerabilities!")
            for issue in report['security_issues']:
                print(f" -[{issue['id']}]{issue['desc']}")
        
        if total_quality > 0:
            print(f"Found {total_quality} QUALITY issues.")