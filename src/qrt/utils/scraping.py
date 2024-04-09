from urllib.parse import urlparse

from bs4 import BeautifulSoup
from quart.sessions import SessionMixin

from qrt.utils.string import camel_to_snake, snake_to_camel
from qrt.utils.constants import DEFAULT_SCRAPING_OPTIONS, ELEMENTS_TO_IGNORE


class ScrapingOptions:
    """
    Options for the scraper.

    Currently supported options:
    - `user_agent`: User-Agent header for the requests.
    - `preferred_language`: Accept-Language header for the requests.
    - `proxy`: The proxy to use for the requests.
    - `preserve_links`: Whether to preserve the links in the scraped content.
    - `include_images`: Whether to include images in the scraped content.
    """

    __slots__ = [
        "user_agent",
        "preferred_language",
        "proxy",
        "preserve_links",
        "include_images",
        "ignore_css_selectors",
    ]

    def __init__(self, session: SessionMixin = None, **kwargs: dict) -> None:
        self.user_agent: str = ""
        self.preferred_language: str = ""
        self.proxy: str = ""
        self.preserve_links: bool = False
        self.include_images: bool = False
        self.ignore_css_selectors: list = []

        if session:
            self.load_from_session(session)

        else:
            self.load_default()

        self.update(**kwargs)

    def __str__(self) -> str:
        return f"ScrapingOptions({', '.join([f'{key}={getattr(self, key)}' for key in self.__slots__])})"

    def load_default(self) -> None:
        """
        Loads the default options.

        The default options are defined in `DEFAULT_SCRAPING_OPTIONS` in `qrt.utils.constants`.
        """
        self.update(**DEFAULT_SCRAPING_OPTIONS)

    def load_from_session(self, session: SessionMixin) -> None:
        """
        Loads the options from the session.

        The session should contain a dictionary with the options.
        """
        session_options = {**DEFAULT_SCRAPING_OPTIONS, **session.get("options", {})}
        self.update(**session_options)

    def update(self, **kwargs: dict) -> "ScrapingOptions":
        """
        Updates the options with the provided keyword arguments.
        Supports both camelCase and snake_case keys.
        """
        for key, value in kwargs.items():
            setattr(self, key, value) if hasattr(self, key) else None
            (
                setattr(self, camel_to_snake(key), value)
                if hasattr(self, camel_to_snake(key))
                else None
            )

        return self

    def serialize(self) -> dict:
        """
        Serializes the options to a dictionary.
        """
        print(self)
        return {snake_to_camel(key): getattr(self, key) for key in self.__slots__}


def get_url_base(url: str) -> str:
    """
    Returns the base of the provided URL.

    Usage:
    >>> get_url_base("https://example.com/page")
    "https://example.com"
    """
    return f"{urlparse(url).scheme}://{urlparse(url).netloc}"


def externalize_href(href: str, url: str) -> str:
    """
    Externalizes the href attribute of an anchor tag.
    If the href is a relative path, it is converted to an absolute path.
    If the href is a hash link, the URL is prepended to it.
    Otherwise, the href is returned as is.

    Usage:
    >>> externalize_href("https://example.com/page", "/about")
    "https://example.com/about"

    >>> externalize_href("https://example.com/page", "#section")
    "https://example.com/page#section"
    """
    if href.startswith("/"):
        return f"{get_url_base(url)}{href}"

    if href.startswith("#"):
        return f"{url}{href}"

    return href


def remove_ignored_elements(
    soup: BeautifulSoup, ignored_elements: list
) -> BeautifulSoup:
    """
    Removes the ignored elements from the soup.

    The ignored elements are defined in `ELEMENTS_TO_IGNORE` in `qrt.utils.constants`.
    """
    for element in ignored_elements:
        for tag in soup.select(element):
            tag.decompose()

    return soup
