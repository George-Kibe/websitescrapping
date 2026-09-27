"""
Extract phone numbers and email addresses from a web page.

Usage:
    python contact_extractor.py http://acumenvaluers.co.ke/
"""

import argparse
import re

from bs4 import BeautifulSoup

from common import get_soup

PHONE_RE = re.compile(r"\+?\(?\d{2,4}\)?[\s.-]?\d{3}[\s.-]?\d{3,4}")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def extract_contacts(soup: BeautifulSoup) -> tuple[list[str], list[str]]:
    """Return (phones, emails) found in the page text and tel:/mailto: links."""
    text = soup.get_text(" ")
    phones = set(PHONE_RE.findall(text))
    emails = set(EMAIL_RE.findall(text))

    for link in soup.select('a[href^="tel:"], a[href^="mailto:"]'):
        scheme, _, value = link["href"].partition(":")
        value = value.split("?")[0].strip()
        if value:
            (phones if scheme == "tel" else emails).add(value)

    return sorted(p.strip() for p in phones), sorted(emails)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("url", nargs="?", default="http://acumenvaluers.co.ke/")
    args = parser.parse_args()

    phones, emails = extract_contacts(get_soup(args.url))
    print("Phones:", ", ".join(phones) or "none found")
    print("Emails:", ", ".join(emails) or "none found")


if __name__ == "__main__":
    main()
