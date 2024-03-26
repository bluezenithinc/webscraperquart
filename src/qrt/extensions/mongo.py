import os

from quart_motor import Motor as BaseMotor

# types
from qrt.types import App


class Motor(BaseMotor):
    """
    Motor extension.
    Gives access to MongoDB.
    """

    def init_app(self, app: App) -> None:
        super().init_app(app, uri=app.config.get("MONGO_URI"))


mongo = Motor()
