# Simple Python Web Scraper

A small scraper built with [requests](https://requests.readthedocs.io/) and
[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/). It collects
quotes (text, author, tags) from [quotes.toscrape.com](https://quotes.toscrape.com),
a public site made for practicing web scraping, following pagination to the end.

## Setup

Requires Python 3.8+.

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python scraper.py                        # all pages -> quotes.json
python scraper.py -o quotes.csv          # save as CSV instead
python scraper.py --max-pages 2          # only the first 2 pages
python scraper.py --delay 2              # wait 2 seconds between requests
```

| Option | Default | Meaning |
| --- | --- | --- |
| `-o`, `--output` | `quotes.json` | Output file; `.csv` writes CSV, anything else writes JSON |
| `-p`, `--max-pages` | all | Stop after this many pages |
| `-d`, `--delay` | `1` | Seconds to wait between requests |
| `--url` | `https://quotes.toscrape.com/` | Page to start from |

Example JSON output:

```json
[
  {
    "text": "“The world as we have created it is a process of our thinking.”",
    "author": "Albert Einstein",
    "tags": ["change", "deep-thoughts", "thinking", "world"]
  }
]
```

## Tests

The tests parse a saved sample page, so they run without a network connection:

```bash
python -m unittest discover tests
```

## Adapting it to another site

The site-specific parts are the CSS selectors in `parse_quotes()` and
`next_page_url()` in `scraper.py`. Change those to match the new page's HTML.
Before scraping a site, check its terms of service and `robots.txt`, and keep
the delay between requests so you don't overload the server.
