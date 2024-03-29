import json
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
    DEFAULT_PARSER_OPTIONS,
)


class ParserView(MethodView):
    async def get(self):
        options = session.get("options", DEFAULT_PARSER_OPTIONS)
        return await render_template("parser/page.html", options=options, tab="Parser")

    async def post(self):
        payload = await request.get_json()
        url = payload.get("url")
        url_base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        options = session.get("options", DEFAULT_PARSER_OPTIONS)

        try:
            async with ClientSession(timeout=ClientTimeout(total=30)) as aiosession:
                async with aiosession.get(
                    url,
                    headers={
                        "User-Agent": options["userAgent"],
                        "Accept-Language": options["prefferedLanguage"],
                        "Accept-Encoding": "gzip, deflate",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Referer": "https://www.google.com/",
                    },
                    proxy=options.get("proxy"),
                    verify_ssl=not options.get("proxy"),
                ) as response:
                    response_text = await response.text()

        except InvalidURL:
            return await render_template(
                "parser/partials/parsed_content.html",
                title="Invalid URL",
                content="The URL you provided is invalid.",
                error=True,
            )

        except ServerTimeoutError:
            return await render_template(
                "parser/partials/parsed_content.html",
                title="Timeout error",
                content="The request to the URL timed out.",
                error=True,
            )

        except ClientConnectionError:
            return await render_template(
                "parser/partials/parsed_content.html",
                title="Connection error",
                content="There was an error connecting to the URL.",
                error=True,
            )

        except Exception as e:
            return await render_template(
                "parser/partials/parsed_content.html",
                content=str(e),
                title="Internal Server Error",
                error=True,
            )

        soup = BeautifulSoup(response_text, "lxml")

        title = soup.title.string

        for element in ELEMENTS_TO_IGNORE:
            for tag in soup.select(element):
                tag.decompose()

        # remove attributes from tags
        for tag in soup.find_all(True):
            href = tag.get("href")
            tag.attrs = {
                "class": TAILWIND_CLASSES.get(tag.name, ""),
            }
            if href:
                if href.startswith("/"):
                    href = f"{url_base}{href}"

                if href.startswith("#"):
                    href = f"{url}{href}"

                tag["href"] = href
                tag["target"] = "_blank"
                tag["rel"] = "noopener noreferrer"

        markdowner = HTML2Text(bodywidth=0)
        markdowner.ignore_tables = True
        markdowner.ignore_images = True

        content = soup.body.prettify()

        return await render_template(
            "parser/partials/parsed_content.html", content=content, title=title
        )
