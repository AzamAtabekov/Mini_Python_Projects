#!/usr/bin/env python3
import argparse, json, os, re, sys
from pathlib import Path

# --------- правила ----------
RULES = [
    {
        "id": "aws_access_key",
        "name": "AWS Access Key",
        "severity": "high",
        "regex": re.compile(r'(?<![A-Z0-9])(AKIA|ASIA)[A-Z0-9]{16}(?![A-Z0-9])')
    },
    {
        "id": "jwt",
        "name": "JWT",
        "severity": "medium",
        "regex": re.compile(r'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}')
    },
    {
        "id": "private_key",
        "name": "Private Key Block",
        "severity": "high",
        "regex": re.compile(r'-----BEGIN (?:RSA|EC|DSA|OPENSSH|PGP)? ?PRIVATE KEY-----')
    },
    {
        "id": "generic_token",
        "name": "Generic API Token",
        "severity": "medium",
        "regex": re.compile(r'(?i)\b(token|secret|api[_-]?key|bearer)\b[^\n\r]{0,20}[:=]\s*[\'"]?([A-Za-z0-9_\-]{24,})')
    },
    {
        "id": "dotenv_password",
        "name": ".env password/secret",
        "severity": "medium",
        "regex": re.compile(r'(?i)^(?:\s*)?(?:password|passwd|secret|token|apikey)\s*=\s*.+')
    },
]

BINARY_EXT = {".png",".jpg",".jpeg",".gif",".pdf",".exe",".dll",".so",".dylib",".zip",".tar",".gz",".7z",".mp4",".mov"}
SKIP_DIRS_DEFAULT = {".git","node_modules","dist","build","venv",".venv","__pycache__"}

def load_gitignore(root: Path):
    patterns = []
    gi = root / ".gitignore"
    if gi.exists():
        for line in gi.read_text(errors="ignore").splitlines():
            t = line.strip()
            if not t or t.startswith("#"): 
                continue
            patterns.append(t)
    return patterns

def match_gitignore(path: Path, patterns, root: Path):
    rel = str(path.relative_to(root)).replace("\\","/")
    for p in patterns:
        if p.endswith("/"):
            if rel.startswith(p.rstrip("/")): return True
        elif p.startswith("*."):
            if rel.endswith(p[1:]): return True
        elif p == rel:
            return True
    return False

def iter_files(root: Path, excludes: set, gitignore_patterns):
    for dirpath, dirnames, filenames in os.walk(root):
        dp = Path(dirpath)
        dirnames[:] = [d for d in dirnames
                       if d not in excludes and not match_gitignore(dp / d, gitignore_patterns, root)]
        for f in filenames:
            p = dp / f
            if p.suffix.lower() in BINARY_EXT: 
                continue
            if match_gitignore(p, gitignore_patterns, root):
                continue
            yield p

def scan_file(path: Path):
    findings = []
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        return findings
    for i, line in enumerate(text.splitlines(), start=1):
        for rule in RULES:
            for m in rule["regex"].finditer(line):
                start, end = m.span()
                snippet = line[max(0,start-20):min(len(line), end+20)]
                findings.append({
                    "file": str(path),
                    "line": i,
                    "col": start+1,
                    "rule": rule["id"],
                    "name": rule["name"],
                    "severity": rule["severity"],
                    "match": m.group(0)[:80] + ("…" if len(m.group(0))>80 else ""),
                    "context": snippet
                })
    return findings

def main():
    ap = argparse.ArgumentParser(description="Scan repository/files for leaked secrets (defensive use).")
    ap.add_argument("path", help="Path to file or directory")
    ap.add_argument("--exclude", default="", help="Comma-separated dirs to exclude")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    root = Path(args.path).resolve()
    excludes = SKIP_DIRS_DEFAULT | {e.strip() for e in args.exclude.split(",") if e.strip()}
    gitignore_patterns = load_gitignore(root if root.is_dir() else root.parent)

    targets = [root] if root.is_file() else list(iter_files(root, excludes, gitignore_patterns))

    all_findings = []
    for p in targets:
        all_findings.extend(scan_file(p))

    if args.json:
        print(json.dumps({"findings": all_findings}, indent=2, ensure_ascii=False))
        return

    if not all_findings:
        print("No obvious secrets found.")
        return

    print(f"Potential secrets found: {len(all_findings)}\n")
    for f in all_findings:
        print(f"[{f['severity'].upper()}] {f['name']}  ({f['rule']})")
        print(f"  {f['file']}:{f['line']}:{f['col']}")
        print(f"  match:   {f['match']}")
        print(f"  context: …{f['context']}…\n")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python secretscout.py <path> [--exclude dir1,dir2] [--json]")
        print("Run only on code you own or have explicit permission to test.")
        sys.exit(1)
    main()
