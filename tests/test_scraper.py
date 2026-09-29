"""Offline tests: parse a saved sample page, no network needed."""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import scraper  # noqa: E402

SAMPLE = """
<div class="quote">
  <span class="text">“The world as we have created it is a process of our thinking.”</span>
  <span>by <small class="author">Albert Einstein</small></span>
  <div class="tags">
    <a class="tag" href="/tag/change/">change</a>
    <a class="tag" href="/tag/thinking/">thinking</a>
  </div>
</div>
<div class="quote">
  <span class="text">“A day without sunshine is like, you know, night.”</span>
  <span>by <small class="author">Steve Martin</small></span>
  <div class="tags"></div>
</div>
<nav><ul class="pager"><li class="next"><a href="/page/2/">Next</a></li></ul></nav>
"""


class ParseTests(unittest.TestCase):
    def test_parse_quotes(self):
        quotes = scraper.parse_quotes(SAMPLE)
        self.assertEqual(len(quotes), 2)
        self.assertEqual(quotes[0]["author"], "Albert Einstein")
        self.assertEqual(quotes[0]["tags"], ["change", "thinking"])
        self.assertEqual(quotes[1]["tags"], [])

    def test_next_page_url(self):
        self.assertEqual(scraper.next_page_url(SAMPLE, "https://quotes.toscrape.com/"),
                         "https://quotes.toscrape.com/page/2/")
        self.assertIsNone(scraper.next_page_url("<html></html>", "https://x/"))

    def test_save_json_and_csv(self):
        quotes = scraper.parse_quotes(SAMPLE)
        for ext in ("json", "csv"):
            path = f"/tmp/_scraper_test.{ext}"
            scraper.save(quotes, path)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Albert Einstein", content)
            os.remove(path)
        scraper.save(quotes, "/tmp/_scraper_test.json")
        with open("/tmp/_scraper_test.json", encoding="utf-8") as f:
            self.assertEqual(json.load(f), quotes)
        os.remove("/tmp/_scraper_test.json")


if __name__ == "__main__":
    unittest.main()
