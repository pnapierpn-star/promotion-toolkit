import urllib.request
from html.parser import HTMLParser

URL = "https://www.paulnapierskie.com/"

class SEOParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.h1_count = 0
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and attrs.get("name", "").lower() == "description":
            self.description = attrs.get("content", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data

def main():
    print("Auditing:", URL)
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 SEO-Audit/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8", errors="replace")
        print("HTTP status:", response.status)

    parser = SEOParser()
    parser.feed(html)

    print("Title:", parser.title.strip() or "MISSING")
    print("Meta description:", parser.description or "MISSING")
    print("H1 headings:", parser.h1_count)

if __name__ == "__main__":
    main()
