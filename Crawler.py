from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import re

visited = set()

def crawl(url, domain):
    global visited

    if url in visited:
        return
    visited.add(url)

    print(f"\n[PAGE] {url}")
    time.sleep(1)  # rate limiting for safety

    try:
        html = urlopen(url)
        bs = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(f"[ERROR] Cannot open {url} — {e}")
        return

    # Print page title
    if bs.title:
        print("[TITLE]", bs.title.get_text())

    # Follow links
    for link in bs.find_all("a", href=True):
        href = link["href"]
        absolute = urljoin(url, href)

        # Stay inside the same domain
        if urlparse(absolute).netloc != domain:
            continue

        # Skip non-HTML files
        if re.search(r"\.(jpg|png|pdf|zip|exe|mp4|css|js)$", absolute):
            continue

        if absolute not in visited:
            print(" └── Found:", absolute)
            crawl(absolute, domain)


def start(url):
    domain = urlparse(url).netloc
    print("[STARTING DOMAIN]:", domain)
    crawl(url, domain)


# Example:
start("https://example.com")

