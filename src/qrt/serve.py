import asyncio

from hypercorn.config import Config
from hypercorn.asyncio import serve

from qrt import create_app


def dev() -> None:
    app = create_app(mode="dev")
    app.run(debug=True, use_reloader=True)


def prod() -> None:
    app = create_app(mode="prod")
    asyncio.run(serve(app, Config()))


if __name__ == "__main__":
    dev()
