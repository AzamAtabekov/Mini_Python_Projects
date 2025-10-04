from urllib.parse import urljoin, urlparse
import tldextract

def normalize_url(base: str, link: str | None) -> str | None:
    if not link or link.startswith(("mailto:", "javascript:", "tel:")):
        return None
    return urljoin(base, link.split("#")[0].strip())

def is_same_reg_domain(a: str, b: str) -> bool:
    ea = tldextract.extract(a)
    eb = tldextract.extract(b)
    return ea.domain == eb.domain and ea.suffix == eb.suffix

def has_ignored_ext(url: str, ignore_exts: tuple[str, ...]) -> bool:
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in ignore_exts)
