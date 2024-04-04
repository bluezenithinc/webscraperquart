from quart import render_template, request, session
from quart.views import MethodView

from qrt.utils.constants import DEFAULT_SCRAPING_OPTIONS
from qrt.utils.scraping import ScrapingOptions


class OptionsView(MethodView):
    async def get(self):
        options = ScrapingOptions(session)
        return await render_template(
            "scraper/partials/options_drawer.html", options=options
        )

    async def patch(self):
        payload = await request.get_json()
        payload = {
            k: v.strip() if isinstance(v, str) else v for k, v in payload.items()
        }

        for option, value in DEFAULT_SCRAPING_OPTIONS.items():
            if isinstance(value, bool):
                payload[option] = payload.get(option) == "on"

            if option == "ignoreCssSelectors":
                payload[option] = payload.get(option, "").split(",")

        options = ScrapingOptions(session).update(**payload)
        session["options"] = options.serialize()

        return await render_template(
            "scraper/partials/options_drawer.html",
            options=options,
        )
