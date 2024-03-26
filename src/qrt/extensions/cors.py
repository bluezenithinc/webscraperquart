import re

from quart_cors import cors as base_cors

from qrt.extensions.base import AppExtension

# types
from qrt.types import App


class CORS(AppExtension):
    """
    CORS extension.
    Controls cross-origin resource sharing.
    """

    def init_app(self, app: App) -> None:
        base_cors(
            app_or_blueprint=app,
            allow_origin=app.config.get("CORS_ALLOW_ORIGIN", "*"),
            allow_headers=[
                # standard htmx headers
                "HX-Boosted",
                "HX-Current-URL",
                "HX-History-Restore-Request",
                "HX-Prompt",
                "HX-Request",
                "HX-Target",
                "HX-Trigger-Name",
                "HX-Trigger",
            ],
            expose_headers=[
                # standard htmx headers
                "HX-Location",
                "HX-Push-Url",
                "HX-Redirect",
                "HX-Refresh",
                "HX-Replace-Url",
                "HX-Reswap",
                "HX-Retarget",
                "HX-Reselect",
                "HX-Trigger",
                "HX-Trigger-After-Settle",
                "HX-Trigger-After-Swap",
            ],
        )


cors = CORS()
