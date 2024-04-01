from traceback import format_exc

from aiohttp.client import ClientSession, ClientTimeout
from aiohttp.client_exceptions import (
    InvalidURL,
    ClientConnectionError,
    ServerTimeoutError,
)
from bs4 import BeautifulSoup
from quart import render_template, request, session, current_app
from quart.views import MethodView
from html2text import HTML2Text

from qrt.utils.constants import (
    ELEMENTS_TO_IGNORE,
    TAILWIND_CLASSES,
    DEFAULT_SCRAPING_OPTIONS,
)
from qrt.utils.scraping import ScrapingOptions, remove_ignored_elements
from qrt.utils.tailwind import TailwindClassesManager


class ScraperView(MethodView):
    async def get(self):
        options = ScrapingOptions(session)
        return await render_template(
            "scraper/page.html", options=options, tab="Scraper"
        )

    async def post(self):
        payload = await request.get_json()
        url = payload.get("url")
        options = ScrapingOptions(session)

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
            current_app.logger.error(format_exc())
            return await render_template(
                "scraper/partials/scraped_content.html",
                content=str(e),
                title="Internal Server Error",
                extra={"menu": {"clear": True}},
                error=True,
            )

        elements_to_ignore = ELEMENTS_TO_IGNORE
        if not options.include_images:
            elements_to_ignore = ELEMENTS_TO_IGNORE + ["img"]

        soup = remove_ignored_elements(
            BeautifulSoup(page_html, "lxml"), elements_to_ignore
        )

        title = soup.title.string

        soup = TailwindClassesManager(options=options).manage_soup(soup, url)

        markdowner = HTML2Text(bodywidth=0)
        markdowner.ignore_tables = True
        markdowner.ignore_images = not options.include_images

        markdown = markdowner.handle(soup.body.prettify())

        content = soup.body.prettify()

        return await render_template(
            "scraper/partials/scraped_content.html",
            content=content,
            title=title,
            extra={
                "menu": {
                    "clear": True,
                },
                "data": {
                    "markdown": markdown,
                },
            },
        )

    async def delete(self):
        return await render_template(
            "scraper/partials/scraped_content.html",
        )
