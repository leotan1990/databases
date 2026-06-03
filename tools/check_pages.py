#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import sys


LEGAL_PAGES = [
    Path("AppStore/privacy_en.html"),
    Path("AppStore/privacy_zh-CN.html"),
    Path("AppStore/terms_en.html"),
    Path("AppStore/terms_zh-CN.html"),
]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(1)


def check_legal_pages():
    for path in LEGAL_PAGES:
        text = path.read_text()
        lower = text.lower()

        if "cocoa html writer" in lower:
            fail(f"{path}: contains Cocoa HTML Writer markup")
        if "file:///" in lower:
            fail(f"{path}: contains local file:// links")
        if 'href="styles/legal.css"' not in text:
            fail(f"{path}: missing shared legal stylesheet")
        if '<div class="container">' not in text:
            fail(f"{path}: missing styled container")
        if "<html" not in lower or "</html>" not in lower:
            fail(f"{path}: missing html root")
        if "</head>" not in lower or "</body>" not in lower:
            fail(f"{path}: missing head/body close tags")

        parser = LinkParser()
        parser.feed(text)
        local_hrefs = [
            href
            for href in parser.hrefs
            if not href.startswith(("http://", "https://", "mailto:"))
        ]
        missing = [
            href
            for href in local_hrefs
            if not (path.parent / href).is_file()
        ]
        if missing:
            fail(f"{path}: missing local link targets: {missing}")

        stylesheet = path.parent / "styles/legal.css"
        if not stylesheet.is_file():
            fail(f"{path}: missing stylesheet target: {stylesheet}")


def check_homepage_links():
    parser = LinkParser()
    parser.feed(Path("index.html").read_text())
    local_hrefs = [
        href
        for href in parser.hrefs
        if not href.startswith(("http://", "https://", "mailto:"))
    ]
    missing = [href for href in local_hrefs if not Path(href).is_file()]
    if missing:
        fail(f"index.html: missing local link targets: {missing}")


def main():
    check_legal_pages()
    check_homepage_links()
    print("Page checks passed")


if __name__ == "__main__":
    main()
