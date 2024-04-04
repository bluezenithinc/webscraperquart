from quart import render_template, request, session
from quart.views import MethodView

from qrt.scraper.domain import scrape_url
from qrt.utils.scraping import ScrapingOptions


class ScraperView(MethodView):
    async def get(self):
        url = request.args.get("url")
        options = ScrapingOptions(session)

        scraped = {}
        if url:
            scraped = await scrape_url(url, options)

        return await render_template(
            "scraper/page.html", options=options, tab="Scraper", **scraped
        )

    async def post(self):
        payload = await request.get_json()
        url = payload.get("url")
        options = ScrapingOptions(session)

        scraped = await scrape_url(url, options)

        return await render_template(
            "scraper/partials/scraped_content.html",
            **scraped,
        )

    async def delete(self):
        return await render_template("scraper/partials/scraped_content.html", extra={})
