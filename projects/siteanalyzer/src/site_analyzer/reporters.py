import json, csv
from pathlib import Path

def save_json(data: list[dict], out_dir: str | Path, name: str = "report.json"):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    (out / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def save_csv_summary(data: list[dict], out_dir: str | Path, name: str = "summary.csv"):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    fields = ["url","status","depth","response_time_ms","content_length","title"]
    with open(out / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for row in data: w.writerow({k: row.get(k) for k in fields})
