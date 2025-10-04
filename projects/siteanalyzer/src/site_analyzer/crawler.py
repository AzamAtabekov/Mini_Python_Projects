import asyncio
from bs4 import BeautifulSoup
import httpx
from .constants import DEFAULT_USER_AGENT, IGNORE_EXTENSIONS
from .utils import normalize_url, is_same_reg_domain, has_ignored_ext
from .robots import Robots
from .fetcher import fetch
from .parser import parse_html

async def crawl(
    start_url: str,
    *,
    max_depth: int = 2,
    max_pages: int = 200,
    concurrency: int = 5,
    delay: float = 0.5,
    respect_robots: bool = True,
    follow_external: bool = False,
    user_agent: str = DEFAULT_USER_AGENT,
):
    queue: asyncio.Queue[tuple[str,int]] = asyncio.Queue()
    await queue.put((start_url, 0))
    visited: set[str] = set()
    results: list[dict] = []

    robots = Robots(start_url, user_agent) if respect_robots else None
    limits = httpx.Limits(max_keepalive_connections=concurrency)
    async with httpx.AsyncClient(headers={"User-Agent": user_agent}, limits=limits) as client:
        sem = asyncio.Semaphore(concurrency)

        async def worker():
            nonlocal results
            while len(results) < max_pages:
                try:
                    url, depth = await asyncio.wait_for(queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    break
                if url in visited:
                    queue.task_done(); continue
                visited.add(url)

                if robots and not robots.allowed(url):
                    queue.task_done(); continue
                if has_ignored_ext(url, IGNORE_EXTENSIONS):
                    queue.task_done(); continue

                await asyncio.sleep(delay)
                async with sem:
                    fres = await fetch(client, url)

                page = {"url": url, "status": None, "depth": depth,
                        "content_length": None, "response_time_ms": None,
                        "title": None, "h1": [], "internal_links": [], "external_links": []}

                if not fres:
                    results.append(page); queue.task_done(); continue

                page["status"] = fres.status
                page["content_length"] = len(fres.content) if fres.content else None
                page["response_time_ms"] = fres.elapsed_ms

                if fres.text:
                    parsed = parse_html(fres.url, fres.text)
                    page.update({k: parsed.get(k) for k in ("title","h1")})
                    soup = BeautifulSoup(fres.text, "lxml")
                    for a in soup.find_all(["a","area"]):
                        link = normalize_url(fres.url, a.get("href"))
                        if not link or has_ignored_ext(link, IGNORE_EXTENSIONS):
                            continue
                        same = is_same_reg_domain(start_url, link)
                        (page["internal_links"] if same else page["external_links"]).append(link)
                        if (same or follow_external) and depth + 1 <= max_depth and link not in visited:
                            await queue.put((link, depth + 1))

                results.append(page)
                queue.task_done()

        workers = [asyncio.create_task(worker()) for _ in range(concurrency)]
        await queue.join()
        for w in workers: w.cancel()
    return results
