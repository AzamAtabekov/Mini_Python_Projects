import argparse, asyncio
from pathlib import Path
from .crawler import crawl
from .reporters import save_json, save_csv_summary

def main():
    p = argparse.ArgumentParser(prog="site-analyzer", description="Analyze owned/authorized websites politely.")
    p.add_argument("url")
    p.add_argument("-d","--max-depth", type=int, default=2)
    p.add_argument("-n","--max-pages", type=int, default=200)
    p.add_argument("-c","--concurrency", type=int, default=5)
    p.add_argument("--delay", type=float, default=0.5)
    p.add_argument("--ignore-robots", action="store_true")
    p.add_argument("--follow-external", action="store_true")
    p.add_argument("-o","--out", default="./reports")
    args = p.parse_args()

    results = asyncio.run(crawl(
        args.url,
        max_depth=args.max_depth,
        max_pages=args.max_pages,
        concurrency=args.concurrency,
        delay=args.delay,
        respect_robots=not args.ignore_robots,
        follow_external=args.follow_external,
    ))
    out = Path(args.out)
    save_json(results, out)
    save_csv_summary(results, out)
    print(f"Saved: {out}/report.json and {out}/summary.csv")

if __name__ == "__main__":
    main()
