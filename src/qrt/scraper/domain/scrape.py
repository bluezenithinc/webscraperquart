import regex as re
import sys
from traceback import format_exc
from urllib.parse import urlparse

from aiohttp import (
    ClientConnectionError,
    ClientSession,
    ClientTimeout,
    InvalidURL,
    ServerTimeoutError,
)
from bs4 import BeautifulSoup
from html2text import HTML2Text

from qrt.utils.constants import ELEMENTS_TO_IGNORE
from qrt.utils.scraping import ScrapingOptions, remove_ignored_elements
from qrt.utils.tailwind import TailwindClassesManager


async def scrape_url(url: str, options: ScrapingOptions):
    try:
        async with ClientSession(timeout=ClientTimeout(total=30)) as aiosession:
            async with aiosession.get(
                url,
                headers={
                    "User-Agent": options.user_agent,
                    "Accept-Language": options.preferred_language,
                    "Accept-Encoding": "gzip, deflate",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Referer": "https://www.google.com/",
                },
                proxy=options.proxy,
                verify_ssl=not options.proxy,
            ) as response:
                page_html = await response.text()

            elements_to_ignore = ELEMENTS_TO_IGNORE
            if not options.include_images:
                elements_to_ignore = ELEMENTS_TO_IGNORE + ["img"]
            if options.ignore_css_selectors:
                elements_to_ignore += options.ignore_css_selectors

            soup = remove_ignored_elements(
                BeautifulSoup(page_html, "lxml"), elements_to_ignore
            )

            title = soup.title.string

            soup = TailwindClassesManager(options=options).manage_soup(soup, url)

            markdowner = HTML2Text(bodywidth=0)
            markdowner.ignore_tables = True
            markdowner.ignore_images = not options.include_images
            markdowner.strong_mark = "**"
            markdowner.emphasis_mark = "__"

            markdown = markdowner.handle(soup.body.prettify())
            markdown == re.sub(r"\n{3,}", r"\n\n", markdown)

            content = soup.body.prettify()

            return {
                "title": title,
                "content": content,
                "extra": {
                    "menu": {
                        "clear": True,
                        "download_markdown": True,
                    },
                    "data": {
                        "url": url,
                        "domain": urlparse(url).netloc,
                        "markdown": markdown,
                    },
                },
            }

    except InvalidURL:
        return {
            "title": "Invalid URL",
            "content": "The URL you provided is invalid.",
            "extra": {"menu": {"clear": True}, "error": True, "data": {"url": url}},
        }

    except ServerTimeoutError:
        return {
            "title": "Timeout error",
            "content": "The request to the URL timed out.",
            "extra": {"menu": {"clear": True}, "error": True, "data": {"url": url}},
        }

    except ClientConnectionError:
        return {
            "title": "Connection error",
            "content": "There was an error connecting to the URL.",
            "extra": {"menu": {"clear": True}, "error": True, "data": {"url": url}},
        }

    except Exception as e:
        print(format_exc(), file=sys.stderr)
        return {
            "title": "Internal Server Error",
            "content": str(e),
            "extra": {"menu": {"clear": True}, "error": True, "data": {"url": url}},
        }
