from bs4 import BeautifulSoup
from collections import Counter

STOP = {"the","a","an","and","or","of","to","in","on","for","is","it","this","that","with","as","at","by","from"}

def parse_html(url: str, html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    title = (soup.title.string or "").strip() if soup.title and soup.title.string else None
    h1 = [h.get_text(strip=True) for h in soup.find_all("h1")][:3]
    words = [w.lower().strip(".,:;!?()[]{}\"'") for w in soup.get_text(" ").split()]
    words = [w for w in words if w and w.isalpha() and w not in STOP]
    top_words = Counter(words).most_common(10)
    return {"url": url, "title": title, "h1": h1, "top_words": top_words}
