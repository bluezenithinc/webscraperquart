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
        )


cors = CORS()
