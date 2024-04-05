from bs4 import BeautifulSoup

from qrt.utils.constants import DEFAULT_SCRAPING_OPTIONS
from qrt.utils.scraping import (
    externalize_href,
    get_url_base,
    remove_ignored_elements,
    ScrapingOptions,
)


def test_get_url_base():
    assert get_url_base("https://example.com/page") == "https://example.com"
    assert (
        get_url_base("https://example.com/page?query=string") == "https://example.com"
    )
    assert get_url_base("https://example.com/page#section") == "https://example.com"
    assert (
        get_url_base("https://example.com/page?query=string#section")
        == "https://example.com"
    )


def test_externalize_href():
    assert (
        externalize_href("/about", "https://example.com/page")
        == "https://example.com/about"
    )
    assert (
        externalize_href("#section", "https://example.com/page")
        == "https://example.com/page#section"
    )
    assert (
        externalize_href("https://example.com/about", "https://example.com/page")
        == "https://example.com/about"
    )


def test_remove_ignored_elements():
    soup = BeautifulSoup(
        """
        <html>
            <head>
                <title>Test</title>
            </head>
            <body>
                <h1>Heading</h1>
                <p>Paragraph</p>
                <img src="image.jpg" />
            </body>
        </html>
        """,
        "html.parser",
    )

    soup = remove_ignored_elements(soup, ["img"])

    assert not soup.find("img")
    assert soup.find("h1")


def test_scraping_options():
    options = ScrapingOptions(
        user_agent="Mozilla/5.0",
        preferred_language="en-US",
        preserve_links=True,
        include_images=True,
        ignore_css_selectors=[".hidden"],
        proxy="http://proxy.com",
    )
    assert options.serialize()["userAgent"] == "Mozilla/5.0"

    options.update(preserve_links=False)
    assert options.serialize()["preserveLinks"] == False

    options.load_default()
    assert (
        options.serialize()["includeImages"]
        == DEFAULT_SCRAPING_OPTIONS["includeImages"]
    )

    options.load_from_session({"options": {"ignoreCssSelectors": [".cookie-banner"]}})
    assert options.serialize()["ignoreCssSelectors"] == [".cookie-banner"]
