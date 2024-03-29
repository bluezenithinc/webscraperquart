from urllib.parse import urlparse

from aiohttp.client import ClientSession, ClientTimeout
from aiohttp.client_exceptions import (
    InvalidURL,
    ClientConnectionError,
    ServerTimeoutError,
)
from bs4 import BeautifulSoup
from quart import render_template, request, session
from quart.views import MethodView
from html2text import HTML2Text

from qrt.utils.constants import (
    ELEMENTS_TO_IGNORE,
    TAILWIND_CLASSES,
    DEFAULT_SCRAPER_OPTIONS,
)


class ScraperView(MethodView):
    async def get(self):
        options = {**DEFAULT_SCRAPER_OPTIONS, **session.get("options", {})}
        return await render_template("scraper/page.html", options=options, tab="Scraper")

    async def post(self):
        payload = await request.get_json()
        url = payload.get("url")
        url_base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        options = {**DEFAULT_SCRAPER_OPTIONS, **session.get("options", {})}

        try:
            async with ClientSession(timeout=ClientTimeout(total=30)) as aiosession:
                async with aiosession.get(
                    url,
                    headers={
                        "User-Agent": options["userAgent"],
                        "Accept-Language": options["prefferedLanguage"],
                        "Accept-Encoding": "gzip, deflate",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Referer": "https://www.google.com/",
                    },
                    proxy=options.get("proxy"),
                    verify_ssl=not options.get("proxy"),
                ) as response:
                    page_html = await response.text()

        except InvalidURL:
            return await render_template(
                "scraper/partials/scraped_content.html",
                title="Invalid URL",
                content="The URL you provided is invalid.",
                extra={"menu": {"clear": True}},
                error=True,
            )

        except ServerTimeoutError:
            return await render_template(
                "scraper/partials/scraped_content.html",
                title="Timeout error",
                content="The request to the URL timed out.",
                extra={"menu": {"clear": True}},
                error=True,
            )

        except ClientConnectionError:
            return await render_template(
                "scraper/partials/scraped_content.html",
                title="Connection error",
                content="There was an error connecting to the URL.",
                extra={"menu": {"clear": True}},
                error=True,
            )

        except Exception as e:
            return await render_template(
                "scraper/partials/scraped_content.html",
                content=str(e),
                title="Internal Server Error",
                extra={"menu": {"clear": True}},
                error=True,
            )

        soup = BeautifulSoup(page_html, "lxml")

        title = soup.title.string

        for element in ELEMENTS_TO_IGNORE:
            for tag in soup.select(element):
                tag.decompose()

        # remove attributes from tags
        for tag in soup.find_all(True):
            href = tag.get("href")
            tag.attrs = {}
            if href:
                tag["class"] = TAILWIND_CLASSES.get(tag.name, "")[options.get("preserveLinks", True)]
                if options.get("preserveLinks"):
                    if href.startswith("/"):
                        href = f"{url_base}{href}"

                    if href.startswith("#"):
                        href = f"{url}{href}"

                    tag["href"] = href
                    tag["target"] = "_blank"
                    tag["rel"] = "noopener noreferrer"
            else:
                tagх["class"] = TAILWIND_CLASSES.get(tag.name, "")

        markdowner = HTML2Text(bodywidth=0)
        markdowner.ignore_tables = True
        markdowner.ignore_images = True

        markdown = markdowner.handle(soup.body.prettify())

        content = soup.body.prettify()

        return await render_template(
            "scraper/partials/scraped_content.html", content=content, title=title, extra={
                "menu": {
                    "clear": True,
                },
                "data": {
                    "markdown": markdown,
                },
            }
        )

    async def delete(self):
        return await render_template(
            "scraper/partials/scraped_content.html",
            title="Scraped Content",
            content="The scraped content will be displayed here.",
            error=True,
            extra={"menu": {}},
        )
