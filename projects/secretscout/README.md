# secretscout

A minimal Python-based secret scanner for files and repositories.  
It detects hardcoded credentials, tokens, and private keys in your codebase.  
> Use **only** on code you own or have explicit permission to test.

---

## Features
- Detects common sensitive patterns:
  - AWS Access Keys
  - JWT tokens
  - Private key blocks
  - Generic API tokens
  - `.env` secrets and passwords
- Skips binaries and files ignored by `.gitignore`
- Outputs to console or JSON
- Simple CLI interface

---

## Installation

**Bash / Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**PowerShell / Windows**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Usage

### Scan current directory
**Bash**
```bash
python projects/secretscout/secretscout.py .
```

**PowerShell**
```powershell
python .\projects\secretscout\secretscout.py .
```

### Scan a specific folder
**Bash**
```bash
python projects/secretscout/secretscout.py /path/to/project
```

**PowerShell**
```powershell
python .\projects\secretscout\secretscout.py D:\path\to\project
```

### Scan a single file
**Bash**
```bash
python projects/secretscout/secretscout.py /path/to/file.txt
```

**PowerShell**
```powershell
python .\projects\secretscout\secretscout.py .\projects\secretscout\sample\test_env.txt
```

### Exclude directories
```bash
python projects/secretscout/secretscout.py . --exclude node_modules,venv,__pycache__
```

### JSON output
```bash
python projects/secretscout/secretscout.py . --json > report.json
```

---

## Example Output

**Console**
```
Potential secrets found: 1

[MEDIUM] .env password/secret  (dotenv_password)
  projects/secretscout/sample/test_env.txt:1:1
  match:   PASSWORD=supersecret123
  context: …PASSWORD=supersecret123…
```

**JSON**
```json
{
  "findings": [
    {
      "file": "projects/secretscout/sample/test_env.txt",
      "line": 1,
      "col": 1,
      "rule": "dotenv_password",
      "name": ".env password/secret",
      "severity": "medium",
      "match": "PASSWORD=supersecret123",
      "context": "PASSWORD=supersecret123"
    }
  ]
}