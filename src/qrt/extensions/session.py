from quart_session import Session as BaseSession

# types
from qrt.types import App


class Session(BaseSession):
    def init_app(self, app: App) -> None:
        super().init_app(app)


session = Session()
