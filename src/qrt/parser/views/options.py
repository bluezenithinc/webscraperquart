import json

from quart import render_template, request, session, current_app
from quart.views import MethodView

from qrt.utils.constants import DEFAULT_PARSER_OPTIONS


class OptionsView(MethodView):
    async def patch(self):
        payload = await request.get_json()
        payload = {
            k: v.strip() if isinstance(v, str) else v for k, v in payload.items()
        }

        old_options = session.get("options", {})

        options = {**DEFAULT_PARSER_OPTIONS, **old_options, **payload}
        session["options"] = options

        return await render_template(
            "parser/partials/options_drawer.html",
            options=options,
        )
