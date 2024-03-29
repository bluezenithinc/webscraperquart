from quart import render_template, request, session
from quart.views import MethodView

from qrt.utils.constants import DEFAULT_SCRAPER_OPTIONS


class OptionsView(MethodView):
    async def get(self):
        options = {**DEFAULT_SCRAPER_OPTIONS, **session.get("options", {})}
        return await render_template("scraper/partials/options_drawer.html", options=options)

    async def patch(self):
        payload = await request.get_json()
        payload = {
            k: v.strip() if isinstance(v, str) else v for k, v in payload.items()
        }

        for option, value in DEFAULT_SCRAPER_OPTIONS.items():
            if isinstance(value, bool):
                payload[option] = payload.get(option) == "on"

        old_options = session.get("options", {})

        options = {**DEFAULT_SCRAPER_OPTIONS, **old_options, **payload}
        session["options"] = options

        return await render_template(
            "scraper/partials/options_drawer.html",
            options=options,
        )
