from bs4 import BeautifulSoup, PageElement

from .constants import TAILWIND_CLASSES
from .scraping import externalize_href, ScrapingOptions


class TailwindClassesManager:
    """
    This class assings tailwind classes to the html elements based on the element name.
    """

    def __init__(
        self,
        options: ScrapingOptions = ScrapingOptions(),
        classes: list = TAILWIND_CLASSES,
    ):
        self.options: ScrapingOptions = options
        self.classes: list = classes

    def add_class(self, element: PageElement) -> PageElement:
        """
        Adds a tailwind class to the element.

        If the element is an anchor tag, it is processed separately.

        Usage:
        >>> add_class(BeautifulSoup('<h1>Title</h1>', "html.parser"))
        <h1 class="text-2xl">Title</h1>
        """
        if element.name == "a":
            element["class"] = self.classes.get(element.name, "")[
                self.options.preserve_links
            ]
        else:
            element["class"] = self.classes.get(element.name, "")
        return element

    def make_anchor_attrs(self, element: PageElement, url: str) -> dict:
        """
        Processes the anchor tag.

        Externalizes the href attribute and adds the target and rel attributes so that the links open in a new tab.

        Usage:
        >>> process_anchor(BeautifulSoup('<a href="/page">Page</a>', "lxml"))
        <a href="https://example.com/page" target="_blank" rel="noopener noreferrer">Page</a>
        """
        href = element.get("href")
        if not href:
            return {}

        return {
            "href": externalize_href(href, url),
            "target": "_blank",
            "rel": "noopener noreferrer",
        }

    def manage_soup(self, soup: BeautifulSoup, url: str) -> BeautifulSoup:
        """
        Removes most attributes from the html elements and assigns tailwind classes to the html elements.

        Usage:
        >>> assign_classes(BeautifulSoup('<h1><a href="/page">Title</a></h1>', "lxml"), "https://example.com")
        <p class="text-base"><a href="https://example.com/page" target="_blank" rel="noopener noreferrer">Title</a><p>
        """
        for element in soup.find_all(True):
            if element.name == "a":
                element.attrs = self.make_anchor_attrs(element, url)

            elif element.name in [
                "img",
            ]:
                element.attrs = {"src": element.get("src"), "alt": element.get("alt")}

            else:
                element.attrs = {}
            element = self.add_class(element)
        return soup
