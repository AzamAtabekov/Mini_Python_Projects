# SiteAnalyzer

Small, async website analyzer in Python.  
Crawls pages within a domain, collects status codes, titles, basic text signals, and links.  
Respects `robots.txt` by default, supports depth/page limits, concurrency and delay.

> ⚠️ Use on **your own sites** or with explicit permission from the owner.

---

## Features

- Async fetching via `httpx` (HTTP/1.1 + optional HTTP/2)
- Respect for `robots.txt` (can be disabled)
- Configurable:
  - max depth, max pages
  - concurrency & polite delay between requests
  - follow or ignore external links
- Outputs:
  - `reports/report.json` — detailed, per-page data
  - `reports/summary.csv` — compact table for quick review (openable in Excel)

---

## Project layout

```
src/site_analyzer/
  __init__.py
  cli.py          # CLI entry point
  crawler.py      # BFS queue, depth/limits, domain filtering
  fetcher.py      # httpx client + response handling
  parser.py       # BeautifulSoup, titles/H1, simple word stats
  reporters.py    # JSON/CSV writers
  robots.py       # robots.txt checks
  utils.py        # URL normalization, domain checks, etc.
```

---

## Requirements

Project-local runtime deps (`projects/siteanalyzer/requirements.txt`):

```
httpx[http2]
beautifulsoup4
lxml
tldextract
```

> In your repo root you may also keep a **global** requirements file for dev tools (black, ruff, pytest, etc.), shared by all mini-projects.

---

## Quick start

From your repo root, activate your venv, then switch to the project folder:

```powershell
# Windows PowerShell example
& D:\Mini_Python_Projects\venv\Scripts\Activate.ps1
cd D:\Mini_Python_Projects\projects\siteanalyzer

# install project deps
pip install -r requirements.txt
```

Run a tiny test crawl (fast, safe):

```powershell
# add src/ to import path (since we don’t install the package)
$env:PYTHONPATH = "src"
python -m site_analyzer.cli https://example.com --max-depth 1 --max-pages 3 -o .\reports
```

You should see:

- `reports/report.json`  
- `reports/summary.csv`

---

## Usage

```text
python -m site_analyzer.cli URL [options]
```

Common options:

- `-d, --max-depth INT` — crawl depth (default: 2)  
- `-n, --max-pages INT` — page limit (default: 200)  
- `-c, --concurrency INT` — concurrent requests (default: 5)  
- `--delay FLOAT` — delay (seconds) between requests (default: 0.5)  
- `--follow-external` — follow external domains (off by default)  
- `--ignore-robots` — ignore robots.txt (not recommended)  
- `-o, --out PATH` — output directory (default: `./reports`)

Examples:

```powershell
# Fast smoke test: home page + immediate links
$env:PYTHONPATH="src"
python -m site_analyzer.cli https://example.com --max-depth 1 --max-pages 5 -o .\reports

# Slightly deeper, still bounded
$env:PYTHONPATH="src"
python -m site_analyzer.cli https://example.com --max-depth 2 --max-pages 20 --delay 0.5 -o .\reports

# Explore external links (can grow fast)
$env:PYTHONPATH="src"
python -m site_analyzer.cli https://example.com --max-depth 1 --max-pages 30 --follow-external -o .\reports
```

> Prefer starting with small limits on unfamiliar sites.

---

## Output format

### `summary.csv` (columns)

- `url` — page URL  
- `status` — HTTP status (e.g., 200, 301, 404)  
- `depth` — crawl depth  
- `response_time_ms` — response latency  
- `content_length` — bytes received  
- `title` — `<title>` content, if present

### `report.json` (per-page fields)

- `url`, `status`, `depth`  
- `content_length`, `response_time_ms`  
- `title`, `h1` (up to first three)  
- `internal_links`, `external_links`

---

## Optional: install as a console command

If you prefer running `site-analyzer ...` instead of `python -m ...`, add a minimal `setup.py` in the project root:

```python
from setuptools import setup, find_packages

setup(
    name="site-analyzer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["httpx[http2]", "beautifulsoup4", "lxml", "tldextract"],
    entry_points={"console_scripts": ["site-analyzer = site_analyzer.cli:main"]},
)
```

Then:

```powershell
pip install -e .
site-analyzer https://example.com --max-depth 1 --max-pages 5 -o .\reports
```

*(If you prefer `pyproject.toml`, you can use that instead. For mini-projects, `setup.py` is the lightest option.)*

---

## Troubleshooting

**`ModuleNotFoundError: site_analyzer`**  
You likely didn’t set `PYTHONPATH`. Run from the project folder and:

```powershell
$env:PYTHONPATH = "src"
python -m site_analyzer.cli https://example.com --max-pages 3
```

**Windows console shows encoding issues**  
Before running:

```powershell
[Console]::OutputEncoding = [Text.UTF8Encoding]::new()
chcp 65001 | Out-Null
```

**Crawl is too slow or too fast**  
Tune `--concurrency` and `--delay`, and keep `--max-pages` and `--max-depth` small for tests.

---

## .gitignore (recommended)

Add to the repo’s root `.gitignore`:

```
projects/siteanalyzer/reports/
projects/siteanalyzer/.pytest_cache/
projects/siteanalyzer/**/__pycache__/
```

---

## License

See the repository’s root `LICENSE`.
