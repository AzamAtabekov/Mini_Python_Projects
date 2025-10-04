from urllib.parse import urljoin, urlparse
import urllib.robotparser as urp

class Robots:
    def __init__(self, base_url: str, user_agent: str):
        parsed = urlparse(base_url)
        self.base = f"{parsed.scheme}://{parsed.netloc}"
        self.user_agent = user_agent
        self.rp = urp.RobotFileParser()
        self.rp.set_url(urljoin(self.base, "/robots.txt"))
        try: self.rp.read()
        except Exception: pass

    def allowed(self, url: str) -> bool:
        try: return self.rp.can_fetch(self.user_agent, url)
        except Exception: return True
