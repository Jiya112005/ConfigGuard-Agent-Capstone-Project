import os
import google.generativeai as genai
from dotenv import load_dotenv

class FixerAgent:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ Error: GEMINI_API_KEY not found in .env")
        
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_fix(self, yaml_content, drift_report, audit_report):
        """
        Sends the broken YAML + the error report to Gemini and asks for a fixed version.
        """
        print(" Fixer Agent (Gemini): Generating remediation code...")

        prompt = self._construct_prompt(yaml_content, drift_report, audit_report)
        
        try:
            full_prompt = (
                "SYSTEM: You are a Senior DevOps Engineer. Your goal is to fix configuration files. "
                "Output ONLY valid YAML code. Do not include markdown formatting (like ```yaml), "
                "do not include explanations. Just the raw YAML text.\n\n"
                f"USER: {prompt}"
            )

            response = self.model.generate_content(full_prompt)
            
            fixed_yaml = response.text.strip()
            
            
            if "```yaml" in fixed_yaml:
                fixed_yaml = fixed_yaml.replace("```yaml", "").replace("```", "")
            elif "```" in fixed_yaml:
                fixed_yaml = fixed_yaml.replace("```", "")
                
            return fixed_yaml.strip()
            
        except Exception as e:
            print(f"❌ Fix generation failed: {e}")
            return None

    def _construct_prompt(self, yaml_content, drift_report, audit_report):
        prompt = f"""
        I have a YAML configuration file that has drifted from its intended state and failed security audits.
        
        CURRENT YAML:
        {yaml_content}
        
        ISSUES TO FIX:
        """
        
        if drift_report:
            prompt += "\n--- DRIFT (Must match intended state) ---\n"
            for item in drift_report:
                prompt += f"- {item}\n"
                
        if audit_report and audit_report.get('security_issues'):
            prompt += "\n--- SECURITY/QUALITY VIOLATIONS ---\n"
            for issue in audit_report.get('security_issues', []):
                prompt += f"- {issue['desc']}\n"
                
        prompt += "\nReturn the fully corrected YAML file. Do not omit any existing valid keys."
        return prompt 