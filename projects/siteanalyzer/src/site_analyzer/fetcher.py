import httpx
from .constants import TEXT_MIME_PREFIXES

class FetchResult:
    def __init__(self, url: str, status: int | None, content: bytes, text: str | None, headers: dict, elapsed_ms: int):
        self.url = url
        self.status = status
        self.content = content
        self.text = text
        self.headers = headers
        self.elapsed_ms = elapsed_ms

async def fetch(client: httpx.AsyncClient, url: str, timeout: float = 15.0) -> FetchResult | None:
    try:
        resp = await client.get(url, timeout=timeout, follow_redirects=True)
        ctype = resp.headers.get("content-type", "").lower()
        text = resp.text if any(ctype.startswith(p) for p in TEXT_MIME_PREFIXES) else None
        return FetchResult(
            url=str(resp.url),
            status=resp.status_code,
            content=resp.content,
            text=text,
            headers=dict(resp.headers),
            elapsed_ms=int(resp.elapsed.total_seconds() * 1000),
        )
    except httpx.HTTPError:
        return None
