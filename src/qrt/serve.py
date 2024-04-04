import os
import sys

import asyncio

from dotenv import load_dotenv
from hypercorn.config import Config
from hypercorn.asyncio import serve

from qrt import create_app

load_dotenv()


def dev() -> None:
    app = create_app(mode="dev")
    app.run(debug=True, use_reloader=True)


def prod() -> None:
    app = create_app(mode="prod")
    asyncio.run(
        serve(
            app,
            Config.from_mapping(
                {
                    "bind": ["0.0.0.0:8000"],
                }
            ),
        )
    )


if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else os.getenv("ENV", "dev")
    print(f"Running in {env} mode")
    {"dev": dev, "prod": prod}[env]()
