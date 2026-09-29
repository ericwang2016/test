"""Simple web scraper for https://quotes.toscrape.com, a site built for scraping practice.

Collects each quote's text, author and tags, follows the "Next" link across
pages, and writes the results to JSON or CSV.
"""

import argparse
import csv
import json
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
HEADERS = {"User-Agent": "simple-scraper/1.0 (+https://github.com/ericwang2016/test)"}


def fetch(url, session, timeout=10):
    """Download a page and return its HTML."""
    response = session.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def parse_quotes(html):
    """Extract quotes from one page. Returns a list of dicts."""
    soup = BeautifulSoup(html, "html.parser")
    quotes = []
    for block in soup.select("div.quote"):
        quotes.append({
            "text": block.select_one("span.text").get_text(strip=True),
            "author": block.select_one("small.author").get_text(strip=True),
            "tags": [tag.get_text(strip=True) for tag in block.select("a.tag")],
        })
    return quotes


def next_page_url(html, current_url):
    """Return the absolute URL of the next page, or None on the last page."""
    soup = BeautifulSoup(html, "html.parser")
    link = soup.select_one("li.next > a")
    return urljoin(current_url, link["href"]) if link else None


def scrape(start_url=BASE_URL, max_pages=None, delay=1.0):
    """Scrape pages starting at start_url, pausing `delay` seconds between requests."""
    results = []
    url = start_url
    pages = 0
    with requests.Session() as session:
        while url and (max_pages is None or pages < max_pages):
            print(f"Fetching {url}", file=sys.stderr)
            html = fetch(url, session)
            results.extend(parse_quotes(html))
            pages += 1
            url = next_page_url(html, url)
            if url:
                time.sleep(delay)
    return results


def save(quotes, path):
    """Write quotes to .json or .csv, chosen by the file extension."""
    if path.endswith(".csv"):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
            writer.writeheader()
            for q in quotes:
                writer.writerow({**q, "tags": ";".join(q["tags"])})
    else:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(quotes, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-o", "--output", default="quotes.json",
                        help="output file, .json or .csv (default: quotes.json)")
    parser.add_argument("-p", "--max-pages", type=int, default=None,
                        help="stop after this many pages (default: all)")
    parser.add_argument("-d", "--delay", type=float, default=1.0,
                        help="seconds to wait between requests (default: 1)")
    parser.add_argument("--url", default=BASE_URL, help="page to start from")
    args = parser.parse_args()

    try:
        quotes = scrape(args.url, args.max_pages, args.delay)
    except requests.RequestException as e:
        sys.exit(f"Request failed: {e}")

    save(quotes, args.output)
    print(f"Saved {len(quotes)} quotes to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
