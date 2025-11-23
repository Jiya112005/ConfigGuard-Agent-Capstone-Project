# Project Overview
ConfigGuard Agent is automated DevOps remediation agent designed to combat "Configuration Drift", a leading cause of cloud security incidents and system downtime. While traditional monitoring tools merely flag errors, ConfigGuard actively fixes them. It utilizes a robust sequential multi-agent architecture where Ingest and Audit agents employ deterministic tools - like DeepDiff and Checkov - to identify discrepancies against a secure "Golden State" with mathematical precision.

When violations are detected, a Fixer Agent powered by Google Gemini synthesizes a precise, context-aware YAML patch to resolve the issue.Crucially, the system bridges a gap between AI speed and enterprise safety through a "Human-in-the-Loop" workflow. Instead of blindly pushing code, the agent generates a detailed GitHub Pull Request and pauses for mandatory managerial approval.

# Problem Statement

Managing configuration files is least exciting part of software engineering, but it's where things go wrong the fastest. We call it "Configuration Drift". This happens when a secure config is deployed, but over time, manual changes (like enabling a debug flag or disabling a resource limit) are made and forgotten.

This is a "silent killer" of infrastructure. It causes security breaches and downtime that traditional monitoring tools only complain about but don't fix.

ConfigGuard solves this by building a tool that doesn't just sound the alarm but automatically puts out fire.

# Solution 

Traditional automation scripts are rigid, but they can't understand context ot write code to fix complex errors. Agents are the right solution because remediation requires reasoning and complex orchestration. 
The ConfigGuard system is modeled after a specialized human DevOps team:

- The Audit Agent runs specific, deterministic security tools.

- The Fixer Agent takes the unstructured error report from audit, uses an LLM (Gemini) to reason about the best fix, synthesis new, valid code.

- The PR Agent handles the final, crucial step: managing Git workflow, which requires understanding repository state,branches, and remote operations.
Fulfilled by using GitHub library.

# Architecture and Workflow 

The ConfigGuard system operates as a five-stage, sequential pipeline.

Agent Pipeline & Responsibilities

- Ingestion Agent:

    Role: State Gatherer.

    Action: Connects to the target GitHub repository (TARGET_REPO) via PyGithub, fetches the live configuration file (CONFIG_PATH), and stores it as the Actual State.


- Drift Agent: 

    Role: Consistency Checker.

    Action: Compares the Actual State (remote) with the Golden State (local intended_state.yaml) using the DeepDiff tool. If differences are found (e.g., image version mismatches), it generates a Drift Report.

- Audit Agent:

    Role: Security Scanner.

    Action: Runs the Checkov static analysis tool against the Actual State. It compiles a list of high-severity security and compliance violations (e.g., CKV_K8S_28 for running as root).

- Fixer Agent (LLM Core):

    Role: Remediation Synthesizer.

    Action: Receives the consolidated Drift Report and Audit Report. It uses the Gemini API with a System Instruction to generate a single, unified YAML patch (the Fixed State) that resolves all issues.

- PR Agent:

    Role: Git Manager & Human-in-the-Loop Gate.

    Action: Uses PyGithub to commit the Fixed State to a new branch, pushes it to the remote repository, and opens a detailed Pull Request. It then pauses the entire execution, requiring manual terminal confirmation before completing.

![Alt Text (ConfigGuard Agent Workflow Diagram)](ConfigGuard%20Workflow.jpg "Optional Title")

# Installation 
Installation

This project was built against Python 3.10+.

Clone this repository (or your working directory):

    git clone [https://github.com/YourUsername/ConfigGuard-Agent-Capstone.git]
    (https://github.com/YourUsername/ConfigGuard-Agent-Capstone.git)
    cd ConfigGuard-Agent-Capstone


Create and activate a virtual environment (recommended):

    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    .\venv\Scripts\activate   # Windows


Install dependencies:

    pip install -r requirements.txt


Running the Agent

#### Configure Environment: Create a file named .env in the root directory and securely add your credentials and target repository details.

    .env (Make sure this file is excluded by .gitignore)
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    GITHUB_TOKEN="YOUR_GITHUB_PAT"

#### The target repository and file path to audit (must contain security flaws/drift)
    TARGET_REPO="YourUsername/example-voting-app-audit-target"
    CONFIG_PATH="k8s-specifications/vote-deployment.yaml"


 Define Golden State: Ensure your desired, secure configuration (with image tags and resource limits) is saved locally in:  
 
    config/intended_state.yaml.

Execute the Orchestrator:

    python main.py

# Project Structure

The project is organized to ensure clear separation of concerns, with each agent residing in its own file and the core orchestration logic managed centrally.

    .
    ├── config/
    │   └── intended_state.yaml  
    ├── agents/
    │   ├── audit_agent.py       
    │   ├── drift_agent.py      
    │   ├── ingest_agent.py     
    │   ├── fixer_agent.py      
    │   └── pr_agent.py          
    ├── main.py                  
    ├── .env                     
    ├── .gitignore             
    ├── requirements.txt         
    └── README.md                



